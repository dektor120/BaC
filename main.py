from tkinter import *
from tkinter.dialog import *
from tkinter import Tk , Text
from random import choice
import tkinter as tk
import tkinter.font as tkFont
import sqlite3
import re
import bcrypt
hidden_number= ''
moves_amount = 0
def create_user_table():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    connection.commit()
    connection.close()

def validate_data(data):
    return re.match("^[a-zA-Z0-9]+$", data) is not None

def check_existing_username(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    if not validate_data(username):
        lbl_status.config(text="Используйте только английские буквы и цифры\nбез пробелов.")
        return
    if not validate_data(password):
        lbl_status.config(text="Используйте только английские буквы и цифры\nбез пробелов.")
        return
    if check_existing_username(username):
        lbl_status.config(text="Пользователь с таким логином уже существует.")
        return
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
    connection.commit()
    connection.close()
    lbl_status.config(text="Регистрация прошла успешно")

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    if not validate_data(username):
        lbl_status.config(text="Используйте только английские буквы и цифры\nбез пробелов.")
        return
    if not validate_data(password):
        lbl_status.config(text="Используйте только английские буквы и цифры\nбез пробелов.")
        return
    if not check_existing_username(username):
        lbl_status.config(text="Пользователя с таким логином не существует.")
        return
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user is not None and bcrypt.checkpw(password.encode(), user[1]):
        lbl_status.config(text="Вход выполнен успешно")
        game()
    else:
        lbl_status.config(text="Введены неверные данные")
    connection.close()

def game():

    def check_number(input_text):
        try:
            number = int(input_text)
            if number >= 1023 and number <= 9876:
                msg.config(text="Число введено корректно")
                return True
            else:
                UserNumber.delete(0, 'end')
                msg.config(text="Число не подходит")
                return False
        except ValueError:
            UserNumber.delete(0, 'end')
            msg.config(text="Введено некорректное значение")

    def check_unique_digits(number):
        digit_set = set()
        while number > 0:
            digit = number % 10
            if digit in digit_set:
                UserNumber.delete(0, 'end')
                msg.config(text="Цифры не должны повторяться")
                return False
            digit_set.add(digit)
            number //= 10
        return True

    def number_generate():
        NumbersList = '0123456789'
        secret_number = choice(NumbersList[1:10])
        for i in range(3):
            NumbersList = ''.join(NumbersList.split(secret_number[i]))
            secret_number += choice(NumbersList)
        return secret_number

    def play(event):
        global hidden_number, moves_amount
        if len(hidden_number) == 0:
            hidden_number = number_generate()
            txt_field.configure(state=NORMAL)
            txt_field.delete("1.0", "end")
            txt_field.configure(state=DISABLED)
        guess_number = UserNumber.get()
        check = check_number(guess_number)
        int_GN = int(guess_number)
        if (check == True):
            check1 = check_unique_digits(int_GN)
            if (check1 == True):
                bulls = 0
                cows = 0
                for i in range(4):
                    if hidden_number[i] == guess_number[i]:
                        bulls += 1
                    elif guess_number[i] in hidden_number:
                        cows += 1
                moves_amount += 1
                txt_field.configure(state=NORMAL)
                txt_field.tag_configure("center", justify='center')
                txt_field.insert(END,
                                 str(moves_amount) + ". Ваше число: " + guess_number + ". Быков: " + str(bulls) + ". Коров: " + str(cows) + ".\n")
                txt_field.tag_add("center", "1.0", "end")
                txt_field.see("end")
                txt_field.configure(state=DISABLED)
                UserNumber.delete(0, END)
                if bulls == 4:
                    gameOver = Dialog(title='Победа за ' + str(moves_amount) + ' ходов.',
                                      text='     Сыграем ещё?           ',
                                      bitmap='questhead',
                                      default=0,
                                      strings=('Да', 'Нет'))
                    if gameOver.num == 1: tkgame.destroy()
                    moves_amount = 0
                    hidden_number = ''
                    txt_field.configure(state=NORMAL)
                    txt_field.delete("1.0", "end")
                    txt_field.tag_configure("left", justify='left')
                    txt_field.insert(END,
                                     "Правила игры:\n1.Системой загадано некое 4-ёхзначеное число.\n2.Вам нужно вводить свои числа в поле\nвыше и с помощью подсказок найти ответ.\n3.Количество быков - это количество цифр, которые\nнаходятся на своём месте в числе.\n4.Количество коров - это количество цифр, которые\nесть в числе, но на другой позиции.","left" )
                    txt_field.configure(state=DISABLED)
                    msg.config(text='Введите число от 1023 до 9876 '
                                    'такое, чтобы цифры, составляющие это число,'
                                    ' не повторялись!')

    window_login.destroy()
    tkgame = Tk()
    tkgame.resizable(False, False)
    tkgame.configure(bg='lightblue')
    screen_width1 = tkgame.winfo_screenwidth()
    screen_height1 = tkgame.winfo_screenheight()
    window_width = 400
    window_height = 350
    x_coord = (screen_width1 / 2) - (window_width / 2)
    y_coord = (screen_height1 / 2) - (window_height / 2)
    tkgame.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))
    tkgame.title('Быки и Коровы')
    msg = Message(width=400, padx=10, pady=5,
                  text='Введите число от 1023 до 9876 '
                       'такое, чтобы цифры, составляющие это число,'
                       ' не повторялись!')
    msg.pack(padx=10, pady=5)
    msg.config(bg='light grey', fg='black',
               font=('times', 12, 'italic'))
    UserNumber = Entry(width=8, justify='center', font=('times', 11, 'normal'))
    UserNumber.pack()
    UserNumber.focus()
    UserNumber.bind('<Return>', play)
    txt_field = Text(tkgame, height=200, width=400, pady=10, font=('times', 12, 'normal'))
    txt_field.insert(END,
                     "Правила игры:\n1.Системой загадано некое 4-ёхзначеное число.\n2.Вам нужно вводить свои числа в поле\nвыше и с помощью подсказок найти ответ.\n3.Количество быков - это количество цифр, которые\nнаходятся на своём месте в числе.\n4.Количество коров - это количество цифр, которые\nесть в числе, но на другой позиции.")
    txt_field.tag_add("center", "1.0", "end")
    txt_field.configure(state=DISABLED)
    txt_field.pack()
    tk.mainloop()


