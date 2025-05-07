class DelayMetrics:
    def __init__(self, system_components):
        self.components = system_components
        
    def calculate_delay(self):
        """Calculate total delay for the system"""
        # For subtractors, take the maximum delay since they operate in parallel
        subtractors_delay = max(subtractor.get_delay() for subtractor in self.components['subtractors'])
        
        return sum([
            self.components['dac'].get_delay(),
            self.components['crossbar'].get_delay(),
            subtractors_delay,  # Use the maximum delay from subtractors
            self.components['ramp_generator'].get_delay(),
            self.components['comparator'].get_delay(),
            self.components['tdc'].get_delay()
        ])