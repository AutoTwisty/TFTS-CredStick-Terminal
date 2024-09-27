import nfc
import nfc.clf
import nfc.tag.tt2
import nfc.tag.tt3
import nfc.tag.tt4
import nfc.tag.tt1
import ndef
import tkinter as tk
import tkinter.font
from tkinter import simpledialog, messagebox
from tkinter import ttk
from tkinter import *
from threading import *
import requests
from requests.auth import HTTPBasicAuth
import json


clf = nfc.ContactlessFrontend('usb')

username = "tales"
password = "IP*OHtkgR5CTi7Gcr6Bao#v0!AGrDKDj"
authentication = HTTPBasicAuth(username, password)

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
    if tag.ndef is not None:
        readData = tag.ndef.records[0]
        read_data_label.config(text=f"Nuyens on credstick: {readData.text}")
    if tag.ndef is None:
        read_data_label.config(text=f"No credstick detected")
        

def write_tag():
    readTag = scan_tag()
    old_value = readTag.ndef.records[0].text
    input_value = input_window.get()
    
    if matrixWrite.get() == 1:
        if handle_input.get() != "":
            #handle = handle_input.get()
            api_adress = "https://talesbot.codegrotto.com/api/balance/" + handle_input.get()
            print(api_adress)
            response = requests.get(api_adress,auth=authentication)
            print(response.status_code)
            print(response.content)
            if response.status_code >= 200 and response.status_code < 300:
                accountBalance = json.loads(response.content)
                accountBalance = accountBalance["amount"]
                print(accountBalance)
    
                if input_value[0] == "-" or input_value[0] == '-':
                    writeValue = int(old_value) - int(input_value[1:])
                    #Do some math: IF write value is not a negative number - increase the nuyen on the Matrix with the amount subtracted from credstick
                    if writeValue >= 0:
                        #accountBalance = accountBalance + input_value
                        transferData = {"receiver":handle_input.get(),"amount": int(input_value[1:])}
                    else:
                        #input would set credstick to a negative balance, set credstick to 0 instead and put whatever remained on credstick into handle account. AKA assume user just wants to take out as much as possible
                        #accountBalance = int(old_value)
                        transferData = {"receiver":handle_input.get(),"amount": int(old_value)}
                        writeValue = 0
                        #ALERT user that the credstick is now empty and inform them of how much was actualy transfered
                        messagebox.showerror('Transfer Alert', 'Alert: transfer requested exceeds value available on credstick. Remaining balance on credstick transfered to handle. Total amount transfered: {transfered_value}. Credstick is now empty.')


                elif input_value[0] == '+':
                    #Do some math: IF write value does not make Matrix value into negative number - decrease the nuyen on the Matrix with the amount added onto the credstick
                    if accountBalance >= int(input_value[1:]):
                        accountBalance = accountBalance - int(input_value[1:])
                        writeValue = int(old_value) + int(input_value[1:])
                        transferData = {"sender":handle_input.get(),"amount": int(input_value[1:])}
                    else:
                        print("user wants to put more credits on stick than they have on matrix account, alert user that they do not have the nuyen for that \n")
                        #user wants to put more credits on stick than they have on matrix account, alert user that they do not have the nuyen for that
                        #ALERT user
                        messagebox.showerror('Transfer Alert', 'Alert: transfer requested exceeds value available on bank account. No transfer was made. Please try again.')

                elif input_value[0] == '*' or input_value[0] == 'x':
                    writeValue = int(old_value) * int(input_value[1:])
                    print(writeValue)
                    #Do some math: IF write value does not make Matrix value into negative number - decrece the nuyen on the Matrix with the amount added onto the credstick
                    if accountBalance >= writeValue:
                        transferData = {"sender":handle_input.get(),"amount": writeValue}
                    else:
                        messagebox.showerror('Transfer Alert', 'Alert: transfer requested exceeds value available on bank account. No transfer was made. Please try again.')
                else:
                    #Compare new and old credstick value, if new is larger than old: subtract money from matrix account, same check as above. If old is larger than new, add money to matrix account, same check as above.
                    input_value = int(input_value)
                    old_value = int(old_value)
                    if input_value > old_value:
                        if accountBalance >= int(input_value):
                            accountBalance = accountBalance - input_value
                            writeValue = int(input_value)
                            transferData = {"sender":handle_input.get(),"amount": input_value}
                        else:
                            print("user wants to put more credits on stick than they have on matrix account, alert user that they do not have the nuyen for that \n")
                            #user wants to put more credits on stick than they have on matrix account, alert user that they do not have the nuyen for that
                            #ALERT user
                            messagebox.showerror('Transfer Alert', 'Alert: transfer requested exceeds value available on bank account. No transfer was made. Please try again.')

                    elif input_value < old_value:
                        writeValue = old_value - input_value
                        if writeValue >= 0:
                            #accountBalance = accountBalance + input_value
                            transferData = {"receiver":handle_input.get(),"amount": input_value}
                        else:
                            #input would set credstick to a negative balance, set credstick to 0 instead and put whatever remained on credstick into handle account. AKA assume user just wants to take out as much as possible
                            #accountBalance = int(old_value)
                            transferData = {"receiver":handle_input.get(),"amount": old_value}
                            writeValue = 0
                            #ALERT user that the credstick is now empty and inform them of how much was actualy transfered
                            transfered_value = old_value
                            messagebox.showerror('Transfer Alert', 'Alert: transfer requested exceeds value available on credstick. Remaining balance on credstick transfered to handle. Total amount transfered: {transfered_value}. Credstick is now empty.')

                response = requests.post("https://talesbot.codegrotto.com/api/transfer",auth=authentication, json = transferData)
                print(transferData)
                print(response.status_code)
                print(response.text)
                print(response.json)

            else:
                error_code = response.status_code
                print("Error during GET, response from server: {error_code}")
                messagebox.showerror('Server Error', 'Error: {error_code}')
        else:
            #ERROR no handle
            messagebox.showerror('Input ERROR', 'Error: No handle!')
            return False
    else:

        if input_value[0] == "-" or input_value[0] == '-':
            writeValue = int(old_value) - int(input_value[1:])
        elif input_value[0] == '+':
            writeValue = int(old_value) + int(input_value[1:])
        elif input_value[0] == '*' or input_value[0] == 'x':
            writeValue = int(old_value) * int(input_value[1:])
        else:
            writeValue = input_value

    readTag.ndef.records = [ndef.TextRecord(str(writeValue))]
    #place_label.config(text=f"Write successful")



