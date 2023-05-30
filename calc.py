import tkinter as tk
import sqlite3

class Calculadora:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculadora")

        self.entry = tk.Entry(self.window)
        self.entry.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

        self.db_connection = sqlite3.connect("calculadora.db")
        self.create_table()

        self.window.mainloop()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS historico (id INTEGER PRIMARY KEY AUTOINCREMENT, expressao TEXT, resultado REAL)"
        )
        self.db_connection.commit()

    def insert_into_history(self, expressao, resultado):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO historico (expressao, resultado) VALUES (?, ?)", (expressao, resultado))
        self.db_connection.commit()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'Histórico'  # Botão para exibir o histórico
        ]

        row = 1
        col = 0

        for button in buttons:
            tk.Button(
                self.window, text=button, width=5, command=lambda value=button: self.button_click(value)
            ).grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def button_click(self, value):
        if value == '=':
            expressao = self.entry.get()
            resultado = eval(expressao)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(resultado))
            self.insert_into_history(expressao, resultado)
        elif value == 'Histórico':
            self.show_history()
        else:
            self.entry.insert(tk.END, value)

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("Histórico")

        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_listbox = tk.Listbox(history_window, yscrollcommand=scrollbar.set)
        history_listbox.pack(fill=tk.BOTH, expand=True)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM historico")
        records = cursor.fetchall()

        for record in records:
            expressao = record[1]
            resultado = record[2]
            history_listbox.insert(tk.END, f"Expressão: {expressao} - Resultado: {resultado}")

        scrollbar.config(command=history_listbox.yview)

    def __del__(self):
        self.db_connection.close()

Calculadora()

