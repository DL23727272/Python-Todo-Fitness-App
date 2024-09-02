import uuid
import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rowena_lorrie"
        )
        self.cursor = self.connection.cursor()

    def add_todo(self, value):
        todo_id = str(uuid.uuid4())
        query = "INSERT INTO my_list (id, value) VALUES (%s, %s)"
        self.cursor.execute(query, (todo_id, value))
        self.connection.commit()
        return todo_id

    def update_todo(self, todo_id, new_value):
        query = "UPDATE my_list SET value = %s WHERE id = %s"
        self.cursor.execute(query, (new_value, todo_id))
        self.connection.commit()

    def delete_todo(self, todo_id):
        query = "DELETE FROM my_list WHERE id = %s"
        self.cursor.execute(query, (todo_id,))
        self.connection.commit()

    def get_all_todos(self):
        query = "SELECT * FROM my_list"
        self.cursor.execute(query)
        todos = []
        for row in self.cursor.fetchall():
            todos.append({"id": row[0], "value": row[1]})
        return todos
    
    def signup(self, username, password):
        try:
            insert_user_query = "INSERT INTO user(username, password) VALUES(%s, %s)"
            self.cursor.execute(insert_user_query, (username, password))
            self.connection.commit()
            return True
        except mysql.connector.IntegrityError:
            return False

        
    def check_user(self, username, password):
        check_user_query = "SELECT * FROM user WHERE username = %s AND password = %s"
        self.cursor.execute(check_user_query, (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

    def close_db_connection(self):
         self.con.close()
