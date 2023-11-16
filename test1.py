import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox, filedialog
from tkinter import ttk
import json

class Shape:
    def __init__(self, shape_type, x, y, width, height, color):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = None  # Identifiant de la forme sur le canevas

    def calculate_perimeter(self):
        if self.shape_type in ["rectangle", "square"]:
            return 2 * (self.width + self.height)
        elif self.shape_type == "ellipse":
            # Approximation du périmètre d'une ellipse (formule simplifiée)
            return 3.1416 * (self.width + self.height)
        elif self.shape_type == "circle":
            return 3.1416 * 2 * self.width
        elif self.shape_type == "diamond":
            # Approximation du périmètre d'un losange (formule simplifiée)
            return 4 * ((self.width / 2) + (self.height / 2))
        elif self.shape_type == "hexagon":
            # Approximation du périmètre d'un hexagone régulier (formule simplifiée)
            return 6 * self.width

    def calculate_area(self):
        if self.shape_type in ["rectangle", "square"]:
            return self.width * self.height
        elif self.shape_type == "ellipse":
            # Approximation de la surface d'une ellipse (formule simplifiée)
            return 3.1416 * (self.width / 2) * (self.height / 2)
        elif self.shape_type == "circle":
            return 3.1416 * (self.width / 2) ** 2
        elif self.shape_type == "diamond":
            # Approximation de la surface d'un losange (formule simplifiée)
            return (self.width * self.height) / 2
        elif self.shape_type == "hexagon":
            # Approximation de la surface d'un hexagone régulier (formule simplifiée)
            return (3 * 3 ** 0.5 * self.width ** 2) / 2

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.shapes = []
        self.selected_shape = None

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=tk.YES, fill=tk.BOTH)

        # Onglet Draw
        self.draw_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.draw_tab, text="Draw")

        self.canvas = tk.Canvas(self.draw_tab, width=800, height=600, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Load", command=self.load)

        draw_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Draw", menu=draw_menu)
        draw_menu.add_command(label="Rectangle", command=lambda: self.draw_shape("rectangle"))
        draw_menu.add_command(label="Ellipse", command=lambda: self.draw_shape("ellipse"))
        draw_menu.add_command(label="Circle", command=lambda: self.draw_shape("circle"))
        draw_menu.add_command(label="Square", command=lambda: self.draw_shape("square"))
        draw_menu.add_command(label="Diamond", command=lambda: self.draw_shape("diamond"))
        draw_menu.add_command(label="Hexagon", command=lambda: self.draw_shape("hexagon"))

        self.canvas.bind("<Button-1>", self.select_shape)
        self.root.bind("<Delete>", self.delete_selected_shape)
        self.canvas.bind("<Double-Button-1>", self.edit_selected_shape)

        # Onglet Edit
        self.edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_tab, text="Edit")

        self.edit_frame = tk.Frame(self.edit_tab)
        self.edit_frame.pack(padx=20, pady=20)

        self.edit_shape_label = tk.Label(self.edit_frame, text="Edit Shape:")
        self.edit_shape_label.grid(row=0, column=0, padx=10, pady=10)

        self.edit_shape_var = tk.StringVar()
        self.edit_shape_dropdown = ttk.Combobox(self.edit_frame, textvariable=self.edit_shape_var, state="readonly")
        self.edit_shape_dropdown["values"] = ["Rectangle", "Ellipse", "Circle", "Square", "Diamond", "Hexagon"]
        self.edit_shape_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.edit_btn = tk.Button(self.edit_frame, text="Edit", command=self.create_new_shape)
        self.edit_btn.grid(row=0, column=2, padx=10, pady=10)

        self.root.bind("<Double-Button-1>", self.edit_selected_shape)

        # Variable pour le déplacement de la forme
        self.drag_data = {"item": None, "x": 0, "y": 0}
        # Ajout d'un événement de déplacement de la souris
        self.canvas.bind("<B1-Motion>", self.move_shape)

    def draw_shape(self, shape_type):
        x, y = 100, 100  # Default position
        width, height = 50, 50  # Default dimensions
        color = "black"  # Default color

        if shape_type != "circle":
            width = simpledialog.askinteger("Width", "Enter width:")
            if width is None:  # If the user canceled the dialog box
                return

            height = simpledialog.askinteger("Height", "Enter height:")
            if height is None:  # If the user canceled the dialog box
                return

        color = colorchooser.askcolor()[1]

        shape = Shape(shape_type, x, y, width, height, color)
        shape.id = self.draw_on_canvas(shape)
        self.shapes.append(shape)

    def draw_on_canvas(self, shape):
        if shape.shape_type == "rectangle":
            return self.canvas.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color)
        elif shape.shape_type == "ellipse":
            return self.canvas.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color)
        elif shape.shape_type == "circle":
            return self.canvas.create_oval(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color)
        elif shape.shape_type == "square":
            return self.canvas.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color)
        elif shape.shape_type == "diamond":
            return self.canvas.create_polygon(shape.x, shape.y + shape.height / 2, shape.x + shape.width / 2, shape.y,
                                              shape.x + shape.width, shape.y + shape.height / 2, shape.x + shape.width / 2,
                                              shape.y + shape.height, fill=shape.color)
        elif shape.shape_type == "hexagon":
            return self.canvas.create_polygon(shape.x, shape.y + shape.height / 2, shape.x + shape.width / 4, shape.y,
                                              shape.x + 3 * shape.width / 4, shape.y, shape.x + shape.width,
                                              shape.y + shape.height / 2, shape.x + 3 * shape.width / 4,
                                              shape.y + shape.height, shape.x + shape.width / 4, shape.y + shape.height,
                                              fill=shape.color)

    def select_shape(self, event):
        x, y = event.x, event.y
        selected_id = self.canvas.find_closest(x, y)[0]
        
        for shape in self.shapes:
            if shape.id == selected_id:
                self.selected_shape = shape
                self.show_shape_properties(shape)
                # Add information for the move
                self.drag_data["item"] = shape.id
                self.drag_data["x"], self.drag_data["y"] = x, y
                # Reset Motion Variable
                self.mouse_moving = False
                # Link Mouse Movement Event
                self.canvas.tag_bind(shape.id, "<B1-Motion>", self.start_move_shape)
                break

    def start_move_shape(self, event):
        self.mouse_moving = True
        self.move_shape(event)

    def delete_selected_shape(self, event):
        if self.selected_shape:
            self.canvas.delete(self.selected_shape.id)
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None

    def edit_selected_shape(self, event=None):
        if self.selected_shape:
            # Retrieve the properties of the selected shape
            shape_type = self.selected_shape.shape_type
            x, y = self.selected_shape.x, self.selected_shape.y
            width, height = self.selected_shape.width, self.selected_shape.height
            color = self.selected_shape.color

            # Delete the selected shape from the canvas
            self.canvas.delete(self.selected_shape.id)

            # Call the draw method to create a new shape with the retrieved properties
            self.draw_shape(shape_type, x, y, width, height, color)

            # Remove the selected shape from the list of shapes
            self.shapes.remove(self.selected_shape)

            # Reset Selected Shape
            self.selected_shape = None

    def edit_selected_shape_from_dropdown(self):
        shape_type = self.edit_shape_var.get()
        if shape_type and self.selected_shape:
            # Prompt the user to change values
            new_width = simpledialog.askinteger(f"Edit {shape_type} Width", f"Enter new width:", initialvalue=self.selected_shape.width)
            new_height = simpledialog.askinteger(f"Edit {shape_type} Height", f"Enter new height:", initialvalue=self.selected_shape.height)
            new_color = colorchooser.askcolor()[1]

            # Update Shape Properties
            self.selected_shape.width = new_width
            self.selected_shape.height = new_height
            self.selected_shape.color = new_color

            # Update the shape on the canvas
            self.canvas.delete(self.selected_shape.id)
            self.selected_shape.id = self.draw_on_canvas(self.selected_shape)

            # View Updated Properties
            self.show_shape_properties(self.selected_shape)

    def create_new_shape(self):
        if self.selected_shape:
            shape_type = self.edit_shape_var.get()
            x, y = self.selected_shape.x, self.selected_shape.y  # Use the position of the selected shape as the default position

            # Prompt the user to specify new dimensions
            new_width = simpledialog.askinteger(f"Edit {shape_type} Width", f"Enter new width:",
                                                initialvalue=self.selected_shape.width)
            new_height = simpledialog.askinteger(f"Edit {shape_type} Height", f"Enter new height:",
                                                initialvalue=self.selected_shape.height)

            new_color = colorchooser.askcolor(initialcolor=self.selected_shape.color)[1]

            # Update the properties of the existing shape
            self.selected_shape.width = new_width
            self.selected_shape.height = new_height
            self.selected_shape.color = new_color

            # Update the shape on the canvas
            self.canvas.delete(self.selected_shape.id)
            self.selected_shape.id = self.draw_on_canvas(self.selected_shape)

            # View Updated Properties
            self.show_shape_properties(self.selected_shape)
        else:
            messagebox.showinfo("Error", "No shape selected for editing.")

    def move_shape(self, event):
        if self.mouse_moving and self.drag_data["item"]:
            # Move the shape according to the movement of the mouse
            x, y = event.x, event.y
            dx, dy = x - self.drag_data["x"], y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], dx, dy)
            # Update the shape coordinates
            self.selected_shape.x += dx
            self.selected_shape.y += dy
            self.drag_data["x"], self.drag_data["y"] = x, y

    def create_new_shape_during_edit(self):
        shape_type = self.edit_shape_var.get()

        if shape_type:
            x, y = self.selected_shape.x, self.selected_shape.y  # Use the position of the selected shape as the default position

            # Prompt the user to specify new dimensions
            new_width = simpledialog.askinteger(f"Edit {shape_type} Width", f"Enter new width:",
                                                initialvalue=self.selected_shape.width)
            new_height = simpledialog.askinteger(f"Edit {shape_type} Height", f"Enter new height:",
                                                initialvalue=self.selected_shape.height)

            new_color = colorchooser.askcolor(initialcolor=self.selected_shape.color)[1]

            # Create a new shape with the new properties
            new_shape = Shape(shape_type, x, y, new_width, new_height, new_color)
            new_shape.id = self.draw_on_canvas(new_shape)

            # Replace the selected shape with the new shape
            self.shapes[self.shapes.index(self.selected_shape)] = new_shape

            # Delete the selected shape from the canvas
            self.canvas.delete(self.selected_shape.id)

            # View the properties of the new shape
            self.show_shape_properties(new_shape)

            # Enable Move for New Shape
            self.activate_shape_drag(new_shape)

    def activate_shape_drag(self, shape):
        # Enable Move for Specified Shape
        shape.id = self.canvas.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color)
        self.drag_data["item"] = shape.id
        self.drag_data["x"], self.drag_data["y"] = shape.x, shape.y

    def show_shape_properties(self, shape):
        if shape and isinstance(shape, Shape):  # Check if shape is not None and is an instance of the Shape class
            properties = f"Type: {shape.shape_type}\nWidth: {shape.width}\nHeight: {shape.height}\nPerimeter: {shape.calculate_perimeter():.2f}\nArea: {shape.calculate_area():.2f}"
            messagebox.showinfo("Shape Properties", properties)
        else:
            # Handle the case where shape is None or is not an instance of Shape
            messagebox.showinfo("Error", "Invalid shape or no shape to show properties for.")

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".taf", filetypes=[("Tkinter App Files", "*.taf")])
        if filename:
            data = {"shapes": []}
            for shape in self.shapes:
                data["shapes"].append({
                    "type": shape.shape_type,
                    "x": shape.x,
                    "y": shape.y,
                    "width": shape.width,
                    "height": shape.height,
                    "color": shape.color
                })
            
            with open(filename, "w") as file:
                json.dump(data, file)
                messagebox.showinfo("Save", "File saved successfully.")

    def load(self):
        filename = filedialog.askopenfilename(defaultextension=".taf", filetypes=[("Tkinter App Files", "*.taf")])
        if filename:
            with open(filename, "r") as file:
                data = json.load(file)
                loaded_shapes = data.get("shapes", [])
                
                for shape_data in loaded_shapes:
                    shape_type = shape_data.get("type", "")
                    x = shape_data.get("x", 0)
                    y = shape_data.get("y", 0)
                    width = shape_data.get("width", 50)
                    height = shape_data.get("height", 50)
                    color = shape_data.get("color", "black")
                    
                    shape = Shape(shape_type, x, y, width, height, color)
                    shape.id = self.draw_on_canvas(shape)
                    self.shapes.append(shape)

                messagebox.showinfo("Load", "File loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
