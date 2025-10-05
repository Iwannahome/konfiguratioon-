#!/usr/bin/env python3
import os
import getpass
import socket
import argparse
import sys

class ShellEmulator:
    def __init__(self, vfs_path=None, startup_script=None):
        """Инициализация эмулятора с параметрами конфигурации"""
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        self.current_dir = "~"
        
        # Отладочный вывод параметров (требование этапа)
        print("=== ДЕБАГ: Параметры конфигурации ===")
        print(f"Путь к VFS: {self.vfs_path or 'Не указан'}")
        print(f"Стартовый скрипт: {self.startup_script or 'Не указан'}")
        print("=====================================")

    def get_current_prompt(self):
        """Формирование приглашения username@hostname:~$"""
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}@{hostname}:{self.current_dir}$ "

    def parse_input(self, user_input):
        """Парсер входной строки"""
        parts = user_input.strip().split()
        if not parts:
            return None, []
        command = parts[0]
        args = parts[1:]
        return command, args

    def execute_startup_script(self):
        """Выполнение стартового скрипта"""
        if not self.startup_script:
            return
        
        print(f"\n=== Выполнение стартового скрипта: {self.startup_script} ===")
        
        try:
            with open(self.startup_script, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"ОШИБКА: Скрипт '{self.startup_script}' не найден!")
            return
        except Exception as e:
            print(f"ОШИБКА: Не удалось прочитать скрипт: {e}")
            return

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # Пропускаем пустые строки
                continue
                
            print(f"\n[{line_num}] {line}")  # Показываем ввод
            command, args = self.parse_input(line)
            
            if command is None:
                continue
                
            # Выполняем команду (имитируем выполнение)
            if command == "exit":
                print("Команда exit проигнорирована в скрипте")
            elif command == "ls":
                print(f"Команда 'ls'. Аргументы: {args}")
            elif command == "cd":
                print(f"Команда 'cd'. Аргументы: {args}")
            else:
                print(f"ОШИБКА: Неизвестная команда '{command}' - строка пропущена")

        print("=== Завершение выполнения стартового скрипта ===\n")

    def run_interactive(self):
        """Запуск интерактивного режима"""
        # Сначала выполняем стартовый скрипт
        self.execute_startup_script()
        
        print("Добро пожаловать в эмулятор командной строки. Для выхода введите 'exit'.")

        while True:
            prompt = self.get_current_prompt()
            try:
                user_input = input(prompt)
            except KeyboardInterrupt:
                print("\nВыход из эмулятора.")
                break
            except EOFError:
                print("\nВыход из эмулятора.")
                break

            command, args = self.parse_input(user_input)

            if command is None:
                continue

            if command == "exit":
                print("Выход из эмулятора.")
                break
            elif command == "ls":
                print(f"Команда 'ls'. Аргументы: {args}")
            elif command == "cd":
                print(f"Команда 'cd'. Аргументы: {args}")
            else:
                print(f"Ошибка: неизвестная команда '{command}'.")

def main():
    """Основная функция с парсингом аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Эмулятор командной строки ОС')
    
    # Добавляем аргументы командной строки
    parser.add_argument('--vfs', type=str, help='Путь к физическому расположению VFS')
    parser.add_argument('--script', type=str, help='Путь к стартовому скрипту')
    
    # Парсим аргументы
    args = parser.parse_args()
    
    # Создаем и запускаем эмулятор
    emulator = ShellEmulator(vfs_path=args.vfs, startup_script=args.script)
    emulator.run_interactive()

if __name__ == "__main__":
    main()