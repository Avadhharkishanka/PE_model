def process_inputs(self, digital_inputs, selected_rows):
    outputs = [None] * 16  # Ensure exactly 16 outputs
    max_operation_time = 0

    if len(digital_inputs) != len(selected_rows):
        raise ValueError("Number of inputs must match number of selected rows")

    # Iterate over each selected row and its corresponding input
    for digital_input, row in zip(digital_inputs, selected_rows):
        # Convert digital input to analog
        analog_input = self.dac.convert(digital_input)
        
        # Compute outputs for all 32 columns in the selected row
        column_outputs = self.crossbar.compute_output([digital_input], row)
        
        # Process column outputs using 16 subtractors
        for i in range(16):  
            col1_output = column_outputs[2 * i]      # Odd-numbered column (non-zero)
            col2_output = column_outputs[2 * i + 1]  # Even-numbered column (always 0)
            subtracted_value = self.subtractors[i].subtract(col1_output, col2_output)
            
            # Initialize ramp generator
            self.ramp_generator.enable()
            start_time = 0
            stop_time = None
            current_time = 0
            
            # Find crossing point for this subtractor
            while True:
                ramp_value = self.ramp_generator.get_value(current_time)
                if self.comparator.compare(ramp_value, subtracted_value):
                    stop_time = current_time
                    break
                
                current_time += self.config.getfloat('System', 'time_step')
                if current_time > self.tdc.max_time:
                    stop_time = self.tdc.max_time
                    break
            
            max_operation_time = max(max_operation_time, current_time)
            
            # If stop_time is valid, measure it and store the result for this subtractor
            if stop_time <= self.tdc.max_time:
                outputs[i] = self.tdc.measure_time(start_time, stop_time)
            elif outputs[i] is None:  
                # If no measurement was made, assign max TDC value
                outputs[i] = 2**self.tdc.num_tdc - 1  

    metrics = self.calculate_metrics(max_operation_time)
    return outputs, metrics
