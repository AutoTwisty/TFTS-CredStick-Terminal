import nfc
import nfc.clf
import nfc.tag.tt2
import nfc.tag.tt3
import nfc.tag.tt4
import nfc.tag.tt1

import ndef

def read_tag(tag):
    try:
        # Försöker läsa från en Typ 1 till Typ 4 tagg
        if isinstance(tag, nfc.tag.tt1.Type1Tag) or isinstance(tag, nfc.tag.tt2.Type2Tag) or \
           isinstance(tag, nfc.tag.tt3.Type3Tag) or isinstance(tag, nfc.tag.tt4.Type4Tag):
            tag_data = tag.ndef.records[0]
            return tag_data.text
        else:
            return "Kunde inte läsa från taggen. Okänt format."
    except Exception as e:
        return f"Fel vid läsning: {e}"

def write_tag(tag, new_data):
    try:
        if isinstance(tag, nfc.tag.tt1.Type1Tag) or isinstance(tag, nfc.tag.tt2.Type2Tag) or \
           isinstance(tag, nfc.tag.tt3.Type3Tag) or isinstance(tag, nfc.tag.tt4.Type4Tag):
            # Skapar ett nytt NDEF-meddelande
            print(new_data)
            data_in_text = new_data + ' Nuyen'
            print(data_in_text)
            tag.ndef.records = [ndef.TextRecord(data_in_text)]
            
            return "Data skrivet till taggen framgångsrikt!"
        else:
            return "Kunde inte skriva till taggen. Okänt format."
    except Exception as e:
        return f"Fel vid skrivning: {e}"

def main():
    clf = nfc.ContactlessFrontend('usb')
    print("Placera en Cred-Stick på läsaren...")

    while True:
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        if tag is not None:
            read_data = read_tag(tag)
            print(f"Läst data från Cred-Stick: {read_data}")

            if input("Vill du skriva över värdet på Cred-Stick? (j/n): ").lower() == 'j':
                new_data = input("Ange ny data att skriva till Cred-Stick: ")
                result = write_tag(tag, new_data)
                print(result)



if __name__ == "__main__":
    main()
