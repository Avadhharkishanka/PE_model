class EnergyMetrics:
    def __init__(self, system_components):
        self.components = system_components
        
    def calculate_energy(self, operation_time):
        """Calculate total energy consumption for the system"""
        # Calculate subtractors energy separately since it's a list
        subtractors_energy = sum(subtractor.get_energy() for subtractor in self.components['subtractors'])
        
        return sum([
            self.components['dac'].get_energy(1),
            self.components['crossbar'].get_energy([1]),
            subtractors_energy,  # Add the total energy from all subtractors
            self.components['ramp_generator'].get_energy(operation_time),
            self.components['comparator'].get_energy(),
            self.components['tdc'].get_energy(operation_time)
        ])

