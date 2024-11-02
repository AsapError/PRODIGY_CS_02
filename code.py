import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# Initialize the main window
window = tk.Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")

# Global variables
image_original = None
image_encrypted = None
key = None

# Function to open file dialog and load image
def open_img():
    global image_original
    filepath = filedialog.askopenfilename(title='Select an Image', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        image_original = cv2.imread(filepath)
        display_image(image_original, "Original Image")
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Function to display images in the left panel
def display_image(image, title):
    if image is not None:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        panel = tk.Label(window, image=image_tk)
        panel.image = image_tk
        panel.grid(row=1, column=0, padx=10, pady=10)
        
        title_label = tk.Label(window, text=title, font=("Arial", 20))
        title_label.grid(row=0, column=0)

# Function to encrypt the image
def encrypt_image():
    global image_encrypted, key
    if image_original is not None:
        image_normalized = image_original.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, image_normalized.shape) + np.finfo(float).eps
        image_encrypted = image_normalized / key
        display_image((image_encrypted * 255).astype(np.uint8), "Encrypted Image")
        messagebox.showinfo("Success", "Image Encrypted successfully.")
    else:
        messagebox.showwarning("Warning", "No image loaded for encryption.")

# Function to decrypt the image
def decrypt_image():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_decrypted = image_encrypted * key
        display_image((image_decrypted * 255).astype(np.uint8), "Decrypted Image")
        messagebox.showinfo("Success", "Image Decrypted successfully.")
    else:
        messagebox.showwarning("Warning", "No encrypted image found.")

# Function to save the current image
def save_img():
    if image_encrypted is not None:
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filepath:
            cv2.imwrite(filepath, (image_encrypted * 255).astype(np.uint8))
            messagebox.showinfo("Success", "Image saved successfully!")
    else:
        messagebox.showwarning("Warning", "No image to save.")

# Create buttons and layout
btn_frame = tk.Frame(window)
btn_frame.grid(row=2, column=0, pady=20)

btn_choose = tk.Button(btn_frame, text="Choose Image", command=open_img, font=("Arial", 14), bg="lightblue")
btn_choose.grid(row=0, column=0, padx=5)

btn_encrypt = tk.Button(btn_frame, text="Encrypt", command=encrypt_image, font=("Arial", 14), bg="lightgreen")
btn_encrypt.grid(row=0, column=1, padx=5)

btn_decrypt = tk.Button(btn_frame, text="Decrypt", command=decrypt_image, font=("Arial", 14), bg="lightcoral")
btn_decrypt.grid(row=0, column=2, padx=5)

btn_save = tk.Button(btn_frame, text="Save Image", command=save_img, font=("Arial", 14), bg="gold")
btn_save.grid(row=0, column=3, padx=5)

# Exit button with confirmation
def exit_app():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        window.destroy()

btn_exit = tk.Button(window, text="Exit", command=exit_app, font=("Arial", 16), bg="red")
btn_exit.grid(row=3, column=0, pady=10)

# Start the Tkinter main loop
window.mainloop()
