#!/usr/bin/env python3
import os
import getpass
import socket

def get_current_prompt():
    """Функция для формирования приглашения username@hostname:~$"""
    username = getpass.getuser()  # Получаем текущее имя пользователя
    hostname = socket.gethostname()  # Получаем имя хоста
    current_dir = "~"  # Для простоты всегда показываем ~, как в требовании
    return f"{username}@{hostname}:{current_dir}$ "

def parse_input(user_input):
    """Простейший парсер. Разделяет ввод на команду и список аргументов по пробелам."""
    parts = user_input.strip().split()
    if not parts:
        return None, []  # Если ввод пустой
    command = parts[0]
    args = parts[1:]
    return command, args

def main():
    print("Добро пожаловать в эмулятор командной строки. Для выхода введите 'exit'.")

    while True:
        # Получаем и отображаем приглашение
        prompt = get_current_prompt()
        user_input = input(prompt)

        # Парсим введенную строку
        command, args = parse_input(user_input)

        # Если ввод пустой, просто продолжаем цикл
        if command is None:
            continue

        # Обрабатываем команду exit
        if command == "exit":
            print("Выход из эмулятора.")
            break

        # Обрабатываем команду-заглушку ls
        elif command == "ls":
            print(f"Команда 'ls'. Аргументы: {args}")

        # Обрабатываем команду-заглушку cd
        elif command == "cd":
            print(f"Команда 'cd'. Аргументы: {args}")

        # Обрабатываем неизвестную команду
        else:
            print(f"Ошибка: неизвестная команда '{command}'.")

if __name__ == "__main__":
    main()