import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class PhotoTemplateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчёт стоимости фотошаблонов")
        self.root.state('zoomed')
        self.db_connection = sqlite3.connect('phototemplates.db')

        self.selected_technology = tk.StringVar()
        self.selected_templates = []
        self.exchange_rate = tk.DoubleVar(value=self.get_current_rate())
        self.create_widgets()

    def get_current_rate(self):
        return 11

    def validate_exchange_rate(self):
        try:
            rate_str = self.exchange_rate.get()
            if not rate_str:
                messagebox.showerror("Ошибка", "Поле курса не может быть пустым")
                self.exchange_rate.set(self.get_current_rate())
                return False

            rate = float(rate_str)
            if rate <= 0:
                messagebox.showerror("Ошибка", "Курс должен быть положительным числом")
                self.exchange_rate.set(self.get_current_rate())
                return False
            return True
        except (ValueError, tk.TclError):
            messagebox.showerror("Ошибка", "Введите корректное число для курса")
            self.exchange_rate.set(self.get_current_rate())
            return False

    def get_technologies(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM technologies")
        return [row[0] for row in cursor.fetchall()]

    def get_templates_for_technology(self, tech_name):
        cursor = self.db_connection.cursor()
        cursor.execute('''
        SELECT t.template_number, t.route, t.mikron_group
        FROM templates t
        JOIN technologies tech ON t.tech_id = tech.id
        WHERE tech.name = ?
        ORDER BY t.template_number
        ''', (tech_name,))
        return cursor.fetchall()

    def get_factory_group(self, mikron_group, factory):
        cursor = self.db_connection.cursor()
        if factory == "Фабрика №1":
            column = "factory1_group"
        else:
            column = "factory2_group"

        cursor.execute(f'''
        SELECT {column} 
        FROM quality_mapping
        WHERE mikron_group = ?
        ''', (mikron_group,))
        result = cursor.fetchone()
        return result[0] if result and result[0] != '-' else None

    def get_factory_price(self, factory_name, group_name):
        if not group_name:
            return None

        cursor = self.db_connection.cursor()
        cursor.execute('''
        SELECT price 
        FROM factory_prices
        WHERE factory_name = ? AND group_name = ?
        ''', (factory_name, group_name))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_historical_rates(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
        SELECT description, rate_value 
        FROM exchange_rates
        ORDER BY rate_date
        ''')
        return cursor.fetchall()

    def create_widgets(self):
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(left_frame, text="Выберите технологию:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tech_combobox = ttk.Combobox(left_frame, textvariable=self.selected_technology,
                                     values=self.get_technologies())
        tech_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tech_combobox.bind("<<ComboboxSelected>>", self.update_templates_list)

        self.templates_frame = ttk.LabelFrame(left_frame, text="Выберите шаблоны (№ФШ - Маршрут)")
        self.templates_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.columnconfigure(1, weight=1)
        self.canvas = tk.Canvas(self.templates_frame)
        self.scrollbar = ttk.Scrollbar(self.templates_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        ttk.Label(left_frame, text="Курс УЕ к рублю:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        rate_entry = ttk.Entry(left_frame, textvariable=self.exchange_rate)
        rate_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        rate_entry.bind("<FocusOut>", lambda e: self.validate_exchange_rate())

        ttk.Button(left_frame, text="Рассчитать стоимость", command=self.calculate_cost).grid(row=3, column=0,
                                                                                              columnspan=2, pady=10)

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.results_text = tk.Text(right_frame, state="disabled")
        self.results_text.pack(fill="both", expand=True)

    def update_templates_list(self, event=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        tech = self.selected_technology.get()
        if not tech:
            return
        templates = self.get_templates_for_technology(tech)
        self.selected_templates = []

        self.template_vars = {}
        for i, (template_number, route, _) in enumerate(templates):
            var = tk.BooleanVar(value=True)
            self.template_vars[(template_number, route)] = var
            cb = ttk.Checkbutton(
                self.scrollable_frame,
                text=f"{template_number} - {route}",
                variable=var,
                command=lambda v=var, t=template_number, r=route: self.toggle_template(v, t, r)
            )
            cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.selected_templates.append((template_number, route))

    def toggle_template(self, var, template_number, route):
        item = (template_number, route)
        if var.get():
            if item not in self.selected_templates:
                self.selected_templates.append(item)
        else:
            if item in self.selected_templates:
                self.selected_templates.remove(item)

    def calculate_cost(self):
        if not self.validate_exchange_rate():
            return

        tech = self.selected_technology.get()
        if not tech:
            messagebox.showerror("Ошибка", "Выберите технологию!")
            return

        if not self.selected_templates:
            messagebox.showerror("Ошибка", "Выберите хотя бы один шаблон!")
            return

        templates = []
        cursor = self.db_connection.cursor()
        for template_number, route in self.selected_templates:
            cursor.execute('''
            SELECT t.template_number, t.route, t.mikron_group
            FROM templates t
            JOIN technologies tech ON t.tech_id = tech.id
            WHERE tech.name = ? AND t.template_number = ? AND t.route = ?
            ''', (tech, template_number, route))
            result = cursor.fetchone()
            if result:
                templates.append(result)

        results = {}
        price_per_item = {}
        unavailable_templates = {}

        for factory in ["Фабрика №1", "Фабрика №2"]:
            total = 0
            can_produce_something = False
            price_per_item[factory] = {}
            unavailable_templates[factory] = []

            for template in templates:
                template_number = template[0]
                mikron_group = template[2]
                factory_group = self.get_factory_group(mikron_group, factory)

                if not factory_group:
                    unavailable_templates[factory].append(template_number)
                    continue

                price = self.get_factory_price(factory, factory_group)
                if not price:
                    unavailable_templates[factory].append(template_number)
                    continue

                total += price
                can_produce_something = True
                price_per_item[factory][template_number] = price

            if can_produce_something:
                results[factory] = {
                    'total_cost': total,
                    'price_per_item': price_per_item[factory],
                    'unavailable_count': len(unavailable_templates[factory]),
                    'produced_count': len(price_per_item[factory])
                }
            else:
                results[factory] = None

        self.display_results(results, len(templates))

    def display_results(self, results, templates_count):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)

        rate = self.exchange_rate.get()

        self.results_text.insert(tk.END, "Результаты расчёта:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n")

        factory1_available = results["Фабрика №1"] is not None
        factory2_available = results["Фабрика №2"] is not None
        factory1_unavailable = 0 if not factory1_available else results["Фабрика №1"]['unavailable_count']
        factory2_unavailable = 0 if not factory2_available else results["Фабрика №2"]['unavailable_count']
        factory1_missing = factory1_unavailable > 0 and factory2_available and factory2_unavailable < factory1_unavailable

        for factory in ["Фабрика №1", "Фабрика №2"]:
            if results[factory] is not None:
                data = results[factory]
                rub_cost = data['total_cost'] * rate

                self.results_text.insert(tk.END, f"{factory}:\n")
                self.results_text.insert(tk.END,
                                         f"Может изготовить: {data['produced_count']} из {templates_count} шаблонов\n")
                self.results_text.insert(tk.END, f"Общая стоимость: {data['total_cost']} УЕ ({rub_cost:.2f} руб.)\n")

                if data['price_per_item']:
                    self.results_text.insert(tk.END, "Цены за 1 шт:\n")
                    for template, price in data['price_per_item'].items():
                        rub_price = price * rate
                        self.results_text.insert(tk.END, f"¥{template}: {price} УЕ ({rub_price:.2f} руб.)\n")

                if data['unavailable_count'] > 0:
                    self.results_text.insert(tk.END, f"\nНе может произвести: {data['unavailable_count']} шт\n")

                self.results_text.insert(tk.END, "\n")
            else:
                self.results_text.insert(tk.END,
                                         f"{factory}: не может произвести ни одного шаблона (0 из {templates_count})\n\n")

        self.results_text.insert(tk.END, "\nАналитические расчёты:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n")

        historical_rates = self.get_historical_rates()
        valid_factories = {k: v for k, v in results.items() if v is not None}

        if valid_factories:
            for factory, data in valid_factories.items():
                cost = data['total_cost']
                self.results_text.insert(tk.END, f"Для {factory} ({cost} УЕ):\n")
                for desc, historical_rate in historical_rates:
                    historical_cost = cost * historical_rate
                    self.results_text.insert(tk.END, f"{desc}: {historical_cost:.2f} руб.\n")
                self.results_text.insert(tk.END, "\n")

            if len(valid_factories) > 1:
                if factory1_missing:
                    best_factory = ("Фабрика №2", results["Фабрика №2"])
                    reason = " (Фабрика №1 не может произвести некоторые шаблоны)"
                else:
                    best_factory = min(valid_factories.items(), key=lambda x: x[1]['total_cost'])
                    reason = ""

                self.results_text.insert(tk.END, "Вывод:\n")
                self.results_text.insert(tk.END, "=" * 50 + "\n")
                self.results_text.insert(tk.END,
                                         f"Наиболее выгодная фабрика: {best_factory[0]} ({best_factory[1]['total_cost']} УЕ){reason}\n")
            elif factory2_available:
                self.results_text.insert(tk.END, "Вывод:\n")
                self.results_text.insert(tk.END, "=" * 50 + "\n")
                self.results_text.insert(tk.END,
                                         "Наиболее выгодная фабрика: Фабрика №2 (единственная доступная)\n")

        self.results_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoTemplateCalculator(root)
    root.mainloop()
