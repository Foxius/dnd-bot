import tkinter as tk
from tkinter import Canvas, NW
from PIL import Image, ImageTk
import random
import winsound
limit = 20
def roll(limit):
    image_path = f"files/images/d{limit}.png"
    # Загружаем изображение с помощью библиотеки Pillow
    image = Image.open(image_path)

    # Создаем окно программы
    root = tk.Tk()
    root.title("Вывод цифры на середине картинки")

    # Создаем холст с размерами картинки
    canvas = Canvas(root, width=image.width, height=image.height)
    canvas.pack()

    # Отображаем картинку на холсте
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=image_tk)

    random_digit = random.randint(1, limit)

    center_x = image.width // 2
    center_y = image.height // 2
    winsound.PlaySound("files/sounds/rolldice.wav", winsound.SND_FILENAME)

    # Выводим цифру на холсте
    canvas.create_text(center_x, center_y, text=str(random_digit), fill="white", font=("Arial", 30))
    root.mainloop()
roll(limit)

