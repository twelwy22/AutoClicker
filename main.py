import os
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import threading
import time
from config import Config


# Функция для очистки консоли
def clear_console():
    """Очищает консоль в зависимости от операционной системы."""
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux и macOS
        os.system('clear')

# Управление мышью
mouse = Controller()
clicking = False  # Флаг для работы автокликера

def clicker():
    """Функция автокликера."""
    global clicking
    while True:
        if clicking:
            mouse.click(Button.left)  # Левый клик мыши
        time.sleep(Config.CLICK_DELAY)

def on_press(key):
    """Обработка нажатий клавиш."""
    global clicking
    if hasattr(key, 'char') and key.char:  # Проверка, что key имеет атрибут 'char'
        key_pressed = key.char.lower()  # Получаем символ и делаем его в нижнем регистре
    else:
        key_pressed = str(key).lower()  # Если это не символ, то берем строковое представление
    if key_pressed == Config.KEYBOARD_START:
        clicking = not clicking  # Переключение состояния автокликера
        clear_console()  # Очищаем консоль
        if clicking:
            print(f"""
=====================================================
🔗 Скрипт успешно запущен
=====================================================
🤖 Используемая задержка: {Config.CLICK_DELAY}
🔎 Клавиша для запуска скрипта: {Config.KEYBOARD_START}
🔎 Клавиша для остановки скрипта: {Config.KEYBOARD_STOP}
📅 Дата запуска: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}
=====================================================
👤 Владелец: {Config.OWNER}
🔗 Ссылка: {Config.OWNER_LINK}
=====================================================
""")
        else:
            print("Скрипт остановлен.")
    elif key_pressed == Config.KEYBOARD_STOP:
        print("Скрипт завершён.")
        listener.stop()
        exit()

# Приветствие
clear_console()  # Очищаем консоль при запуске
print(f"Нажмите клавишу {Config.KEYBOARD_START.upper()} для старта скрипта.")

# Запуск автокликера в отдельном потоке
click_thread = threading.Thread(target=clicker)
click_thread.daemon = True
click_thread.start()

# Прослушивание клавиатуры
with Listener(on_press=on_press) as listener:
    listener.join()
