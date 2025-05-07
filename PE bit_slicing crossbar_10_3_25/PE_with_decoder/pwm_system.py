import configparser
from pathlib import Path
import numpy as np
from components.Dac import DAC
from components.Decoder import Decoder
from components.Crossbar import Crossbar
from components.subtractor import Subtractor
from components.Ramp_generator import RampGenerator
from components.Comparator import Comparator
from components.tdc import TDC
from Energy_metrics import EnergyMetrics
from Delay_metrics import DelayMetrics
from Power_metrics import PowerMetrics
from Area_metrics import AreaMetrics

class PWMSystem:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.num_bits = self.config.getint('DAC', 'num_bits')
        self._initialize_components()
        self._initialize_metrics()
        
    def _load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config
        
    def _initialize_components(self):
        # Initialize all components with configuration parameters
        self.decoder = Decoder(
            num_bits=self.config.getint('DAC', 'num_bits')
        )
        self.dac = DAC(
            num_bits=self.config.getint('DAC', 'num_bits'),
            pulse_period=self.config.getfloat('DAC', 'pulse_period'),
            Vdd=self.config.getfloat('System', 'Vdd')
        )
        
        self.crossbar = Crossbar(
            Ron=self.config.getfloat('Crossbar', 'Ron'),
            Roff=self.config.getfloat('Crossbar', 'Roff'),
            on_off_ratio=self.config.getfloat('Crossbar', 'on_off_ratio'),
            capacitance=self.config.getfloat('Crossbar', 'capacitance'),
            Vdd=self.config.getfloat('System', 'Vdd'),
            pulse_period=self.config.getfloat('DAC', 'pulse_period'),
            array_rows=self.config.getint('Crossbar', 'array_rows'),
            array_columns=self.config.getint('Crossbar', 'array_columns'),
            A=self.config.getfloat('Crossbar', 'A'),
            weight_bits=self.config.getint('Crossbar', 'weight_bits'),
            vin=self.config.getfloat('Crossbar', 'vin')
        )
        
        # Initialize 16 subtractors
        self.subtractors = [Subtractor() for _ in range(16)]
        
        self.ramp_generator = RampGenerator(
            slope=self.config.getfloat('RampGenerator', 'slope'),
            time_step=self.config.getfloat('System', 'time_step')
        )
        self.comparator = Comparator()
        self.tdc = TDC(
            num_tdc=self.config.getint('TDC', 'num_tdc'),
            time_precision=self.config.getfloat('TDC', 'time_precision')
        )
        
    def _initialize_metrics(self):
        # Create components dictionary for metrics calculators
        self.components = {
            'decoder': self.decoder,
            'dac': self.dac,
            'crossbar': self.crossbar,
            'subtractors': self.subtractors,
            'ramp_generator': self.ramp_generator,
            'comparator': self.comparator,
            'tdc': self.tdc
        }
        
        # Initialize metrics calculators
        self.energy_metrics = EnergyMetrics(self.components)
        self.delay_metrics = DelayMetrics(self.components)
        self.power_metrics = PowerMetrics(self.components)
        self.area_metrics = AreaMetrics(self.components)
    
    def set_weights(self, weights):
        """
        Set custom weights for the crossbar array.
        
        Parameters:
            weights: numpy array of shape (array_rows, array_columns) containing weight values
        """
        rows = self.config.getint('Crossbar', 'array_rows')
        cols = self.config.getint('Crossbar', 'array_columns')
        if weights.shape != (rows, cols):
            raise ValueError(f"Weights must be a {rows}x{cols} array")
        
        max_weight = (1 << self.config.getint('Crossbar', 'weight_bits')) - 1
        if np.any(weights > max_weight) or np.any(weights < 0):
            raise ValueError(f"Weights must be between 0 and {max_weight}")
        
        self.crossbar.weights = weights

    def process_inputs(self, digital_inputs, selected_rows):
        """
        Process multiple digital inputs through the entire PWM system.
    
        Parameters:
            digital_inputs: List of digital input values
            selected_rows: List of rows to apply inputs to
        
        Returns:
            outputs: List of TDC outputs (exactly 16 values)
            metrics: Dictionary of energy and delay metrics
        """
        outputs = []
        max_operation_time = 0
    
        if len(digital_inputs) != len(selected_rows):
            raise ValueError("Number of inputs must match number of selected rows")
        #decode the digital inputs
        decoder_outputs = [self.decoder.decode(input_val) for input_val in digital_inputs]
    
        # Convert all digital inputs to analog
        analog_outputs = [self.dac.convert(input_val) for input_val in digital_inputs]
    
        # Get all column outputs for all selected rows at once
        subtracted_values = []
        for i in range(0, self.crossbar.array_columns, 2):
            # Sum odd-numbered column
            odd_sum = self.crossbar.sum_odd_column(digital_inputs, selected_rows, i)
            
            # Sum even-numbered column 
            even_sum = self.crossbar.sum_even_column(digital_inputs, selected_rows, i + 1)
            
            # Use subtractor to get difference
            subtractor_idx = i // 2
            subtracted_value = self.subtractors[subtractor_idx].subtract(odd_sum, even_sum)
           # print(f"Subtractor {subtractor_idx}: {odd_sum} - {even_sum} = {subtracted_value}")
            subtracted_values.append(subtracted_value)
    
        # Initialize ramp generator
        self.ramp_generator.enable()
        start_time = 0
        stop_time = 0
        current_time = 0
    
        # Process each subtracted value to get final outputs
        for subtracted_value in subtracted_values:
            while True:
                ramp_value = self.ramp_generator.get_value(current_time)
                if self.comparator.compare(ramp_value, subtracted_value):
                    stop_time = current_time
                    print(f"crossing_ponit: {stop_time}")
                    break
            
                current_time += self.config.getfloat('System', 'time_step')
                if current_time > self.tdc.max_time:
                    stop_time = self.tdc.max_time
                    
                    break
        
            max_operation_time = max(max_operation_time, current_time)
        
            if stop_time <= self.tdc.max_time:
               output = self.tdc.measure_time(start_time, stop_time)
               print(f"Start: {start_time}, Stop: {stop_time}, Output: {output}")
               outputs.append(output)
            else:
                outputs.append(2**self.tdc.num_tdc - 1)
    
        metrics = self.calculate_metrics(max_operation_time)
        return outputs, metrics
        
    def calculate_metrics(self, operation_time):
        """Calculate energy and delay metrics for the system using separate modules"""
        return {
            'energy': self.energy_metrics.calculate_energy(operation_time),
            'delay': self.delay_metrics.calculate_delay(),
            'power': self.power_metrics.calculate_power(),
            'area': self.area_metrics.calculate_area(),
            'operation_time': operation_time
        }