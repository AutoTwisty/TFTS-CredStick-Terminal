import tkinter as tk
from tkinter import simpledialog, messagebox
import nfc
import ndef

class NFCReaderWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("NFC Reader/Writer")
        
        self.reader = nfc.ContactlessFrontend('usb')
        
        self.label = tk.Label(root, text="Placera en NFC-tag på läsaren")
        self.label.pack(pady=20)
        
        self.read_button = tk.Button(root, text="Läs tagg", command=self.read_tag)
        self.read_button.pack(pady=10)
        
        self.write_button = tk.Button(root, text="Skriv ny data på tagg", command=self.write_tag)
        self.write_button.pack(pady=10)
        
    def read_tag(self):
        try:
            tag = self.reader.connect(rdwr={'on-connect': lambda tag: False})
            assert tag.ndef is not None
            data = tag.ndef.records[0]
            
            messagebox.showinfo("Tag Läsning", data.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        #finally:
            #self.reader.close()
    
    def write_tag(self):
        new_data = simpledialog.askstring("Skriv ny data", "Ange ny data (bara siffror):")
        if new_data is None:
            return
        
        if len(new_data) > 16:
            messagebox.showerror("Error", "Data är för lång, max 16 tecken tillåtet.")
            return
        
        #data_to_write = [ord(c) for c in new_data.ljust(16, '\0')]
        
        try:
            tag = self.reader.connect(rdwr={'on-connect': lambda tag: False})
            assert tag.ndef is not None
            tag.ndef.records = [ndef.TextRecord(str(new_data))]
            messagebox.showinfo("Skrivning lyckades", "Data har skrivits till taggen.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        #finally:
           # self.reader.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = NFCReaderWriter(root)
    root.mainloop()
