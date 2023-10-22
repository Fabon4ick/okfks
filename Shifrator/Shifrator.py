import customtkinter
import customtkinter as CTk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from PIL import ImageTk

# Азбука Морзе
morse_code = {'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..', 'Е': '.', 'Ё': '.', 'Ж': '...-', 'З': '--..',
              'И': '..', 'Й': '.---', 'К': '-.-',
              'Л': '.-..', 'М': '--', 'Н': '-.', 'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-', 'У': '..-',
              'Ф': '..-.', 'Х': '....', 'Ц': '-.-.',
              'Ч': '---.', 'Ш': '----', 'Щ': '--.-', 'Ь': '-..-', 'Ъ': '-..-', 'Ы': '-.--', 'Э': '..-..', 'Ю': '..--',
              'Я': '.-.-',

              '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
              '7': '--...', '8': '---..', '9': '----.',
              '.': '......', ',': '.-.-.-', ';': '-.-.-.', ':': '---...', '?': '..--..', '!': '--..--', '-': '-....-',
              '"': '.-..-.', '(': '-.--.', ')': '-.--.-',
              '/': '-..-.', '+': '.-.-.', '=': '-...-', '@': '.--.-.'
              }

# Английский алфавит для проверки ввода
ingl_alphabet = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z'}

entry = None


def show_info():
    showinfo(title="Информация по использованию", message="1. Шифратор использует только русский язык.\n\n"
                                                          "2. Для шифрации Азбукой Морзе напишите свой текст в\n    поле ввода и нажмите кнопку 'Зашифровать'.\n\n3. Для дешифрации Азбуки Морзе в конце вашего "
                                                          "\n    предложения должен стоять пробел.\n\n4. Для иcпользования шифра "
                                                          "Цезаря также вводим свой\n    текст в поле ввода, но также необходимо указать 'шаг', с\n    которым будет происходить шифрация.\n\n"
                                                          "5. Чтобы дешифровать шифр Цезаря снова введите свой\n    текст и укажите необходимый сдвиг.\n\n6.При пользовании шифром Атбашь "
                                                          "просто вводим\n   интересующий текст в поле ввода, и программа\n   зашифрует его.\n\n7. Для использования шифра Виженера введите свой текст\n    в поле ввода, а"
                                                          " также укажите ключ для шифрации.\n\n8. При шифрации 'Перестановкой' введите интересующий\n    текст и ключ для перемешивания символов.\n\n9. Кнопка 'Копировать' "
                                                          "копирует окончательный результат\n    из поля вывода.\n\n10. Выход из программы выполняется по кнопке 'Выход'\n      или по нажатию на крестик."
                                                          "\n\n© Shipitsyn D.A.")


# Функция конвертации
def morseEncoder(text):
    text = input_text.get("1.0", END).upper()
    morse_text = ''
    for char in text:
        if char in ingl_alphabet:
            showinfo(title="Предупреждение", message="Введён неверный формат.")
            clear_text1()
            clear_text2()
            return "break"
        elif char in morse_code:
            morse_text += morse_code[char] + ' '
        elif char == ' ':
            morse_text += ' '
    return morse_text


def morseDecoder(message):
    global i
    message = input_text.get("1.0", END)
    decipher = ''
    citext = ''
    for char in message:
        if char != ' ':
            i = 0
            citext += char
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(morse_code.keys())[list(morse_code.values()).index(citext)]
                citext = ''
                decipher = decipher.capitalize()
    return decipher


def caesarEncoder(text, shift):
    cipher_text = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('А') if char.isupper() else ord('а')
            cipher_text += chr((ord(char) - ascii_offset + shift) % 32 + ascii_offset)
        else:
            cipher_text += char
    return cipher_text


def atbashEncoder(text):
    result = ""
    for char in text:
        if char.isalpha():
            offset = ord('А') if char.isupper() else ord('а')
            result += chr(31 - (ord(char) - offset) + offset)
        else:
            result += char
    return result


def atbashDecoder(text):
    return atbashEncoder(text)


def vigenereEncoderDecoder(text, key_entry, mode):
    key_entry = key_entry.lower()
    key_len = len(key_entry)
    text = text.lower()
    result = []

    for i, char in enumerate(text):
        if char.isalpha():
            key_char = key_entry[i % key_len]
            shift = (ord(key_char) - ord('а')) if key_char.isalpha() else 0
            if mode == 'decrypt':
                shift = -shift
            shifted_char = chr(((ord(char) - ord('а') + shift) % 33) + ord('а'))
            result.append(shifted_char)
        else:
            result.append(char)

    return ''.join(result)


def transpositionEncoder(text, key_entry):
    key = int(key_entry)
    encrypted_message = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(text):
            encrypted_message[col] += text[pointer]
            pointer += key
    return ''.join(encrypted_message)


