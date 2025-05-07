class PowerMetrics:
    def __init__(self, system_components):
        self.components = system_components
        
    def calculate_power(self):
        """Calculate total delay for the system"""
        # For subtractors, take the maximum delay since they operate in parallel
        subtractors_power = max(subtractor.get_power() for subtractor in self.components['subtractors'])
        
        return sum([
            self.components['dac'].get_power(),
            self.components['crossbar'].get_power(),
            subtractors_power,  # Use the maximum delay from subtractors
            self.components['ramp_generator'].get_power(),
            self.components['comparator'].get_power(),
            self.components['tdc'].get_power()
        ])