# 1. Возможность ввода:
#  1.1 Названия расхода
#  1.2 Потраченной суммы денег
#  1.3 Причисление расхода к конкретной группе расходов (транспорт, еда, жилье и т.д.)
# 2. Отслеживание даты и времени введенного расхода
# 3. Хранение вышеперечисленной информации в базе данных и группировка по датам и группам

import sqlite3
import argparse

from argparse import ArgumentParser

def create_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   amount REAL, 
                   category TEXT,
                   date DATE)
                   ''')
    conn.commit()
    conn.close()


#Внесение расходов (пока через командную строку)
def add_expense(name, amount, category, date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)", (name, amount, category, date))
    conn.commit()
    conn.close()

#Расходы по датам(от и до)
def view_expenses_by_date(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date", (start_date, end_date))
    expenses = cursor.fetchall()

    conn.close()

    if expenses:
        print('Расходы по датам:')
        for expense in expenses:
            print(f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Категория: {expense[3]}, Дата: {expense[4]}")
    else:
        print("Нет расходов в указанный период")

#Расходы по категориям
def view_expenses_by_category(category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE category=? ORDER BY date", (category,))
    expenses = cursor.fetchall()

    conn.close()

    if expenses:
        print(f"Расходы в категории '{category}':")
        for expense in expenses:
            print(f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Дата: {expense[4]}")
    else:
        print(f"Нет расходов в категории '{category}'.")

#Просмотр всех расходов в базе данных
def view_all_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    conn.close()

    for expense in expenses: 
        print(f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Категория: {expense[3]}, Дата: {expense[4]}")

def view_sum_by_date(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
    total = cursor.fetchone()[0]

    print(f"Сумма всех расходов за указанный период: {total}")

#Запуск
if __name__ == '__main__':
    create_database()

    parser = ArgumentParser(description="Управление расходами")
    subparsers = parser.add_subparsers(dest = "command")

    #Сабпарсер для добавления расходов
    add_parser = subparsers.add_parser("add", help='Добавить расход')
    add_parser.add_argument("--name", required=True, help='Название расхода')
    add_parser.add_argument("--amount", required=True, type=int, help='Сумма расхода')
    add_parser.add_argument("--category", required=True, help='Категория расхода')
    add_parser.add_argument("--date", required=True, help='Дата расхода в формате ГГГГ-ММ-ДД')

    #Сабпарсеры для просмотра расходов по датам
    view_date_parser = subparsers.add_parser("view_by_date", help='Просмотр расходов по датам')
    view_date_parser.add_argument("--start_date", required=True)
    view_date_parser.add_argument("--end_date", required=True)

    #Сабпарсер для просмотра расходов в категории
    view_category_parser = subparsers.add_parser("view_by_category", help='Просмотр расходов по категориям')
    view_category_parser.add_argument("--category", required=True)
    
    #Сабпарсер для просмотра всей базы данных
    view_all_expenses_parser = subparsers.add_parser("view_all_expenses")

    #Сабпарсер для суммы всех расходов в заданный период
    view_sum_by_date_parser = subparsers.add_parser("view_sum_by_date")
    view_sum_by_date_parser.add_argument("--start_date", required=True)
    view_sum_by_date_parser.add_argument("--end_date", required=True)
    
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.name, args.amount, args.category, args.date)
    elif args.command == "view_by_date":
        view_expenses_by_date(args.start_date, args.end_date)
    elif args.command == "view_by_category":
        view_expenses_by_category(args.category)
    elif args.command == "view_all_expenses":
        view_all_expenses()
    elif args.command == "view_sum_by_date":
        view_sum_by_date(args.start_date, args.end_date)
