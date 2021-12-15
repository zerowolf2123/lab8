import sqlite3
import datetime


def connect():
    con = None
    try:
        con = sqlite3.connect("bank.db")
    except sqlite3.Error as e:
        if con:
            con.rollback()
            disconnect(con)
        print(f"Ошибка соединения: {e}")
        return False
    finally:
        return con


def disconnect(con):
    con.close()


class Model(object):

    def __init__(self):
        con = connect()
        if con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys=on")
            cur.executescript("""
            create table if not exists users(
            id integer primary key autoincrement,
            first_name varchar(25) not null,
            last_name varchar (25) not null,
            age integer not null,
            sex boolean not null,
            money real default 0,
            data_create text not null
            );
            create table if not exists more_information(
            user_id integer not null,
            phone varchar(12),
            email varchar(255),
            data_add text not null,
            foreign key(user_id) references users(id) on delete cascade on update cascade
            );
            create table if not exists all_operations(
            user_id integer not null,
            type_oper varchar(50) not null,
            money real default 0,
            user_id_tran integer default null,
            data_oper text not null, 
            foreign key(user_id) references users(id) on delete cascade on update cascade 
            )""")
            con.commit()
            disconnect(con)

    def set_user(self, *args, **kwargs):
        con = connect()
        if con:
            cur = con.cursor()
            cur.execute("""
            insert into users values(
            NULL, ?, ?, ?, ?, ?, ?
            )
            """, (
                kwargs['first_name'],
                kwargs['last_name'],
                kwargs['age'],
                kwargs['sex'],
                kwargs['money'],
                datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
            ))
            last_id = cur.lastrowid
            cur.execute("""
            insert into more_information values (?, NULL, NULL, ?)
            """, (last_id, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")))
            con.commit()
            disconnect(con)

    def get_all_users(self):
        with sqlite3.connect("bank.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("""select * from users""")
            return cur.fetchall()

    def get_one_user(self, user_id):
        with sqlite3.connect("bank.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            try:
                cur.execute("""
                select * from users 
                where id = :User_id
                """, {"User_id": user_id})
                return dict(cur.fetchone())
            except:
                return "Пользователя с таким id нет"

    def update_one_user(self, **kwargs):
        with sqlite3.connect("bank.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("""select * from more_information
            where user_id=:User_id
            """, {"User_id": kwargs["user_id"]})
            if len(cur.fetchall()) == 1:
                cur.execute("""
                update more_information set phone=:Phone, email=:Email
                where user_id=:User_id
                """, {"Phone": kwargs["phone"], "Email": kwargs["email"], "User_id": kwargs["user_id"]})
            else:
                cur.execute("""
                insert into more_information values (?, ?, ?, ?)
                """, (
                    kwargs['user_id'],
                    kwargs['phone'],
                    kwargs['email'],
                    datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
                ))
            con.commit()

    def get_more_inform_one_user(self, user_id):
        with sqlite3.connect("bank.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("""
            select * from more_information
            where user_id=:User_id
            """, {"User_id": user_id})
            return cur.fetchall()

    def add_or_out_money(self, user_id, money, type_oper):
        con = connect()
        if con:
            cur = con.cursor()
            cur.execute("""
            insert into all_operations values(?, ?, ?, NULL, ?)
            """, (user_id, type_oper, money, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")))
            if type_oper == "replenishment":
                cur.execute("""
                update users set money = money + :Money
                where id = :User_id
                """, {"Money": money, "User_id": user_id})
            elif type_oper == "withdrawal":
                cur.execute("""
                update users set money = money - :Money
                where id = :User_id
                """, {"Money": money, "User_id": user_id})
            con.commit()
            disconnect(con)

    def trans_money(self, user_id, user_id_tran, money, type_oper):
        con = connect()
        if con:
            cur = con.cursor()
            cur.execute("""
                insert into all_operations values(?, ?, ?, ?, ?)
                """, (user_id, type_oper, money, user_id_tran, datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")))
            cur.execute("""
                update users set money = money - :Money
                where id = :User_id
                """, {"Money": money, "User_id": user_id})
            cur.execute("""
                update users set money = money + :Money
                where id = :User_id
                """, {"Money": money, "User_id": user_id_tran})
            con.commit()
            disconnect(con)

    def del_user(self, user_id=None):
        con = connect()
        if con:
            cur = con.cursor()
            if user_id:
                cur.execute("""
                delete from users 
                where id = :User_id
                """, {"User_id": user_id})
            else:
                cur.execute("""delete from users""")
            con.commit()
            disconnect(con)

    def del_last_entry(self):
        con = connect()
        if con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row
            cur.execute("""
            select count(rowid) as len_oper from all_operations
            """)
            len_oper = dict(cur.fetchone())["len_oper"]
            cur.execute("""
            delete from all_operations
            where rowid=:Len_oper
            """, {"Len_oper": len_oper})
            con.commit()
            disconnect(con)

    def del_all_entry_user(self, user_id=None):
        con = connect()
        if con:
            cur = con.cursor()
            if user_id:
                cur.execute("""
                delete from all_operations
                where user_id=:User_id
                """, {"User_id": user_id})
            else:
                cur.execute("""
                delete from all_operations
                """)
            con.commit()
            disconnect(con)

