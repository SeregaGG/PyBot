import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBSession:
    def __init__(self, settings):
        self.connection = psycopg2.connect(user=settings['user'],
                                           password=settings['password'],
                                           host=settings['host'],
                                           port=settings['port'],
                                           database=settings['database'])

    def WriteUserMessage(self, tag, message):
        if message[0] != '!':
            cursor = self.connection.cursor()
            cursor.execute('''INSERT INTO users_messages (tag, message) VALUES(%s,%s)''', (tag, message))
            self.connection.commit()
            cursor.close()

    def GetUserMessage(self, tag):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users_messages WHERE tag = %s AND message <> \'!my_mess\'''', (tag,))
        records = cursor.fetchall()
        messages = []
        for row in records:
            messages.append(row[2])
        cursor.close()

        return messages

    def __del__(self):
        if self.connection:
            self.connection.close()
