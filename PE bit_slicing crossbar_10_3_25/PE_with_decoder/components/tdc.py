class TDC:
    def __init__(self, num_tdc, time_precision):
        self.num_tdc = num_tdc
        self.time_precision = time_precision
        self.max_time =  time_precision *(2**num_tdc - 1)
        
    def measure_time(self, start_time, stop_time):
        time_diff = stop_time - start_time
        digital_value = int(time_diff / self.time_precision) 
        return min(digital_value, 2**self.num_tdc - 1)
        
    def get_energy(self, measurement_time):
        return 0.2 * measurement_time
        
    def get_delay(self):
        return self.time_precision
    def get_power(self):
        return 0.5* self.time_precision
    def get_area(self): 
        return 0.1