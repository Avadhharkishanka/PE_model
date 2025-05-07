import numpy as np

class DAC:
    def __init__(self, num_bits, pulse_period, Vdd=1.8):
        self.num_bits = num_bits # number of bits(8 bits)
        self.pulse_period = pulse_period # duration for one pulse
        self.Vdd = Vdd # supply voltage 1.8V
        
    def convert(self, digital_input):
        # dac = digital_input * self.pulse_period
         #print(dac)
         return digital_input * self.pulse_period #converts the digital value to pulse_period
    def get_energy(self, digital_input):
        # Simple energy model based on number of transitions
        return 0.5 * digital_input * self.Vdd * self.pulse_period # energy calculation
        
    def get_delay(self):
        # Simplified delay model
        return 1e-9 # delay calculation
    def get_power(self):
        return  0.1
    def get_area(self):
        return 0.1