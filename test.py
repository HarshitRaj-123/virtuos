import sqlite3

try:
    conn=sqlite3.connect("candidate.db")
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CANDIDATE (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENTNAME TEXT NOT NULL,
            COLLEGENAME TEXT NOT NULL,
            ROUND1MARKS REAL,
            ROUND2MARKS REAL,
            ROUND3MARKS REAL,
            TECHNICALROUNDMARKS REAL,
            TOTALMARKS REAL,
            RESULT TEXT,
            RANK INTEGER
        )
    """)
    conn.commit()
    while True:
        student_name=input("Enter Student Name: ").strip()
        if len(student_name)<=30 and student_name:
            break
        print("Try again")

    while True:
        college_name=input("Enter College Name: ").strip()
        if len(college_name)<=50 and college_name:
            break
        print("Try again")

    def get_marks(prompt, min_val, max_val):
        while True:
            try:
                val=float(input(prompt))
                if val<min_val or val>max_val:
                    raise ValueError
                return val
            except ValueError:
                print("Try again")

    r1=get_marks("Round1 Marks (0-10): ", 0,10)
    r2=get_marks("Round2 Marks (0-10): ", 0,10)
    r3=get_marks("Round3 Marks (0-10): ", 0,10)
    tech=get_marks("Technical Round Marks (0-20): ", 0,20)

    total= r1+r2+r3+tech
    if(total>=35 and r1>=6.5 and r2>=6.5 and r3>=6.5 and tech>=13):
        result="Selected"
    else:
        result="Rejected"

    cursor.execute("""
        INSERT INTO CANDIDATE
        (STUDENTNAME, COLLEGENAME, ROUND2MARKS, ROUND3MARKS, ROUND1MARKS, TECHNICALROUNDMARKS, TOTALMARKS, RESULT)
        VALUES(?,?,?,?,?,?,?,?)
    """,(student_name, college_name, r1, r2, r3, tech, total, result))
    conn.commit()

    cursor.execute("""
        SELECT ID, TOTALMARKS
        FROM CANDIDATE
        ORDER BY TOTALMARKS DESC
    """)
    rows=cursor.fetchall()

    rank=0
    prev_marks=None
    current_rank=0

    for row in rows:
        if row[1]!=prev_marks:
            current_rank+=1
        cursor.execute("UPDATE CANDIDATE SET RANK=? WHERE ID=?", (current_rank, row[0])
        )
        prev_marks=row[1]

    conn.commit()

    cursor.execute("""
        SELECT STUDENTNAME, COLLEGENAME, TOTALMARKS, RESULT, RANK
        FROM CANDIDATE
        ORDER BY RANK
    """)

    print("\n Student | College | Total | Result | Rank")
    print("-----------------------------------")
    for row in cursor.fetchall():
        print(row)

    conn.close()

except sqlite3.Error as e:
    print("Database Error: ", e)

