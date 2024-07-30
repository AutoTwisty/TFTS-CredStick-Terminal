import nfc
import nfc.clf
import nfc.tag.tt2
import nfc.tag.tt3
import nfc.tag.tt4
import nfc.tag.tt1
import ndef
import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import *


clf = nfc.ContactlessFrontend('usb')


#Functions

def threading():
    t1=Thread(target=main)
    t1.start()

def scan_tag():
    readTag = clf.connect(rdwr={'on-connect': updateReadData})
    if readTag is not None:
        return readTag
    else:
        print("Error: Tag empty or not scannable")

def updateReadData(tag):
    print(tag.ndef)
    if tag.ndef is not None:
        readData = tag.ndef.records[0]
        read_data_label.config(text=f"Nuyens on credstick: {readData.text}")
        

def write_tag():
    readTag = scan_tag()
    readTag.ndef.records = [ndef.TextRecord(input_window.get())]

def main():
    while True:
        scan_tag()


# Create main window
root = tk.Tk()
root.title("Cred-Stick Reader/Writer")

frame1 = tk.Frame(master=root, height=20, bg="red")
frame1.pack(fill=tk.X)

# Place a Cred-Stick on the reader label
place_label = tk.Label(root, text="Place credstick on reader...")
place_label.pack(pady=10)

# Label to show read data
read_data_label = tk.Label(root, text="")
read_data_label.pack(pady=10)

# Label to show result of write operation
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

input_label = tk.Label(root, text="New credit balance")
input_label.pack(pady=10)
input_window = tk.Entry(root)
input_window.pack(pady=10)

# Write button
write_button = tk.Button(root, text="Write new value", command=write_tag)
write_button.pack(pady=10)

threading()
root.mainloop()
