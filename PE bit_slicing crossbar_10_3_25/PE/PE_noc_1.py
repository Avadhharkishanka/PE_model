import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import matplotlib.patches as patches

class ProcessingElement:
    def __init__(self):
        self.bit_width = None
        self.memory_array = None
        self.input_value = 0
        self.input_binary = None
        self.result_matrix = None
        self.column_sums = None
        self.column_differences = None
        self.fig = None
        self.axes = None
        self.processed = False
        self.setup_bit_width()

    def setup_bit_width(self):
        while True:
            try:
                bit_width = int(input("Enter desired bit width (1-10): "))
                if 1 <= bit_width <= 10:
                    self.bit_width = bit_width
                    # Create random memory array with values up to 2^bit_width - 1
                    max_value = 2**bit_width - 1
                    # Use appropriate numpy dtype based on bit_width
                    if bit_width <= 8:
                        dtype = np.uint8
                    else:
                        dtype = np.uint16
                    
                    # Initialize memory array with random unsigned integers
                    self.memory_array = np.random.randint(0, max_value + 1, (8, 8), dtype=dtype)
                    self.input_binary = '0' * bit_width
                    break
                else:
                    print("Bit width must be between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")

    def subtractor(self, col1, col2, p1=1, p2=1, p3=1, p4=1):
        """
        Performs subtraction between two column sums with additional parameters
        for future modifications.
        
        Args:
            col1: First column sum
            col2: Second column sum
            p1: Parameter 1 (default=1)
            p2: Parameter 2 (default=1)
            p3: Parameter 3 (default=1)
            p4: Parameter 4 (default=1)
            
        Returns:
            The difference between columns modified by parameters
        """
        difference = (col1 * p1 * p2) - (col2 * p3 * p4)
        return difference

    def setup_visualization(self):
        plt.close('all')
        self.fig = plt.figure(figsize=(15, 12))
        self.axes = {}
        self.axes['main'] = self.fig.add_axes([0.1, 0.3, 0.8, 0.6])
        self.axes['subtraction'] = self.fig.add_axes([0.1, 0.15, 0.8, 0.1])
        self.axes['subtraction'].axis('off')

        self.fig.text(0.2, 0.1, f'Binary Input ({self.bit_width}-bit):', fontsize=10)
        self.binary_input = TextBox(self.fig.add_axes([0.4, 0.09, 0.2, 0.05]), '')
        self.binary_input.on_submit(self.update_binary_input)

        self.process_btn = Button(self.fig.add_axes([0.35, 0.02, 0.3, 0.05]), 'Process')
        self.process_btn.on_clicked(self.process_operation)

        self.fig.suptitle(f'Processing Element with {self.bit_width}- bit quantization', y=0.95)
        self.update_visualization()

    def update_binary_input(self, text):
        if len(text) == self.bit_width and all(bit in '01' for bit in text):
            self.input_binary = text
            self.input_value = int(text, 2)
            self.processed = False
            self.update_visualization()
        else:
            print(f"Invalid binary input. Must be {self.bit_width} bits of 0s and 1s.")

    def process_operation(self, event):
        if not self.processed:
            max_value = 2**self.bit_width - 1
            result = self.memory_array * self.input_value
            # Ensure result stays within unsigned range for the given bit width
            self.result_matrix = np.clip(result, 0, max_value)
            self.column_sums = np.sum(self.result_matrix, axis=0, dtype=np.int32)
            self.column_differences = [(i, i+1, self.subtractor(
                self.column_sums[i], 
                self.column_sums[i+1]
            )) for i in range(0, len(self.column_sums)-1, 2)]
            self.processed = True
            self.update_visualization()

    def add_matrix_labels(self, ax, matrix, include_input=False, include_sums=False):
        rows, cols = matrix.shape
        max_value = 2**self.bit_width - 1
        
        if include_input:
            for i in range(rows):
                ax.text(-2, i, f'[{self.input_binary}={self.input_value}]', ha='center', va='center', 
                       color='black', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))
        
        for i in range(rows):
            for j in range(cols):
                value = matrix[i, j]
                ax.text(j, i, f'{value:3d}', ha='center', va='center', 
                       color='white' if value > (max_value//2) else 'black')
        
        if include_sums and self.column_sums is not None:
            for j in range(cols):
                ax.text(j, rows, f'[{self.column_sums[j]:04d}]', ha='center', va='center', 
                       color='black', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))
        
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(rows - 0.5, -0.5)

    def draw_subtraction_results(self, ax):
        ax.clear()
        ax.axis('off')
        for i, (col1, col2, diff) in enumerate(self.column_differences):
            x_pos = (col1 + col2) / 2
            ax.text(x_pos/8, 0.5, f'C{col1}-C{col2} = {diff:04d}', ha='center', va='center', 
                   bbox=dict(facecolor='lightgray', edgecolor='gray', alpha=0.8))

    def update_visualization(self):
        self.axes['main'].clear()
        matrix_to_show = self.result_matrix if self.processed else self.memory_array
        self.axes['main'].imshow(matrix_to_show, cmap='viridis')
        self.add_matrix_labels(self.axes['main'], matrix_to_show, include_input=True, include_sums=True)
        self.axes['main'].set_xlim(-0.5, 7.5)
        self.axes['main'].set_ylim(7.5, -0.5)
        title = 'Result (After Processing)' if self.processed else 'Initial Memory Array'
        self.axes['main'].set_title(title)
        if self.processed:
            self.draw_subtraction_results(self.axes['subtraction'])
            self.axes['subtraction'].set_visible(True)
        else:
            self.axes['subtraction'].set_visible(False)
        self.fig.canvas.draw_idle()

def main():
    pe = ProcessingElement()
    pe.setup_visualization()
    plt.show()

if __name__ == "__main__":
    main()