import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        # Create a frame to hold the canvas and scrollbar
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(frame, bg="black", width=280, height=280)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_last_position)

        # Scrollbar and Text widget for displaying normalized vector
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.text_widget = tk.Text(frame, wrap=tk.NONE, yscrollcommand=self.scrollbar.set, height=10)
        self.text_widget.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.text_widget.yview)

        # Buttons for Save and Clear
        save_button = tk.Button(root, text="Save", command=self.save_image)
        save_button.pack(side=tk.BOTTOM)

        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.BOTTOM)

        self.image = Image.new("L", (280, 280), color="black")
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None


    def paint(self, event):
        x, y = event.x, event.y

        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="white", width=4)
            self.draw.line([self.last_x, self.last_y, x, y], fill="white", width=4)

        self.last_x, self.last_y = x, y

    def reset_last_position(self, event):
        self.last_x, self.last_y = None, None

    def save_image(self):
        filename = "drawing.png"
        self.image = self.image.resize((28, 28), Image.LANCZOS)
        self.image.save(filename)
        normalized_vector = self.normalize_image(self.image)
        self.text_widget.insert(tk.END, f"Normalized Vector:\n{normalized_vector}\n\n")
        print(f"Image saved as {filename}")

    def normalize_image(self, image):
        flat_array = np.array(image).flatten()
        normalized_vector = flat_array / 255.0
        return normalized_vector

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), color="black")
        self.draw = ImageDraw.Draw(self.image)
        self.last_x, self.last_y = None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()





















