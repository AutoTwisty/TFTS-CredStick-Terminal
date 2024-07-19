import tkinter as tk
from tkinter import simpledialog, messagebox
from smartcard.System import readers
from smartcard.util import toHexString, toBytes

class NFCReaderWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("NFC Reader/Writer")
        
        self.readers = readers()
        if len(self.readers) == 0:
            messagebox.showerror("Error", "Ingen NFC-läsare hittades.")
            return
        
        self.reader = self.readers[0]
        self.connection = self.reader.createConnection()
        self.connection.connect()
        
        self.label = tk.Label(root, text="Placera en NFC-tag på läsaren")
        self.label.pack(pady=20)
        
        self.read_button = tk.Button(root, text="Läs tagg", command=self.read_tag)
        self.read_button.pack(pady=10)
        
        self.write_button = tk.Button(root, text="Skriv ny data på tagg", command=self.write_tag)
        self.write_button.pack(pady=10)
        
    def read_tag(self):
        try:
            apdu = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            response, sw1, sw2 = self.connection.transmit(apdu)
            tag_id = toHexString(response)
            
            apdu_read = [0xFF, 0xB0, 0x00, 0x04, 0x10] # Reading 16 bytes from block 4
            data, sw1, sw2 = self.connection.transmit(apdu_read)
            tag_data = ''.join(chr(b) for b in data if b != 0)
            
            messagebox.showinfo("Tag Läsning", f"Tag ID: {tag_id}\nData: {tag_data}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def write_tag(self):
        new_data = simpledialog.askstring("Skriv ny data", "Ange ny data (max 16 tecken):")
        if new_data is None:
            return
        
        if len(new_data) > 16:
            messagebox.showerror("Error", "Data är för lång, max 16 tecken tillåtet.")
            return
        
        data_to_write = [ord(c) for c in new_data.ljust(16, '\0')]
        apdu_write = [0xFF, 0xD6, 0x00, 0x04, 0x10] + data_to_write # Writing 16 bytes to block 4
        
        try:
            response, sw1, sw2 = self.connection.transmit(apdu_write)
            if sw1 == 0x90 and sw2 == 0x00:
                messagebox.showinfo("Skrivning lyckades", "Data har skrivits till taggen.")
            else:
                messagebox.showerror("Skrivning misslyckades", f"Status: {sw1:02X} {sw2:02X}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = NFCReaderWriter(root)
    root.mainloop()
