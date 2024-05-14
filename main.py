
import sqlite3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.core.window import Window
# Глобальные настройки
Window.clearcolor = (10, 1, 1, 1)
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

class MyApp(App):
    def build(self):
        self.language = "Русский"  # Изначально устанавливаем русский язык
        self.conn = sqlite3.connect('sirius.sqlite3')  # Подключение к базе данных SQLite
        self.cursor = self.conn.cursor()

        # Перед созданием top_panel:
        search_input = TextInput(hint_text="Введите термин", multiline=False, size_hint=(None, None), size=(400, 50))

        # Затем, создание top_panel и добавление search_input_container:
        top_panel = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, padding=[0, 0, 0, 10],
                              spacing=10)
        search_input_container = BoxLayout(size_hint=(None, None), width=400, height=50, pos_hint={'center_x': 0.5})
        search_input_container.add_widget(search_input)
        top_panel.add_widget(search_input_container)
        top_panel.add_widget(Label())  # Пустой виджет для центрирования

        # Остальные виджеты вашего приложения
        self.box = BoxLayout(orientation='vertical', padding=[1450, 50, 50, 800], spacing=3)
        self.Tariffs = Button(text='Тарифы', background_color=[.94, .45, .15, 1], background_normal='', bold=True,
                              italic=True)
        self.subscription_button = Button(text='О приложении', background_color=[.94, .45, .15, 1],
                                          background_normal='', bold=True, italic=True)
        self.language_button_russian = Button(text="Русский", background_color=[.94, .45, .15, 1], background_normal='',
                                              bold=True, italic=True, on_press=self.switch_language_russian)
        self.language_button_english = Button(text="English", background_color=[.94, .45, .15, 1], background_normal='',
                                              bold=True, italic=True, on_press=self.switch_language_english)

        self.box.add_widget(self.Tariffs)
        self.box.add_widget(self.subscription_button)
        self.box.add_widget(self.language_button_russian)
        self.box.add_widget(self.language_button_english)

        self.label = Label(text='Приветственный текст', size_hint=(.6, .6), font_size='25sp',
                           pos_hint={'center_x': .4, 'center_y': .3}, bold=True, italic=True, color=(0, 0, 0, 1))
        self.bl3 = BoxLayout(orientation='vertical', padding=[0, 300, 0, 0])
        self.bl3.add_widget(self.label)

        # Виджет, содержащий все элементы интерфейса
        box1 = AnchorLayout()
        box1.add_widget(self.box)
        box1.add_widget(self.bl3)

        return box1

    def switch_language_russian(self, instance):
        self.language = "Русский"
        self.subscription_button.text = "О приложении"
        self.Tariffs.text = "Тарифы"
        self.update_language()

    def switch_language_english(self, instance):
        self.language = "English"
        self.subscription_button.text = "About in app"
        self.Tariffs.text = "Tariffs"
        self.update_language()

    def update_language(self):
        self.language_button_russian.disabled = self.language == "Русский"
        self.language_button_english.disabled = self.language == "English"
        self.label.text = "Приветственный текст" if self.language == "Русский" else "Welcome Text"

    def search_term(self, instance):
        # Получение информации о столбцах таблицы
        self.cursor.execute("PRAGMA table_info(glossary)")
        columns = self.cursor.fetchall()
        term = instance.text
        if term:
            # Выполняем SQL-запрос для поиска термина во всех столбцах таблицы
            self.cursor.execute("""
                SELECT * FROM glossary 
                WHERE term_eng LIKE ? 
                    OR term_rus LIKE ? 
                    OR definition_rus LIKE ? 
                    OR definition_eng LIKE ? 
                    OR context_eng LIKE ? 
                    OR context_rus LIKE ?
            """, (f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
            results = self.cursor.fetchall()
            if results:
                # Если найдены результаты, выводим их
                definitions = "\n".join(
                    result[6] for result in results)  # Получаем определения терминов из 7-го столбца
                self.label.text = definitions
            else:
                self.label.text = "Термин не найден"

    def on_stop(self):
        # Закрытие соединения с базой данных при завершении приложения
        self.conn.close()

if __name__ == "__main__":
    MyApp().run()