import sqlite3

users = [
    ("Никита", 2203.21),
    ("Андрей", 213.44),
    ("Михаил", 88452.222),
    ("Олег", 983.64),
]
cars = [
    (1, "bmv", 223.21),
    (1, "lada", 10.1),
    (3, "audi", 100.19),
    (2, "lexus", 1023.0),
    (3, "honda", 53.99),
    (4, "honday", 1000.1),
    (2, "bmv", 223.21),
]

# city = [
#     ( , , ),
# ]

with sqlite3.connect("test.db") as con:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.executescript("""
    PRAGMA foreign_keys=on;
    create table if not exists users(
    id integer primary key autoincrement,
    name text,
    money real
    );
    create table if not exists cars(
    user_id integer,
    model text,
    price real,
    foreign key(user_id) references users(id) on delete cascade
    );
    create table if not exists houses(
    user_id integer,
    city text,
    price real,
    foreign key(user_id) references users(id) on delete cascade
    )
    """)
    # cur.executemany("""
    # insert into users values(NULL, ?, ?)
    # """, users)
    # cur.executemany("""
    # insert into cars values(?, ?, ?)
    # """, cars)
    # cur.execute("""
    # select * from users
    # """)
    # for i in cur:
    #     print(i)


    
