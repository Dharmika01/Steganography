import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import binascii
from bitarray import bitarray

# Function to encode the text into the image
def encode_message():
    image_path = image_path_entry.get()
    secret_message = secret_message_entry.get()

    if not image_path or not secret_message:
        messagebox.showerror("Error", "Please provide an image and a secret message.")
        return

    try:
        image = Image.open(image_path)
        encoded_image = steganography_encode(image, secret_message)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            encoded_image.save(save_path)
            messagebox.showinfo("Success", "Message hidden successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to decode the hidden message from the image
def decode_message():
    image_path = image_path_entry.get()

    if not image_path:
        messagebox.showerror("Error", "Please provide an image to decode.")
        return

    try:
        image = Image.open(image_path)
        decoded_message = steganography_decode(image)
        messagebox.showinfo("Decoded Message", decoded_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to encode a secret message into an image using LSB
def steganography_encode(image, secret_message):
    # Convert message to binary format
    message_bin = ''.join(format(ord(char), '08b') for char in secret_message)
    message_bin += '1111111111111110'  # Delimiter to mark end of the message

    # Make sure the image has enough pixels to store the message
    pixels = image.load()
    width, height = image.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):  # RGB channels
                if data_index < len(message_bin):
                    pixel[i] = pixel[i] & ~1 | int(message_bin[data_index])
                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(message_bin):
                return image

    raise ValueError("The image is too small to hide the message.")

# Function to decode the hidden message from an image
def steganography_decode(image):
    pixels = image.load()
    width, height = image.size
    message_bin = ''

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):  # RGB channels
                message_bin += str(pixel[i] & 1)

    # Convert binary string to text
    message_bin = [message_bin[i:i+8] for i in range(0, len(message_bin), 8)]
    secret_message = ''.join(chr(int(bin_str, 2)) for bin_str in message_bin)
    
    # Find the delimiter and extract the actual message
    delimiter = '1111111111111110'
    decoded_message = secret_message.split(delimiter)[0]

    return decoded_message

# Creating the Tkinter window
window = tk.Tk()
window.title("Steganography Tool")
window.geometry("500x400")

# Image path and secret message input
image_path_label = tk.Label(window, text="Image Path")
image_path_label.pack(pady=5)

image_path_entry = tk.Entry(window, width=40)
image_path_entry.pack(pady=5)

browse_button = tk.Button(window, text="Browse", command=lambda: image_path_entry.insert(0, filedialog.askopenfilename()))
browse_button.pack(pady=5)

secret_message_label = tk.Label(window, text="Secret Message")
secret_message_label.pack(pady=5)

secret_message_entry = tk.Entry(window, width=40)
secret_message_entry.pack(pady=5)

# Buttons to encode and decode messages
encode_button = tk.Button(window, text="Encode Message", command=encode_message)
encode_button.pack(pady=10)

decode_button = tk.Button(window, text="Decode Message", command=decode_message)
decode_button.pack(pady=10)

# Run the application
window.mainloop()
