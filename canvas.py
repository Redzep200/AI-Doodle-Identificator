import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import torch
import data.neural_network
import data.data_normalization

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Doodle Identificator")

        # Create a frame to hold the canvas and scrollbar
        frame = tk.Frame(root)
        frame.pack(fill=tk.NONE, expand=False)

        # Canvas
        self.canvas = tk.Canvas(frame, bg="black", width=280, height=280)
        self.canvas.pack(side=tk.LEFT, fill=tk.NONE, expand=False)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_last_position)

        # Scrollbar and Text widget for displaying normalized vector
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.text_widget = tk.Text(frame, yscrollcommand=self.scrollbar.set, height=10)
        self.text_widget.insert(tk.END, f"\n Draw one of these items\n  1. An ANT\n  2. A COMPUTER\n  3.  A COOKIE\n  4. HEADPHONES\n  5. LIGHTNING\n")
        self.text_widget.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.text_widget.yview)

        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)  # Change this line
        
        guess_button = tk.Button(root, text="Guess", command=self.evaluate_image)
        guess_button.pack(side=tk.LEFT)

        self.image = Image.new("L", (280, 280), color="black")
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model('data/doodle_identificator.pth')
        
        
        
    def load_model(self, model_path):
        model = data.neural_network.CNN().to(self.device)
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model


    def paint(self, event):
        x, y = event.x, event.y

        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="white", width=7)
            self.draw.line([self.last_x, self.last_y, x, y], fill="white", width=7)

        self.last_x, self.last_y = x, y

    def reset_last_position(self, event):
        self.last_x, self.last_y = None, None

    def save_image(self):


        
        filename = "drawing.png"
        
        # Resize the image to 28x28
        resized_image = self.image.resize((28, 28), Image.LANCZOS)

        # Find bounding box of non-zero pixels in the resized image
        bbox = resized_image.getbbox()

        # Crop the image to the bounding box
        cropped_image = resized_image.crop(bbox)

        # Ensure the cropped image is 28x28
        final_image = ImageOps.fit(cropped_image, (28, 28), method=0, bleed=0.0, centering=(0.5, 0.5))

        # Save the final image
        final_image.save(filename)

        normalized_vector = self.normalize_image(final_image)
        # self.text_widget.insert(tk.END, f"Normalized Vector:\n{normalized_vector}\n\n")
        print(f"Image saved as {filename}")
        return normalized_vector



        # filename = "drawing.png"
        # self.image = self.image.resize((28, 28), Image.LANCZOS)
        # self.image.save(filename)
        # normalized_vector = self.normalize_image(self.image)
        # self.text_widget.insert(tk.END, f"Normalized Vector:\n{normalized_vector}\n\n")
        # print(f"Image saved as {filename}")
        # return normalized_vector

    def normalize_image(self, image):
        normalized = np.array(image).flatten()
        normalized = normalized.astype('float32')
        normalized /= 255.0
        return normalized
    

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), color="black")
        self.draw = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None
        self.text_widget.delete(1.0, tk.END)
        

    def evaluate_image(self):
        # Assuming self.text_widget is your Text widget

        # Delete all text in the Text widget
        self.text_widget.delete(1.0, tk.END)

        normalized_vector = self.save_image()
        #self.image = self.image.resize((28, 28), Image.LANCZOS)
        #normalized_vector = self.normalize_image(self.image)
        # self.text_widget.insert(tk.END, f"Normalized Vector:\n{normalized_vector}")
        input_tensor = torch.tensor(normalized_vector, dtype=torch.float32).to(self.device)
        with torch.no_grad():
            output = self.model(input_tensor)
        

          # Flatten the output tensor if it has unnecessary dimensions
        output = output.flatten()
        
        predicted_class_normal = torch.argmax(output)

        probabilities_percentages = output*100
        round_percent = probabilities_percentages.round()
        self.text_widget.insert(tk.END, f"\n  I think you drew ... {data.data_normalization.GetLabel(predicted_class_normal.item())}\n")
        
        element_counter=0
        for element in round_percent:
            self.text_widget.insert(tk.END,  f"\n  {data.data_normalization.GetLabel(element_counter)} - {element.item()}%")
            element_counter+=1
        #predicted_class = output.argmax(dim = 1, keepdim = True)
        
        #print(f'Guess: {data.data_normalization.GetLabel(predicted_class.item())} - {predicted_class}')
        #Problem u dimenzijama (vjerovatno), izbaci 4 ili 3 ali je to dimenzija tensora (npr tensor(4) ili tensor(3))

    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('565x310')
    app = DrawingApp(root)
    root.mainloop()
