class AreaMetrics:
    def __init__(self, system_components):
        self.components = system_components
        
    def calculate_area(self):
        """Calculate total delay for the system"""
        # For subtractors, take the maximum delay since they operate in parallel
        subtractors_delay = max(subtractor.get_area() for subtractor in self.components['subtractors'])
        
        return sum([
            self.components['dac'].get_area(),
            self.components['crossbar'].get_area(),
            subtractors_delay,  # Use the maximum delay from subtractors
            self.components['ramp_generator'].get_area(),
            self.components['comparator'].get_area(),
            self.components['tdc'].get_area()
        ])