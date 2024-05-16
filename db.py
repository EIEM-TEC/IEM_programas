import tkinter as tk
import serial
import threading

# Function to read data from serial port
def read_serial(ser, label):
    while True:
        try:
            data = ser.readline().decode().strip()  # Read data from serial port
            if data != "":
                label.config(text=data+" dBA")  # Update label text with received data
        except Exception as e:
            print("Error reading serial data:", e)

# Initialize tkinter
root = tk.Tk()
root.title("Serial Data Reader")
root.geometry("400x200")

# Create label with large text
label = tk.Label(root, text="", font=("Helvetica", 72))
label.pack(pady=20)

# Connect to serial port
try:
    ser = serial.Serial('COM3', 115200, timeout=1)  # Adjust port and baud rate accordingly
    print("Connected to serial port")
    # Start a thread to continuously read data from serial
    read_serial_thread = threading.Thread(target=read_serial, args=(ser, label))
    read_serial_thread.daemon = True
    read_serial_thread.start()
except Exception as e:
    print("Error connecting to serial port:", e)

# Run the tkinter event loop
root.mainloop()