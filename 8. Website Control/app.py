import requests
import tkinter as tk
from tkinter import messagebox

# ESP32 IP address
ESP32_IP = "http://192.168.37.8"  # Replace with your ESP32's IP address

def send_coordinates():
    """Send the entered coordinates to the ESP32."""
    try:
        # Get the entered coordinates
        currentX = float(currentX_entry.get())
        currentY = float(currentY_entry.get())
        targetX = float(targetX_entry.get())
        targetY = float(targetY_entry.get())

        # Send coordinates to ESP32
        params = {
            "currentX": currentX,
            "currentY": currentY,
            "targetX": targetX,
            "targetY": targetY
        }

        response = requests.get(f"{ESP32_IP}/set_coordinates", params=params)

        if response.status_code == 200:
            messagebox.showinfo("Success", "Coordinates sent successfully!")
            print("Response:", response.text)
        else:
            messagebox.showerror("Error", "Failed to send coordinates!")
            print("Error:", response.text)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Failed to connect to ESP32: {e}")

# Create the GUI window
root = tk.Tk()
root.title("ESP32 Coordinate Sender")

# Create and place labels and entry boxes for coordinates
tk.Label(root, text="Current X:").grid(row=0, column=0, padx=10, pady=5)
currentX_entry = tk.Entry(root)
currentX_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Current Y:").grid(row=1, column=0, padx=10, pady=5)
currentY_entry = tk.Entry(root)
currentY_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Target X:").grid(row=2, column=0, padx=10, pady=5)
targetX_entry = tk.Entry(root)
targetX_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Target Y:").grid(row=3, column=0, padx=10, pady=5)
targetY_entry = tk.Entry(root)
targetY_entry.grid(row=3, column=1, padx=10, pady=5)

# Create and place the send button
send_button = tk.Button(root, text="Send Coordinates", command=send_coordinates)
send_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()