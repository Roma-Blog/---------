import sqlite3, config


def create_table_project():
    connection = sqlite3.connect(config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Projects (
    id INTEGER PRIMARY KEY,
    name_projects TEXT NOT NULL,
    name_manager TEXT NOT NULL,
    user_id INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def set_project_all():
    connection = sqlite3.connect(config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT name_projects FROM Projects
    ''')

    result: list = []

    for row in cursor.fetchall():
        result.append(row[0])

    connection.commit()
    connection.close()

    return result

def set_users_list():
    connection = sqlite3.connect(config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT DISTINCT user_id FROM Projects
    ''')

    result: dict = {}

    for row in cursor.fetchall():
        result[row[0]] = {}

    connection.commit()
    connection.close()

    return result

def ser_user(name_projects):
    connection = sqlite3.connect(config.DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT DISTINCT user_id FROM Projects WHERE name_projects = ?
    ''', (name_projects,))

    result = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return result
