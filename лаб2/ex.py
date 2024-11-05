import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd


class DataAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Analyzer")

        # Создаем элементы интерфейса
        self.load_button = tk.Button(
            master, text="Загрузить файл", command=self.load_data
        )
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Место для данных
        self.data_frame = tk.Frame(master)
        self.data_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )  # Занимаем все доступное пространство

        # (Treeview) Просмотр данных в табличном виде
        self.data_tree = ttk.Treeview(
            self.data_frame, columns=(), show="headings", selectmode="browse"
        )
        self.data_tree.pack(fill=tk.BOTH, expand=True)

        # Полосы прокрутки для таблицы
        self.scrollbar_v = tk.Scrollbar(
            self.data_frame, orient="vertical", command=self.data_tree.yview
        )
        self.scrollbar_h = tk.Scrollbar(
            self.data_frame, orient="horizontal", command=self.data_tree.xview
        )
        self.data_tree.configure(
            yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set
        )
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        # Выбор столбца из списка
        self.column_label = tk.Label(master, text="Выберите столбец:")
        self.column_label.grid(row=2, column=0, padx=5, pady=5)

        self.column_combobox = ttk.Combobox(master, state="readonly")
        self.column_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Остальные элементы интерфейса
        self.filter_frame = tk.Frame(master)
        self.filter_frame.grid(row=3, column=0, padx=5, pady=5)

        self.filter_label = tk.Label(self.filter_frame, text="Значение для фильтрации:")
        self.filter_label.grid(row=0, column=0)

        self.filter_entry = tk.Entry(self.filter_frame)
        self.filter_entry.grid(row=0, column=1)

        self.filter_button = tk.Button(
            self.filter_frame, text="Фильтрация", command=self.filter_data
        )
        self.filter_button.grid(row=0, column=2)

        # Кнопки
        self.analysis_frame = tk.Frame(master)
        self.analysis_frame.grid(row=4, column=0, padx=5, pady=5)

        self.mean_button = tk.Button(
            self.analysis_frame, text="Среднее", command=self.calculate_mean
        )
        self.mean_button.grid(row=0, column=0)
        self.min_button = tk.Button(
            self.analysis_frame, text="Минимум", command=self.calculate_min
        )
        self.min_button.grid(row=0, column=1)

        self.max_button = tk.Button(
            self.analysis_frame, text="Максимум", command=self.calculate_max
        )
        self.max_button.grid(row=0, column=2)

        # Загрузка данных
        self.data = None

    def load_data(self):
        # Загружает файл CSV и отображает данные в таблице
        file_path = filedialog.askopenfilename(defaultextension=".csv")
        if file_path:
            self.data = pd.read_csv(file_path)
            self.data_tree["columns"] = list(self.data.columns)
            self.display_data()
            self.update_column_combobox()

    def display_data(self):
        # Отображаем данные в таблице
        self.data_tree.delete(*self.data_tree.get_children())
        for column in self.data.columns:
            self.data_tree.column(
                column, anchor=tk.CENTER, width=100
            )  # Установка ширины столбца
            self.data_tree.heading(column, text=column)
        for index, row in self.data.iterrows():
            self.data_tree.insert("", tk.END, values=list(row))

    def update_column_combobox(self):
        # Обновляем список столбцов в комбобоксе
        self.column_combobox["values"] = list(self.data.columns)

    def filter_data(self):
        # Фильтрация данных по введенному значению
        filter_value = self.filter_entry.get().lower()
        selected_column = self.column_combobox.get()
        if filter_value and selected_column:
            self.data[selected_column] = self.data[selected_column].str.lower()
            self.data = self.data[
                self.data[selected_column].notna()
                & (self.data[selected_column] == filter_value)
            ]
            self.display_data()
            self.update_column_combobox()

    def calculate_mean(self):
        # Подсчет среднего значения для выбранного столбца
        selected_column = self.column_combobox.get()
        if selected_column:
            mean_value = self.data[selected_column].mean()
            tk.messagebox.showinfo(
                "Среднее значение",
                f"Среднее значение в столбце {selected_column}: {mean_value}",
            )

    def calculate_min(self):
        # Вывод минимального значения в выбранном столбце
        selected_column = self.column_combobox.get()
        if selected_column:
            min_value = self.data[selected_column].min()
            tk.messagebox.showinfo(
                "Минимальное значение",
                f"Минимальное значение в столбце {selected_column}: {min_value}",
            )

    def calculate_max(self):
        # Вывод максимального значения в выбранном столбце
        selected_column = self.column_combobox.get()
        if selected_column:
            max_value = self.data[selected_column].max()
            tk.messagebox.showinfo(
                "Максимальное значение",
                f"Максимальное значение в столбце {selected_column}: {max_value}",
            )


root = tk.Tk()
# Устанавливаем минимальные размеры окна
root.geometry("800x600")
app = DataAnalyzerApp(root)

# Настраиваем размер колонок
root.grid_rowconfigure(1, weight=1)  # Расширяем область таблицы
root.grid_columnconfigure(0, weight=1)

root.mainloop()
