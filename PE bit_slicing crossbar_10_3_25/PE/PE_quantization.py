from pwm_system import PWMSystem
import numpy as np
from pathlib import Path
import math

class QuantizedPWMSystem(PWMSystem):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.chunk_size = self.config.getint('Quantization', 'chunk_size')
        self.weight_bits = self.config.getint('Quantization', 'weight_bits')
        self.input_bits = self.config.getint('Quantization', 'input_bits')
        self.cell_weight_bits = self.config.getint('Crossbar', 'cell_weight_bits')

    def set_weights(self, weights):
        """Map weights to crossbar, considering cell capacity"""
        # Calculate total bits needed for all weights
        total_weight_bits = len(weights) * self.weight_bits
        
        # Calculate maximum bits the crossbar can store
        # Each odd column can store cell_weight_bits
        max_crossbar_bits = (self.crossbar.array_columns // 2) * self.cell_weight_bits * self.crossbar.array_rows
        
        if total_weight_bits > max_crossbar_bits:
            raise ValueError(f"Total weight bits ({total_weight_bits}) exceeds crossbar capacity of {max_crossbar_bits} bits")

        padded_weights = np.zeros((self.crossbar.array_rows, self.crossbar.array_columns))
        
        # Calculate weights that can fit per row
        cells_per_weight = math.ceil(self.weight_bits / self.cell_weight_bits)
        weights_per_row = self.crossbar.array_columns // (2 * cells_per_weight)

        for i, weight in enumerate(weights):
            # Calculate row and position within row
            row = i // weights_per_row
            pos_in_row = i % weights_per_row
            
            # Calculate starting column for this weight
            col_offset = pos_in_row * (cells_per_weight * 2)
            
            # Split weight into chunks of cell_weight_bits size
            chunks = self.split_bits(weight, self.weight_bits, self.cell_weight_bits)
            
            # Place chunks in odd-numbered columns
            for j, chunk in enumerate(chunks):
                padded_weights[row, col_offset + j*2] = chunk

        super().set_weights(padded_weights)

    def process_inputs(self, digital_inputs, selected_rows):
        """Process 16-bit inputs in 4-bit chunks, LSB first"""
        input_chunks = []
        expanded_rows = []

        for input_val, row in zip(digital_inputs, selected_rows):
            # Split 16-bit input into 4-bit chunks (LSB first)
            chunks = self.split_bits(input_val, self.input_bits, self.chunk_size, msb_first=False)

            # Process each chunk on the same row
            for chunk in chunks:
                input_chunks.append(chunk)
                expanded_rows.append(row)

        return super().process_inputs(input_chunks, expanded_rows)

    @staticmethod
    def split_bits(value, total_bits, chunk_size, msb_first=True):
        """Split values into bit chunks with configurable order"""
        num_chunks = total_bits // chunk_size
        chunks = []
        for i in range(num_chunks):
            shift = i*chunk_size if msb_first else (num_chunks-1-i)*chunk_size
            chunk = (value >> shift) & ((1 << chunk_size)-1)
            chunks.append(chunk)
        return chunks

if __name__ == "__main__":
    system = QuantizedPWMSystem(Path("config.ini"))
    
    # Calculate how many weights can fit per row
    cells_per_weight = math.ceil(system.weight_bits / system.cell_weight_bits)
    weights_per_row = system.crossbar.array_columns // (2 * cells_per_weight)
    
    print(f"Each row can fit {weights_per_row} weights of {system.weight_bits} bits each")
    
    # Create weights for all 32 rows following a pattern similar to the example
    weight_matrix = []
    for row in range(32):
        row_weights = []
        for col in range(weights_per_row):
            # Generate weight following pattern: row in upper bits, position in lower bits
            # Similar to 0x1C11, 0x2D22, 0x3E33 pattern from example
            weight_value = ((row + 1) << 12) | ((col + 1) << 8) | ((row + 1) << 4) | (col + 1)
            row_weights.append(weight_value)
        weight_matrix.append(row_weights)
    
    # Convert weight matrix to list and validate
    weights = []
    active_rows = []
    
    print("\nProcessing Weight Matrix:")
    for row_idx, row_weights in enumerate(weight_matrix):
        if len(row_weights) > weights_per_row:
            print(f"Warning: Row {row_idx} has {len(row_weights)} weights, truncating to {weights_per_row}")
            row_weights = row_weights[:weights_per_row]
        
        for col_idx, weight in enumerate(row_weights):
            if weight > max_weight:
                raise ValueError(f"Weight at row {row_idx}, position {col_idx} (0x{weight:X}) exceeds maximum (0x{max_weight:X})")
            weights.append(weight)
        active_rows.append(row_idx)
    
    # Set the weights in the system
    system.set_weights(weights)
    
    # Define inputs for all 32 rows following the example pattern
    row_inputs = {}
    input_patterns = [
        0xABCD,  # Pattern 1 (like original example)
        0x1234,  # Pattern 2 (like original example)
        0x5678,  # Pattern 3 (like original example)
        0x9ABC,  # Pattern 4
        0xDEF0,  # Pattern 5
        0x2468,  # Pattern 6
        0x1357,  # Pattern 7
        0xFEDC   # Pattern 8
    ]
    
    for row in range(32):
        # Cycle through patterns and modify slightly for each row to make unique
        base_pattern = input_patterns[row % len(input_patterns)]
        row_inputs[row] = base_pattern + row
    
    # Create input lists for processing
    digital_inputs = []
    selected_rows = []
    
    for row in range(32):
        digital_inputs.append(row_inputs[row])
        selected_rows.append(row)
    
    # Process all inputs
    outputs, metrics = system.process_inputs(digital_inputs, selected_rows)
    
    print("\nConfiguration:")
    print(f"Weight bits: {system.weight_bits}")
    print(f"Cell bits: {system.cell_weight_bits}")
    print(f"Input bits: {system.input_bits}")
    print(f"Chunk size: {system.chunk_size}")
    
    print("\nWeights (showing first 5 rows):")
    for row in range(min(5, 32)):
        print(f"Row {row}: ", end="")
        row_weights = weight_matrix[row]
        for i, w in enumerate(row_weights):
            print(f"W{i}=0x{w:04X}", end="  ")
        print()
    
    print("\nInputs (showing first 5 rows):")
    for row in range(min(5, 32)):
        print(f"Row {row}: Input=0x{row_inputs[row]:04X}")
    
    print("\nResults:")
    print(f"Number of outputs: {len(outputs)}")
    print("First 5 outputs:")
    for i in range(min(5, len(outputs))):
        print(f"Row {i}: {outputs[i]}")
    
    print("\nMetrics Summary:")
    print(f"Energy: {metrics.get('energy', 'N/A')} J")
    print(f"Delay: {metrics.get('delay', 'N/A')} s")
    print(f"Power: {metrics.get('power', 'N/A')} W")
    print(f"Area: {metrics.get('area', 'N/A')} mm²")