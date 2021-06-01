import pymysql
from contextlib import closing
from bot.settings import DATABASE, log


def execute_sql_command(command):
    with open('bot/secret_keys.txt', 'r') as file:
        password = file.readlines()[-1]
    try:
        with closing(pymysql.connect(**DATABASE, password=password)) as connection:
            with connection.cursor() as cursor:
                query = command
                cursor.execute(query)
                connection.commit()
        return cursor

    except RuntimeError:
        log.error('Incorrect db password')
        return 0
    except pymysql.err.OperationalError as error_msg:
        log.error(error_msg)
        return 0
    except pymysql.err.ProgrammingError as error_msg:
        log.error(error_msg)
        return 0


def show_users():
    cursor = execute_sql_command('SELECT id, user_id, is_active FROM users;')
    try:
        for row in cursor:
            print(f"id: {row['id']} - user id: {row['user_id']} - is active: {row['is_active']}")
    except TypeError:
        print(cursor)
        log.error(cursor)


def add_user(user_id):
    cursor = execute_sql_command(f'SELECT id FROM users WHERE user_id = {user_id};')
    # Если пользователь есть в БД, то пропускаем добавление, возвращаемый курсор должен быть больше 0
    for item in cursor:
        if len(item) > 0:
            return
    try:
        execute_sql_command(f"INSERT INTO users (user_id) VALUES ({user_id})")
    except pymysql.err.IntegrityError:
        log.error('Adding user to database failed')


def toggle_notifications(user_id):
    cursor = execute_sql_command(f'SELECT is_active FROM users WHERE user_id = {user_id};')
    for item in cursor:
        if item['is_active']:
            execute_sql_command(f'UPDATE users SET is_active = 0 WHERE user_id = {user_id};')
        else:
            execute_sql_command(f'UPDATE users SET is_active = 1 WHERE user_id = {user_id};')


if __name__ == '__main__':
    show_users()
