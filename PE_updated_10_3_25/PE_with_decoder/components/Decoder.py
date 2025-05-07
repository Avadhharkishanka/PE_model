class Decoder:
    def __init__(self,num_bits):
        self.num_bits = num_bits
    
    def decode(self, digital_input):
       # dec= digital_input
       # print(f"Decoded value: {dec}")
        return 2**digital_input
    
    def get_energy(self, digital_input):
        # Simple energy model based on number of transitions
        return 0.5 * digital_input
        
    def get_delay(self):
        # Simplified delay model
        return 1e-9 # delay calculation
    def get_power(self):
        return  0.1
    def get_area(self):
        return 0.1

