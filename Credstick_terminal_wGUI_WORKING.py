import nfc
import nfc.clf
import nfc.tag.tt2
import nfc.tag.tt3
import nfc.tag.tt4
import nfc.tag.tt1
import ndef
import tkinter as tk
from tkinter import simpledialog, messagebox
import time, threading

tag = None

def read_tag(tag):
    try:
        # Försöker läsa från en Typ 1 till Typ 4 tagg
        if isinstance(tag, nfc.tag.tt1.Type1Tag) or isinstance(tag, nfc.tag.tt2.Type2Tag) or \
           isinstance(tag, nfc.tag.tt3.Type3Tag) or isinstance(tag, nfc.tag.tt4.Type4Tag):
            tag_data = tag.ndef.records[0]
            return tag_data.text
        else:
            return "Unknow format, Could not read creditstick"
    except Exception as e:
        return f"Error when reading {e}"

def write_tag(tag, new_data):
    try:
        if isinstance(tag, nfc.tag.tt1.Type1Tag) or isinstance(tag, nfc.tag.tt2.Type2Tag) or \
           isinstance(tag, nfc.tag.tt3.Type3Tag) or isinstance(tag, nfc.tag.tt4.Type4Tag):
            # Skapar ett nytt NDEF-meddelande
            data_in_text = new_data + ' Nuyen'
            tag.ndef.records = [ndef.TextRecord(data_in_text)]
            return "New credit value recorded successfully"
        else:
            return "Could not write to credstick, unknown format"
    except Exception as e:
        return f"Error when writing: {e}"

def main():
    def on_read_button_click():
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        if tag is not None:
            read_data = read_tag(tag)
            read_data_label.config(text=f"Nuyens on credstick: {read_data}")

            #write_prompt = messagebox.askyesno("Write data", "Change value on credstick?")
            #if write_prompt:
                #new_data = simpledialog.askstring("New data", "Input new value on credstick:")
                #new_data = input_window.get()
                #if new_data != '':
                  #  result = write_tag(tag, new_data)
                  #  input_window.delete(0, tk.END)
                   # result_label.config(text=result)


    # Initialize NFC reader
    clf = nfc.ContactlessFrontend('usb')

    # Create main window
    root = tk.Tk()
    root.title("Cred-Stick Reader/Writer")

    frame1 = tk.Frame(master=root, height=20, bg="red")
    frame1.pack(fill=tk.X)

    # Place a Cred-Stick on the reader label
    place_label = tk.Label(root, text="Place credstick on reader...")
    place_label.pack(pady=10)

    # Read button
    #read_button = tk.Button(root, text="Read ", command=on_read_button_click)
    #read_button.pack(pady=10)

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

    button = tk.Button(root, text="Write value", width=25, height=5)
    button.bind("<Button-1>", write_tag(tag,input_window.get()))
    

    ticker = threading.Event()
    while not ticker.wait(2):
        on_read_button_click()

    root.mainloop()


    

if __name__ == "__main__":
    main()
