from kivymd.app import MDApp
from kivy.lang import Builder
# Импортируем классы для создания диалогового окна
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from data_manager import DataManager


class CommunalApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dm = DataManager()
        # Добавляем свойство для хранения ссылки на диалоговое окно
        self.dialog = None

        # 🔥 ВАЖНО: создаём поля до загрузки kv-файла
        self.readings = self.dm.load_readings()
        self.tariffs = self.dm.load_tariffs()

    def build(self):
        return Builder.load_file("communal.kv")

    # --- Методы обновления данных ---
    def update_reading(self, key, value):
        self.readings[key] = value
        self.dm.save_readings(self.readings)

    def update_tariff(self, key, value):
        self.tariffs[key] = value
        self.dm.save_tariffs(self.tariffs)

    # --- Расчёт ---
    def calculate(self):
        print("Расчёт...")

        # Безопасное извлечение данных и преобразование в float
        try:
            cold_r = float(self.readings.get('cold', 0))
            hot_r = float(self.readings.get('hot', 0))
            elec_r = float(self.readings.get('electricity', 0))

            cold_t = float(self.tariffs.get('cold', 0))
            hot_t = float(self.tariffs.get('hot', 0))
            sewage_t = float(self.tariffs.get('sewage', 0))
            # Добавляем тариф на электричество, который мы добавим в kv-файле
            elec_t = float(self.tariffs.get('electricity', 0))

            # Логика расчетов
            cost_cold = cold_r * cold_t
            cost_hot = hot_r * hot_t
            # Водоотведение = (горячая + холодная) * тариф
            cost_sewage = (cold_r + hot_r) * sewage_t
            cost_elec = elec_r * elec_t
            total_cost = cost_cold + cost_hot + cost_sewage + cost_elec

            # Формируем текст для диалогового окна
            result_text = (
                f"Холодная вода: {cost_cold:.2f} ₽\n"
                f"Горячая вода: {cost_hot:.2f} ₽\n"
                f"Водоотведение: {cost_sewage:.2f} ₽\n"
                f"Электричество: {cost_elec:.2f} ₽\n"
                f"\n[b]ИТОГО: {total_cost:.2f} ₽[/b]"
            )
            title = "Результаты расчета"

        except ValueError:
            result_text = "Пожалуйста, введите корректные числовые значения во все поля."
            title = "Ошибка ввода"

        # Отображаем результаты в MDDialog
        self.show_results_dialog(title, result_text)

    def show_results_dialog(self, title, text):
        # Если диалог уже существует, закрываем его перед созданием нового
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[],
        )
        # Устанавливаем markup=True для поддержки жирного шрифта [b][/b] в тексте
        self.dialog.text_color = self.theme_cls.text_color
        self.dialog.auto_dismiss = False # Не закрывать по клику вне окна
        self.dialog.open()

    def dismiss_dialog(self, *args):
        # Метод для закрытия диалогового окна при нажатии кнопки "ОК"
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None


if __name__ == "__main__":
    CommunalApp().run()
