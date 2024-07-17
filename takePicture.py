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

def update_frame():
    ret, frame = cap.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, update_frame)

def switchToCam():
    global lmain 
    for widget in root.winfo_children():
        widget.destroy()
    
    lmain = tk.Label(root)
    lmain.pack(fill=tk.BOTH, expand=True)
    take_photo_button = tk.Button(root, text="Überprüfe QR Code", command=take_photo)
    take_photo_button.pack(pady=20)

    update_frame()

def displayData(data):
    for widget in root.winfo_children():
        widget.destroy()

    take_another_photo_button = tk.Button(root, text="Weiteres Produkt scannen", command=switchToCam)
    take_another_photo_button.pack(pady=20)

    for key, value in data.items():
        label = tk.Label(root, text=f"{key}: {value}", justify='left')
        label.pack(padx=10, pady=10)

def getData(barcodeDataCode):
    try:
        response = requests.get(f'https://world.openfoodfacts.org/api/v2/product/{barcodeDataCode}.json')
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        messagebox.showerror("Fehler", f"HTTP Fehler: {str(e)}")
        return None

    try:
        data = response.json()
    except ValueError:
        messagebox.showerror("Fehler", "Fehler beim Dekodieren der JSON-Daten")
        return None

    product_data = data.get('product', {})

    showed_data = {
        "ID": data.get('code', 'Keine Daten'),
        "Produktname": product_data.get('generic_name_de', 'Keine Daten'),
        "Marke(n)": product_data.get('brands', 'Keine Daten'),
        "Nutri-Score Note": product_data.get('nutriscore_grade', 'Keine Daten'),
        "Nutri-Score Punkte": product_data.get('nutriscore_score', 'Keine Daten'),
        "In folgenden Ländern verfügbar": product_data.get('countries', 'Keine Daten'),
        "Nahrungsgruppe(n)": product_data.get('food_groups', 'Keine Daten'),
        "Kategorie(n)": product_data.get('categories', 'Keine Daten'),
        "Zutaten": product_data.get('ingredients_text_de', 'Keine Daten'),
        "Beschriftungen": product_data.get('labels', 'Keine Daten')
    }

    displayData(showed_data)

def BarcodeReader(image):
    img = cv2.imread(image)

    detectedBarcodes = decode(img)

    if not detectedBarcodes:
        messagebox.showerror("Fehler", "Barcode wurde nicht erkannt oder ist leer/beschädigt!")
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
                getData(barcodeDataCode)

def take_photo():
    if not cap.isOpened():
        messagebox.showerror("Fehler", "Kamera konnte nicht geöffnet werden!")
        return

    ret, frame = cap.read()
    if ret:
        cv2.imwrite("picture.png", frame)
        BarcodeReader("picture.png")
    else:
        messagebox.showerror("Fehler", "Konnte kein Bild aufnehmen!")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    messagebox.showerror("Fehler", "Kamera konnte nicht geöffnet werden!")
    cap.release()
    exit()


take_photo_button = tk.Button(root, text="Check QR Code", command=take_photo)
take_photo_button.pack(pady=20)
update_frame()
root.mainloop()

cap.release()
