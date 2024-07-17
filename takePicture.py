import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import json
import requests

root = tk.Tk()
root.title("Barcodescanner")
lmain = tk.Label(root)
lmain.pack(fill=tk.BOTH, expand=True)


def displayData(data):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"ID: {data['code']}").pack()
    tk.Label(root, text=f"Produktname: {data['product']['generic_name_de']}").pack()
    tk.Label(root, text=f"Nahrungsgruppe(n): {data['product']['food_groups']}").pack()
    tk.Label(root, text=f"Kategorie(n): {data['product']['categories']}").pack()

    

def getData(barcodeDataCode):
    response = requests.get(f'https://world.openfoodfacts.org/api/v2/product/{barcodeDataCode}.json')

    if response.status_code == 200:
        try:
            data = response.json()
            displayData(data)
        except ValueError:
            print("Fehler beim Dekodieren der JSON-Daten")
    else:
        print(f"HTTP Fehler: {response.status_code}")
        return None

def BarcodeReader(image):
    img = cv2.imread(image)

    detectedBarcodes = decode(img)

    if not detectedBarcodes: 
        print("Barcode Not Detected or your barcode is blank/corrupted!") 
    else: 
        for barcode in detectedBarcodes:   
            # Locate the barcode position in image 
            (x, y, w, h) = barcode.rect 
              
            # Put the rectangle in image using  
            # cv2 to highlight the barcode 
            cv2.rectangle(img, (x-10, y-10), 
                          (x + w+10, y + h+10),  
                          (255, 0, 0), 2)

            barcodeDataCode = barcode.data.decode("utf-8")
              
            if barcode.data!="": 
                print(barcodeDataCode) 
                # print(barcode.type) 
                getData(barcodeDataCode)

def take_photo():
    if not cap.isOpened():
        messagebox.showerror("Fehler", "Kamera konnte nicht geöffnet werden!")
        return

    ret, frame = cap.read()
    if ret:
        # Speichere das Bild als picture.png
        cv2.imwrite("picture.png", frame)
        BarcodeReader("picture.png")
       # messagebox.showinfo("Erfolg", "Foto wurde gespeichert als picture.png")
    else:
        messagebox.showerror("Fehler", "Konnte kein Bild aufnehmen!")

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Konvertiere das Bild in ein Format, das tkinter anzeigen kann
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, update_frame)

# Zugriff auf die Kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    messagebox.showerror("Fehler", "Kamera konnte nicht geöffnet werden!")
    cap.release()
    exit()

# GUI erstellen
take_photo_button = tk.Button(root, text="Check QR Code", command=take_photo)
take_photo_button.pack(pady=20)
update_frame()  # Starte den Kamera-Feed
root.mainloop()

cap.release()