def main():
    while True:
        scan_tag()


# Create main window


root = tk.Tk()
root.title("Cred-Stick Reader/Writer")
root.geometry("500x700")
root.configure(background='black')

TitleFont = tkinter.font.Font( family = "Terminal",  
                                 size = 20 
                                 )
NormalFont = tkinter.font.Font( family = "Terminal",  
                                 size = 10 
                                 ) 

frame1 = tk.Frame(master=root, height=20, bg="#804000")
frame1.pack(fill=tk.X)

# Place a Cred-Stick on the reader label
place_label = tk.Label(root, text="Place credstick on reader...",fg="#ffe6cc",bg="#804000")
place_label.config(font = TitleFont)
place_label.pack(pady=10)

# Label to show read data
read_data_label = tk.Label(root, text="", fg="#ffe6cc",bg="#804000")
read_data_label.config(font = TitleFont)
read_data_label.pack(pady=30)

# Label to show result of write operation
#result_label = tk.Label(root, text="", fg="#ffa64d",bg="#804000")
#result_label.pack(pady=10)

input_label = tk.Label(root, text="New credstick balance (You can also use - , + and *):", fg="#ffe6cc",bg="#804000")
input_label.pack(pady=5)
input_label.config(font = NormalFont)
input_window = tk.Entry(root)
input_window.config(font = NormalFont)
input_window.pack(pady=10)

matrixWrite = IntVar()
writeToMatrixCheck = tk.Checkbutton(root, text="Withdraw/Deposit nuyen to Matrix handle?",fg="#ffe6cc",bg="#804000",variable=matrixWrite, onvalue=1, offvalue=0)
writeToMatrixCheck.config(font = NormalFont)
writeToMatrixCheck.pack(pady=50)

handle_input_label = tk.Label(root, text = "Enter handle to withdraw/deposit nuyen from/to:", fg="#ffe6cc",bg="#804000")
handle_input_label.config(font = NormalFont)
handle_input_label.pack(pady=5)

handle_input = tk.Entry(root)
handle_input.config(font = NormalFont)
handle_input.pack(pady=20)

# Write button
write_button = tk.Button(root, text="Write new value",fg="#ffe6cc",bg="#804000", command=write_tag)
write_button.config(font = TitleFont)
write_button.pack(pady=50)


threading()
root.mainloop()
