class RampGenerator:
    def __init__(self, slope, time_step):
        self.slope = slope  # V/ns
        self.time_step = time_step
        self.current_value = 0
        self.enabled = False
        
    def enable(self):
        self.enabled = True
        self.current_value = 0
        
    def get_value(self, time_step):
        if not self.enabled:
            return 0
            
        # Convert time to nanoseconds since slope is in V/ns
        #time_ns = time * 1e9
        self.current_value = self.slope * time_step
        return self.current_value
        
    def get_energy(self, time_step):
        if not self.enabled:
            return 0
        return 0.5 * self.slope * time_step * self.current_value
        
    def get_delay(self):
        return self.time_step
    def get_power(self):
        return 0.2
    def get_area(self):
        return 0.3e-12