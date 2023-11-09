import os
import subprocess
import json

import tkinter as tk
from PIL import Image, ImageTk

class PhotoCompareApp:
    def __init__(self, root, photo_list):
        self.root = root
        self.photo_list = photo_list
        self.index = 0

        self.image_label1 = tk.Label(root)
        self.image_label2 = tk.Label(root)
        self.value_label = tk.Label(root)

        self.show_photos()

        next_button = tk.Button(root, text="Next", command=self.next_photo)
        next_button.pack()

    def show_photos(self):
        photo1_path, photo2_path, value = self.photo_list[self.index]

        image1 = Image.open(photo1_path)
        image2 = Image.open(photo2_path)

        # Resize images to fit in the window
        image1 = image1.resize((300, 300), Image.Resampling.LANCZOS)
        image2 = image2.resize((300, 300), Image.Resampling.LANCZOS)

        photo1 = ImageTk.PhotoImage(image1)
        photo2 = ImageTk.PhotoImage(image2)

        self.image_label1.config(image=photo1)
        self.image_label1.image = photo1
        self.image_label1.pack(side=tk.LEFT, padx=10)

        self.image_label2.config(image=photo2)
        self.image_label2.image = photo2
        self.image_label2.pack(side=tk.LEFT, padx=10)

        self.value_label.config(text=f"Value: {value}")
        self.value_label.pack()

    def next_photo(self):
        self.index += 1

        if self.index < len(self.photo_list):
            # Clear previous images and labels
            self.image_label1.pack_forget()
            self.image_label2.pack_forget()
            self.value_label.pack_forget()

            # Show the next set of photos
            self.show_photos()
        else:
            self.root.destroy()


def check_data_prepared():
    file_path = 'data_prepared'  # Replace with the actual file name you're checking for

    if not os.path.exists(file_path):
      venv_path = 'envfotocomp'
      venv_python = os.path.join(venv_path, 'bin', 'python') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'python.exe')
      subprocess.run([venv_python, 'prepare_images.py'])


def load_photo_list_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    method = 'histogram'
    json_file_path = "results\\images_"+method+'_results.json'

    check_data_prepared()

    root = tk.Tk()
    root.title("Photo Compare App")

    photo_list = load_photo_list_from_json(json_file_path)

    app = PhotoCompareApp(root, photo_list)

    root.mainloop()
