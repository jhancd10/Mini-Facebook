import pymysql
from db_config import mysql
from datetime import date

class UsersRepository(object):
    def __init__(self):
        self.conn = mysql.connect()

    def login(self, username, password):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id AS id FROM user WHERE username=%s AND password=%s", (username, password))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_user_by_id(self, id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT email, name, username FROM user WHERE id=%s", id)
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_user_by_name(self, name):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT email, name, username FROM user WHERE name=%s", name)
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_all_users(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user")
        row = cursor.fetchall()
        cursor.close()
        return row

    def create_new_user(self, _email, _name, _password, _username):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO user(email, name, password, username) VALUES(%s,%s,%s,%s)",(_email, _name, _password, _username))
        #affectedRows = cursor.rowcount()
        row = cursor.fetchone()
        #affectedRows = row[0]
        cursor.close()
        #print(row)
        self.conn.commit()
        return row
    
    def count(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT count(id) as count FROM user")
        row = cursor.fetchone()
        cursor.close()
        return row

    def exist(self, id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT name FROM user WHERE id=%s", id)
        row = cursor.fetchone()
        value = True
        cursor.close()
        if row is None:
            value = False     
        return value

    def send_friend_request(self, id1, id2):
        row = None
        idExist1 = self.exist(id1)
        idExist2 = self.exist(id2)
        if idExist1 == True and idExist2 == True:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            actualDate = date.today()
            cursor.execute("INSERT INTO friend_requests(user_id_origin, user_id_target, status, create_date, update_date) VALUES(%s,%s,'sent',%s,%s)",(id1, id2, actualDate, actualDate))
            row = cursor.fetchone()
            cursor.close()
            self.conn.commit()
        else:
            row = False
        return row

    def findTargetID(self, id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_id_target FROM friend_requests WHERE user_id_origin=%s", id)
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_friend_request(self, idOrigin):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        #idTarget = self.findTargetID(idOrigin)
        cursor.execute("SELECT name, DATE(create_date) as fecha FROM friend_requests inner join user on(user_id_origin = user.id) WHERE user_id_target = %s", idOrigin)
        row = cursor.fetchall()
        cursor.close()
        return row

    def accept_reject_friend_request(self, id, idFriendRequest, status):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("UPDATE friend_requests SET status = %s WHERE user_id_origin=%s and user_id_target=%s", (status, idFriendRequest, id))
        row = cursor.fetchone()
        self.conn.commit()
        cursor.close()
        return 'ok'