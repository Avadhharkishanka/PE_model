class Comparator:
    def __init__(self):
        self.last_comparison = None  # intializing the atttribute to none 
        
    def compare(self, ramp_value, reference):
        self.last_comparison = (ramp_value, reference)# stores the tuple onto the last_comparsion attribute
        return ramp_value >= reference  # returns the comparison result
        
    def get_energy(self):
        return 0.1 if self.last_comparison else 0
        
    def get_delay(self):
        return 0.02  # Fixed delay in ns
    def get_power(self):
        return 0.1
    def get_area(self):
        return 0.1