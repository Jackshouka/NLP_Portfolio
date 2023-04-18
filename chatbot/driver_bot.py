import tkinter as tk
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
from bot import Bot
from tkinter import Entry, Label, Button, Text, END 

def main():
    def on_send_click():
        input_text = input_box.get()
        response = bot.respond(input_text)
        chat_history.insert(END, "You: " + input_text + '\n')
        chat_history.insert(END, "Bot: " + response + '\n')

    bot = Bot("guilty_gear_data.db")

    root = tk.Tk()
    root.title("Dustloop Chatbot")

    chat_history = Text(root, wrap = tk.WORD)
    chat_history.pack(padx=10, pady=10)

    input_box = Entry(root, width=50)
    input_box.pack(padx=20, pady=10)

    send_button = Button(root, text="Send", command=on_send_click)
    send_button.pack(padx=10, pady=10)

    root.mainloop()
    bot.close()

if __name__ == "__main__":
    main()