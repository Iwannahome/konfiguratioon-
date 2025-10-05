#!/bin/bash

echo "=== Тестирование эмулятора ОС ==="
echo ""

echo "=== Тест 1: Запуск без параметров ==="
python3 emulator.py << EOF
ls
exit
EOF

echo -e "\n=== Тест 2: Запуск с VFS ==="
python3 emulator.py --vfs test_vfs/minimal.json << EOF
ls
exit
EOF

echo -e "\n=== Тест 3: Запуск со скриптом ==="
python3 emulator.py --script scripts/startup.txt

echo -e "\n=== Тест 4: Запуск с обоими параметрами ==="
python3 emulator.py --vfs test_vfs/complex.json --script scripts/startup.txt

echo -e "\n=== Тест 5: Ошибочный скрипт (должна быть ошибка) ==="
python3 emulator.py --script scripts/nonexistent.txt << EOF
exit
EOF

echo -e "\n=== Тестирование завершено ==="
