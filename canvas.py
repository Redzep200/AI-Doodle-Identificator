import tkinter as tk

class Canvas():
    def __init__(self, root):
        # Sets the Tkinter main window instance as a pameter of the Canvas class
        self.root = root
        self.root.title("Drawing Canvas")

        # Adds a canvas to the main window instance and sets the canvas to fill the window
        self.canvas = tk.Canvas(root,bg="black")
        self.canvas.pack(fill=tk.BOTH,expand=True)

        self.pen_color="white"

        # Denotes that the user is not actively drawing and that there is no x,y cursor coordinates
        self.drawing = False
        self.last_x, self.last_y = None, None

        # List to store drawn lines
        self.lines = []

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
            line = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=2)
            self.lines.append(line)     # add line to line list
            self.last_x, self.last_y = x, y     # set last x and y to new x,y
    

    def stop_draw():
        self.drawing = False

    # Check if line array is empty if not remove the last line from array and delete from canvas
    def undo(self):
        if self.lines:
            last_line = self.lines.pop()    
            self.canvas.delete(last_line)

    def erase(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = Canvas(root)
    root.mainloop()









