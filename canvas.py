import tkinter as tk

class Canvas():
    def __init__(self, root):
        # Sets the Tkinter main window instance as a pameter of the Canvas class
        self.root = root
        self.root.title("Drawing Canvas")

        # Disable window resizing
        self.root.resizable(width=False, height=False)

        # Set resolution of canvas
        self.canvas_width = 254
        self.canvas_height = 254

        # Set size of pixels
        self.pixelation_factor = 10

        # Adds a canvas to the main window instance and sets the canvas to fill the window
        self.canvas = tk.Canvas(root,bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH,expand=False)

        self.pen_color="white"

        # Denotes that the user is not actively drawing and that there is no x,y cursor coordinates
        self.drawing = False
        self.last_x, self.last_y = None, None

        # List to store drawn lines
        self.pixels = []

        # Button to undo the last drawn line
        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
        self.undo_button.pack(side = tk.LEFT)

        # Button to erase all drawn lines
        self.erase_button = tk.Button(root, text="Erase", command=self.erase)
        self.erase_button.pack(side=tk.LEFT)

        # Button to save the drawing
        self.save_button = tk.Button(root, text="Save")
        self.save_button.pack(side=tk.RIGHT)

        # Binding of left mouse button events to functions
        self.canvas.bind("<Button-1>",self.start_draw)
        self.canvas.bind("<B1-Motion>",self.draw)
        self.canvas.bind("<ButtonRelease-1>",self.stop_draw)

    # Set parameters to initate drawing
    def start_draw(self,event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    # Start drawing - creates line from last x and y to the current x,y 
    def draw(self,event):
        if self.drawing:
            x, y = event.x, event.y
            x = round(x/self.pixelation_factor)*self.pixelation_factor
            y = round(y/self.pixelation_factor)*self.pixelation_factor

            # Check to see if pixel is in bounds
            if 0 <= x < self.canvas_width and 0 <= y < self.canvas_height:
                pixel = self.canvas.create_rectangle(x, y, x+self.pixelation_factor, y+self.pixelation_factor, fill=self.pen_color, outline="")
                self.pixels.append(pixel)     # add pixel to pixel list
    

    def stop_draw(self):
        self.drawing = False

    # Check if line array is empty if not remove the last line from array and delete from canvas
    def undo(self):
        if self.pixels:
            last_pixel = self.pixels.pop()    
            self.canvas.delete(last_pixel)

    def erase(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = Canvas(root)
    root.mainloop()