if __name__ == "__main__":
    create_user_table()
    window_login = Tk()
    window_login.title("Регистрация и авторизация")
    window_login.resizable(False, False)
    font_style = tkFont.Font(family="Arial", size=12)
    bg_color = '#e6e6e6'
    button_color = '#4CAF50'
    label_color = '#333333'
    width = 400
    height = 320
    screen_width = window_login.winfo_screenwidth()
    screen_height = window_login.winfo_screenheight()
    x_coord = (screen_width / 2) - (width / 2)
    y_coord = (screen_height / 2) - (height / 2)
    window_login.geometry('%dx%d+%d+%d' % (width, height, x_coord, y_coord))
    lbl_username = Label(window_login, text="Имя пользователя:", bg=bg_color, fg=label_color, font=font_style)
    lbl_username.pack(padx=20, pady=10)
    entry_username = Entry(window_login, font=font_style)
    entry_username.pack(padx=20, pady=5)
    lbl_password = Label(window_login, text="Пароль:", bg=bg_color, fg=label_color, font=font_style)
    lbl_password.pack(padx=20, pady=10)
    entry_password = Entry(window_login, show="*", font=font_style)
    entry_password.pack(padx=20, pady=5)
    btn_register = Button(window_login, text="Зарегистрироваться", command=register_user, bg=button_color,
                          font=font_style, fg='white')
    btn_register.pack(padx=20, pady=10)
    btn_login = Button(window_login, text="Войти", command=login_user, bg=button_color, font=font_style, fg='white')
    btn_login.pack(padx=20, pady=5)
    lbl_status = Label(window_login, text="", bg=bg_color, fg=label_color, font=font_style)
    lbl_status.pack(padx=20, pady=10)
    window_login.mainloop()










