import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.crop_rect = None
        self.rect_id = None
        self.image_path = None
        self.img = None
        self.tk_img = None
        self.aspect_ratio = 1.0  # Set aspect ratio (width/height)
        self.rect_width = 200
        self.rect_height = int(self.rect_width / self.aspect_ratio)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<MouseWheel>", self.on_mouse_scroll)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.img = Image.open(file_path)
            self.display_image()

    def display_image(self):
        self.canvas.delete("all")
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.create_fixed_aspect_crop_rect()

    def create_fixed_aspect_crop_rect(self):
        self.canvas.delete(self.rect_id)
        self.crop_rect = [50, 50, 50 + self.rect_width, 50 + self.rect_height]
        self.rect_id = self.canvas.create_rectangle(*self.crop_rect, outline="red")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_x1 = self.crop_rect[0]
        self.rect_y1 = self.crop_rect[1]

    def on_mouse_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.crop_rect = [self.rect_x1 + dx, self.rect_y1 + dy, self.rect_x1 + dx + self.rect_width, self.rect_y1 + dy + self.rect_height]
        self.canvas.coords(self.rect_id, *self.crop_rect)

    def on_button_release(self, event):
        self.crop_rect = [self.crop_rect[0], self.crop_rect[1], self.crop_rect[0] + self.rect_width, self.crop_rect[1] + self.rect_height]

    def on_mouse_scroll(self, event):
        scale = 1.1 if event.delta > 0 else 0.9
        new_width = self.rect_width * scale
        new_height = new_width / self.aspect_ratio
        self.update_guideline(new_width, new_height)

    def on_canvas_resize(self, event):
        if self.img:
            self.display_image()

    def save_image(self):
        if self.crop_rect and self.img is not None:
            x1, y1, x2, y2 = self.crop_rect
            x1, y1 = max(x1, 0), max(y1, 0)
            x2, y2 = min(x2, self.img.width), min(y2, self.img.height)
            if x2 > x1 and y2 > y1:
                cropped_img = self.img.crop((x1, y1, x2, y2))
                save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
                if save_path:
                    cropped_img.save(save_path)
                    messagebox.showinfo("Image Cropper", "Image saved successfully!")

    def update_guideline(self, new_width, new_height):
        self.rect_width = new_width
        self.rect_height = new_height
        self.create_fixed_aspect_crop_rect()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.geometry("800x600")
    root.mainloop()
