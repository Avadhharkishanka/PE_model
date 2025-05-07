from pathlib import Path
from pwm_system import PWMSystem
from PE_quantization import QuantizedPWMSystem
import numpy as np

if __name__ == "__main__":
    config_path = Path("config.ini")
    print(f"Absolute config path: {config_path.absolute()}")  # Add after line 8
    system = PWMSystem(config_path)
    #system = QuantizedPWMSystem(config_path) 
    
    # Get configuration limits
    num_rows = system.config.getint('Crossbar', 'array_rows')
    num_columns = system.config.getint('Crossbar', 'array_columns')
    weight_bits = system.config.getint('Crossbar', 'cell_weight_bits')
    max_weight = (1 << weight_bits) - 1
    max_input_value = (1 << system.num_bits) - 1

    # HARDCODE WEIGHTS HERE
    #weights = np.zeros((num_rows, num_columns))
    
    # Create the complete matrix at once
    weights = np.array([
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3],
    [2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2, 2, 6, 3, 7, 1, 5, 4, 2],
    [5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5, 5, 2, 7, 1, 4, 6, 3, 5],
    [4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4, 4, 7, 1, 5, 2, 3, 6, 4],
    [1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2, 1, 4, 2, 6, 3, 7, 5, 2],
    [3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3, 3, 1, 5, 2, 6, 4, 7, 3]
])

    
    # Validate weights
    if np.any(weights > max_weight):
        raise ValueError(f"Weights must not exceed {max_weight} ({weight_bits}-bits)")
    
    # Set the weights in the system
    system.set_weights(weights)

    # Specify rows to process and their inputs
    selected_rows = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]  # Add or remove rows as needed
    digital_inputs = [1,2,3,4,5,6,7,7,6,5,4,3,2,1,0,1,2,3,4,5,6]  # Must match length of selected_rows
    
    # Validate inputs and rows
    if len(digital_inputs) != len(selected_rows):
        raise ValueError("Number of inputs must match number of selected rows")
    
    for row in selected_rows:
        if row < 0 or row >= num_rows:
            raise ValueError(f"Row must be between 0 and {num_rows-1}")
    
    for input_value in digital_inputs:
        if input_value < 0 or input_value > max_input_value:
            raise ValueError(f"Input values must be between 0 and {max_input_value}")
            

    # Process inputs (this should return exactly 16 values)
    outputs, metrics = system.process_inputs(digital_inputs, selected_rows)
    

    # Print results
    print("\nConfiguration:")
    print(f"Array Dimensions: {num_rows}x{num_columns}")
    print(f"Weight Bits: {weight_bits} (max: {max_weight})")
    print(f"DAC Bits: {system.num_bits} (max: {max_input_value})")
    
    print("\nInputs:")
    for row, input_val in zip(selected_rows, digital_inputs):
        print(f"Row {row}: {input_val}")
    
    print("\nResults:")
    print(f"Digital outputs : {outputs}")
    print(f"Metrics: {metrics}")