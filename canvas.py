import tkinter as tk
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.canvas = tk.Canvas(root, bg="black", width=280, height=280)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.canvas.bind("<B1-Motion>", self.paint)

        self.save_button = tk.Button(root, text="Save", command=self.save_image)
        self.save_button.pack(side=tk.BOTTOM)

        self.image = Image.new("L", (280, 280), color="black")
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None

    def paint(self, event):
        x, y = event.x, event.y

        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="white", width=4)
            self.draw.line([self.last_x, self.last_y, x, y], fill="white", width=4)

        self.last_x, self.last_y = x, y

    def save_image(self):
        filename = "drawing.png"
        self.image = self.image.resize((28, 28), Image.LANCZOS)
        self.image.save(filename)
        print(f"Image saved as {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


















