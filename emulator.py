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

    def execute_command(self, command, args):
        """Выполнение одной команды"""
        if command == "exit":
            return "exit"
        elif command == "ls":
            print(f"Команда 'ls'. Аргументы: {args}")
            return True
        elif command == "cd":
            print(f"Команда 'cd'. Аргументы: {args}")
            return True
        else:
            print(f"ОШИБКА: Неизвестная команда '{command}' - строка пропущена")
            return False

    def execute_script(self, script_path):
        """Выполняет команды из скрипт-файла с поддержкой комментариев"""
        try:
            if not os.path.exists(script_path):
                print(f"ОШИБКА: Скрипт {script_path} не найден")
                return
            
            print(f"\n=== Выполнение стартового скрипта: {script_path} ===\n")
            
            with open(script_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line:
                    print(f"[{i}] (пустая строка)")
                    continue
                
                if line.startswith('#'):
                    print(f"[{i}] {line}")
                    print("# Комментарий пропущен")
                    continue
                
                print(f"[{i}] {line}")
                
                # Разбиваем на команду и аргументы
                parts = line.split()
                if not parts:
                    continue
                    
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                # Выполняем команду
                success = self.execute_command(command, args)
                
                if not success:
                    print(f"ОШИБКА: Не удалось выполнить команду '{command}' - строка пропущена")
            
            print("\n=== Завершение выполнения стартового скрипта ===")
            
        except Exception as e:
            print(f"ОШИБКА во время исполнения скрипта: {str(e)}")

    def execute_startup_script(self):
        """Выполняет стартовый скрипт если он указан"""
        if self.startup_script:
            self.execute_script(self.startup_script)

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

            result = self.execute_command(command, args)
            if result == "exit":
                print("Выход из эмулятора.")
                break

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