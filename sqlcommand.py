import sqlite3

from telegram import user


class DB():
    def __init__(self, databasename):
        self.conn = sqlite3.connect(databasename, check_same_thread=False)

    def table(self):
        cursor = self.conn.cursor()
        cursor.executescript(
            """CREATE TABLE IF NOT EXISTS users(
                    iduser INT NOT NULL PRIMARY KEY,
                    numfile INT NULL ,
                    sell );

                CREATE TABLE IF NOT EXISTS files(
                    name INT NOT NULL ,
                    fileid VARCHAR(1000),
                    filetype VARCHAR(20),
                    caption NVARCHAR(4000) );""")
        self.conn.commit()
        cursor.close()
    
    def insert_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT or IGNORE INTO users(iduser) VALUES(:user_id)", {"user_id":user_id})
        self.conn.commit()
        cursor.close()
    
    def update_user(self, user_id , toll):
        cursor = self.conn.cursor()
        cursor.execute("SELECT numfile FROM users WHERE iduser = :user_id", {"user_id": user_id })
        res = cursor.fetchone()
        if res[0] is not None:
            toll+=res[0]
        cursor.execute("""UPDATE users SET numfile =:toll WHERE iduser = :user_id """ , {"user_id": user_id , "toll": toll})
        self.conn.commit()
        cursor.close()
    
    def insert_file(self, name , file_id , file_type, caption):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO files(name , fileid , filetype , caption) VALUES(:name , :file_id , :file_type , :caption)"
        ,{"name": name , "file_id": file_id ,"file_type": file_type , "caption":caption})
        self.conn.commit()
        cursor.close()
    
    def search_with_name(name):
        cursor = self.conn.cursor()



        cursor.execute("SELECT fileid , filetype , caption FROM files LIMIT :num",{"num":num})
        file_info = cursor.fetchall()
        cursor.close()
        return file_info


    def get_file(self, num):
        cursor = self.conn.cursor()
        cursor.execute("SELECT fileid , filetype , caption FROM files LIMIT :num",{"num":num})
        file_info = cursor.fetchall()
        cursor.close()
        return file_info
    
    def get_users(self, user_id=0):
        cursor = self.conn.cursor()

        if user_id :
            cursor.execute("SELECT numfile FROM users WHERE iduser = :user_id", {"user_id":user_id})
            user_info = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM users")
            user_info = cursor.fetchall()

        cursor.close()  
        return user_info

    def get_file_number(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT  name, COUNT(fileid) FROM files GROUP BY name ")
        file_info = cursor.fetchall()
        return file_info

