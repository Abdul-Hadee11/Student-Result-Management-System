import sqlite3
def create_db():
    con=sqlite3.connect(database="database_srms.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(C_ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, DURATION TEXT, CHARGES TEXT, DESCRIPTION TEXT)")
    con.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        roll_no INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        gender TEXT,
        dob TEXT,
        contact TEXT,
        admission TEXT,
        course TEXT,
        address TEXT
    )
""")
    con.commit()


    cur.execute("CREATE TABLE IF NOT EXISTS result(select_stud INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, course TEXT, marks TEXT, fullmarks TEXT)")
    con.commit()

    


    



    
    con.close()


create_db()