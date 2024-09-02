'''
sqlite3 database for the todolist
'''
import sqlite3 as sq

from datetime import datetime


def create_table():
    connection = sq.connect("tasklist.db")

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            date_created TEXT,
            date_due TEXT, 
            completed_status INTEGER
            )""")
    
    connection.commit()
    connection.close()
    
def create_task(task):
    bool_value = 0
    date_created = datetime.now().strftime("%m-%d-%y %I:%M %p")
    date_due = datetime.now().strftime("%m-%d-%y %I:%M %p")

    connection = sq.connect("tasklist.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO tasks (task_name, date_created, date_due, completed_status) VALUES (?,?,?,?)", (task, date_created, date_due, bool_value))
    connection.commit()
    connection.close()


def delete_task(task_name):
    connection = sq.connect("tasklist.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE task_name = (?)",(task_name,))

    connection.commit()
    connection.close()

def mark_task(task_name, bool):
    connection = sq.connect("tasklist.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE tasks SET completed_status = (?) WHERE task_name = (?)",(bool,task_name))

    connection.commit()
    connection.close()

def list_tasks():
    connection = sq.connect("tasklist.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)

    connection.commit()
    connection.close()
    return tasks