import cv2
import tkinter as tk
from tkinter import messagebox

def take_photo():
    # Zugriff auf die Kamera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Fehler", "Kamera konnte nicht geöffnet werden!")
        return

    ret, frame = cap.read()
    if ret:
        # Speichere das Bild als picture.png
        cv2.imwrite("picture.png", frame)
        messagebox.showinfo("Erfolg", "Foto wurde gespeichert als picture.png")
    else:
        messagebox.showerror("Fehler", "Konnte kein Bild aufnehmen!")

    cap.release()

def on_key_press(event):
    if event.char == 't':
        take_photo()

# GUI erstellen
root = tk.Tk()
root.title("Kamera App")

root.bind('<KeyPress>', on_key_press)

take_photo_button = tk.Button(root, text="Foto machen", command=take_photo)
take_photo_button.pack(pady=20)

root.mainloop()
