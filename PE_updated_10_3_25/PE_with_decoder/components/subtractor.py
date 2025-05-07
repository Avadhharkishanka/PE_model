class Subtractor:
    def __init__(self):
        self.last_operation = None
        
    def subtract(self, col1_output, col2_output):
        """
        Subtracts the values of two columns.
        """
        self.last_operation = (col1_output, col2_output)
        return col1_output - col2_output
        
    def get_energy(self):
        """
        Returns the energy consumption of the subtractor.
        """
        return 0.3e-12 if self.last_operation else 0
        
    def get_delay(self):
        """
        Returns the delay of the subtractor.
        """
        return 0.5e-9  # Fixed delay in ns
    def get_power(self):
        return 0.1
    def get_area(self):
        return 0.1