def transpositionDecoder(text, key_entry):
    key = int(key_entry)
    num_rows = -(-len(text) // key)
    num_empty_boxes = (num_rows * key) - len(text)
    decrypted_message = [''] * num_rows
    col, row = 0, 0
    for symbol in text:
        decrypted_message[row] += symbol
        row += 1
        if (row == num_rows) or (row == num_rows - 1 and col >= key - num_empty_boxes):
            row = 0
            col += 1
    return ''.join(decrypted_message)


def Encoder():
    text = input_text.get("1.0", CTk.END).strip()
    selected_cipher = combo.get()
    if selected_cipher == "Азбука Морзе":
        output = morseEncoder(text)
    elif selected_cipher == "Шифр Цезаря":
        shift = int(key_entry.get())
        output = caesarEncoder(text, shift)
    elif selected_cipher == "Шифр Атбаш":
        output = atbashEncoder(text)
    elif selected_cipher == "Шифр Виженера":
        key = key_entry.get()
        output = vigenereEncoderDecoder(text, key, 'encrypt')
    elif selected_cipher == "Шифр Перестановки":
        key = int(key_entry.get())
        output = transpositionEncoder(text, key)

    output_text.delete("1.0", CTk.END)
    output_text.insert(END, output)


def Decoder():
    message = input_text.get("1.0", CTk.END).strip()
    selected_cipher = combo.get()
    if selected_cipher == "Азбука Морзе":
        output = morseDecoder(message)
    elif selected_cipher == "Шифр Цезаря":
        shift = int(key_entry.get())
        output = caesarEncoder(message, -shift)
    elif selected_cipher == "Шифр Атбаш":
        output = atbashDecoder(message)
    elif selected_cipher == "Шифр Виженера":
        key = key_entry.get()
        output = vigenereEncoderDecoder(message, key, 'decrypt')
    elif selected_cipher == "Шифр Перестановки":
        key = int(key_entry.get())
        output = transpositionDecoder(message, key)

    output_text.delete(1.0, CTk.END)
    output_text.insert(CTk.END, output)


# Функция копирования второго поля
def copy():
    root.clipboard_clear()
    root.clipboard_append(output_text.get('1.0', CTk.END).rstrip())


# Очистка полей ввода и вывода
def clear_texts():
    clear_text1()
    clear_text2()
    clear_text3()
    clear_key()


def clear_text1():
    input_text.delete("1.0", END)


def clear_text2():
    output_text.delete("1.0", END)


def clear_text3():
    output_text.delete("1.0", END)


def clear_key():
    key_entry.delete(0, END)


# Функция выхода из программы
def exit_func():
    quit()


# Функция для создания поля Entry
def create_entry(event):
    selected_option = combo.get()

    if selected_option == "Шифр Цезаря":
        if not entry_exists():
            create_new_entry()
    elif selected_option == "Шифр Виженера":
        if not entry_exists():
            create_new_entry()
    elif selected_option == "Шифр Перестановки":
        if not entry_exists():
            create_new_entry()
    else:
        if entry_exists():
            remove_entry()


def remove_entry():
    global key_entry
    if entry_exists():
        key_entry.destroy()
        input_label.destroy()


def entry_exists():
    for widget in root.winfo_children():
        if isinstance(widget, customtkinter.CTkEntry):
            return True
    return False


def create_new_entry():
    global key_entry
    global input_label
    input_label = customtkinter.CTkLabel(root, text="Ключ:")
    input_label.place(x=360, y=98)
    key_entry = customtkinter.CTkEntry(root, height=30, width=45)
    key_entry.place(x=358, y=125)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Оформление окна
root = customtkinter.CTk()
root.title("Шифратор/дешифратор")
root.geometry("770x430")

image_info = ImageTk.PhotoImage(file="info.png")
button_info = customtkinter.CTkButton(root, image=image_info, text="", width=30, height=30, command=show_info)
button_info.place(x=30, y=15)

input_label = customtkinter.CTkLabel(root, text="Ввод:")
input_label.place(x=30, y=70)

input_text = customtkinter.CTkTextbox(root, font=('Courier', 13), height=150, width=290)
input_text.place(x=30, y=98)

# input_label = customtkinter.CTkLabel(root, text="Ключ:")
# input_label.place(x=360, y=98)

# key_entry = customtkinter.CTkEntry(root, height=30, width=45)
# key_entry.place(x=358, y=125)

output_label = customtkinter.CTkLabel(root, text="Вывод:")
output_label.place(x=440, y=70)

output_text = customtkinter.CTkTextbox(root, font=('Courier', 13), height=150, width=290)
output_text.place(x=440, y=98)

convert_encoder = customtkinter.CTkButton(root, text="Зашифровать", command=Encoder)
convert_encoder.place(x=180, y=280)

button_decoder = customtkinter.CTkButton(root, text="Дешифрация", command=Decoder)
button_decoder.place(x=440, y=280)

button_copy = customtkinter.CTkButton(root, text="Копировать", command=copy)
button_copy.place(x=180, y=340)

button_clear = customtkinter.CTkButton(root, text="Очистить", command=clear_texts)
button_clear.place(x=440, y=340)

image_quit = ImageTk.PhotoImage(file="exit.png")
button_exit = customtkinter.CTkButton(root, image=image_quit, text="", height=30, width=30, command=exit_func)
button_exit.place(x=690, y=15)

combo_label = customtkinter.CTkLabel(root, text="Выберите шифр:")
combo_label.place(x=320, y=10)

combo = ttk.Combobox(root, values=["Азбука Морзе", "Шифр Цезаря", "Шифр Атбаш", "Шифр Виженера", "Шифр Перестановки"])
combo.set("...")
combo.place(x=300, y=35)

combo.bind("<<ComboboxSelected>>", create_entry)

root.mainloop()
