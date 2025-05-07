import numpy as np

class Crossbar:
    def __init__(self, Ron, Roff, on_off_ratio, capacitance, Vdd, pulse_period, array_rows, 
                 vin, array_columns, A, weight_bits):
        self.Ron = Ron  # 5K ohm
        self.Roff = Roff  # 50K ohm
        self.on_off_ratio = on_off_ratio
        self.capacitance = capacitance
        self.Vdd = Vdd
        self.pulse_period = pulse_period
        self.array_rows = array_rows
        self.array_columns = array_columns
        self.weight_bits = weight_bits
        self.A = A
        self.vin = vin
        
        # Initialize weights as zeros instead of random values
        self.weights = np.zeros((array_rows, array_columns))
       # print(f"Initialized weights shape: {self.weights.shape}")

    def compute_output(self, input_vector, row):
        """
        Computes the output for all 32 columns in the selected row.
        Combines pairs of columns to produce 16 outputs for the subtractors.
        
        Parameters:
            input_vector: List of input values (single value for the selected row)
            row: Selected row for input application
        
        Returns:
            List of 32 column outputs (which will be processed by 16 subtractors)
        """
        if len(input_vector) != 1:
            raise ValueError("Input vector must contain a single value for the selected row.")
        
        column_outputs = []
        
        # Process all 32 columns
        for col in range(self.array_columns):
            if col % 2 == 0:  # even-numbered columns (0, 2, 4...)
                weighted_sum = input_vector[0] * self.weights[row][col]
                column_output = ((self.vin * self.pulse_period) / 
                               (self.Ron * self.capacitance * self.A)) * (weighted_sum / self.on_off_ratio)
                print(f"Column {col} output: {column_output}")
            else:  # odd-numbered columns (1, 3, 5...)
                column_output = 0
                print(f"Column {col} output: {column_output}")
            column_outputs.append(column_output)

        return column_outputs
    def sum_odd_column(self, input_vector, selected_rows, column_idx):
        """
        Sum the outputs for a specific odd-numbered column across selected rows.
        
        Parameters:
            input_vector: List of input values for selected rows
            selected_rows: List of row indices
            column_idx: The odd-numbered column to sum (0, 2, 4, etc.)
            
        Returns:
            Sum of outputs for the specified odd-numbered column
        """
        if len(input_vector) != len(selected_rows):
            raise ValueError("Number of inputs must match number of selected rows")
            
        column_sum = 0
        for i, row in enumerate(selected_rows):
            weighted_sum = input_vector[i] * self.weights[row][column_idx]
            output = ((self.vin * self.pulse_period) /
                     (self.Ron * self.capacitance * self.A)) * (weighted_sum / self.on_off_ratio)
            column_sum += output
            #print(f"Row {row}, Column {column_idx} contribution: {output}")
            
       # print(f"Total sum for Column {column_idx}: {column_sum}")
        return column_sum
    
    def sum_even_column(self, input_vector, selected_rows, column_idx):
        """
        Sum the outputs for a specific even-numbered column across selected rows.
        Always returns 0 as per the original implementation.
        
        Parameters:
            input_vector: List of input values for selected rows
            selected_rows: List of row indices
            column_idx: The even-numbered column (1, 3, 5, etc.)
            
        Returns:
            0 (as even-numbered columns are kept at 0)
        """
        #print(f"Column {column_idx} (even) sum: 0")
        return 0
    

    def get_energy(self, input_vector):
        return 0.5 * self.capacitance * len(input_vector) * self.array_columns * (self.Vdd ** 2)*self.array_rows
    def get_delay(self):
        return self.Ron * self.capacitance
    def get_power(self):
        return 0.5
    def get_area(self):
        return 0.5