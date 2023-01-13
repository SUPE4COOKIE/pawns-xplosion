import tkinter as tk


def create_canvas_with_shapes():
    # Create a canvas widget
    canvas = tk.Canvas(root, width=200, height=100)
    # Draw a rectangle and circles on the canvas
    rect = canvas.create_rectangle(25, 25, 150, 75, fill="blue")
    circle1 = canvas.create_oval(35, 35, 65, 65, fill="red")
    circle2 = canvas.create_oval(85, 35, 115, 65, fill="red")
    circle3 = canvas.create_oval(135, 35, 165, 65, fill="red")
    # Return the canvas
    return canvas


# Create the main window
root = tk.Tk()

# Create a canvas widget and draw a red rectangle on it
main_canvas = tk.Canvas(root, width=400, height=200, background="red")
main_canvas.pack()

# Call the create_canvas_with_shapes function to get the canvas with the rectangle and circles
canvas_with_shapes = create_canvas_with_shapes()
# Use the create_window method to display the canvas on the main canvas
main_canvas.create_window(100, 50, window=canvas_with_shapes)

root.mainloop()
