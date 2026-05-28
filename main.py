from fastapi import FastAPI
import mysql.connector


app = FastAPI()



def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="",
        port="",
    )

@app.on_event("startup")
def startup():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense_tracker(
        id INT AUTO_INCREMENT PRIMARY KEY,
        expense_title VARCHAR(200),
        expense_amount FLOAT,
        expense_category VARCHAR(100),
        payment_type VARCHAR(100),
        expense_created_date DATE,
        expense_description TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Expense Tracker API Running"}

# ===================== ADD =====================
@app.post("/add_expense")
def add_expense(payload: dict):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expense_tracker(
        expense_title,
        expense_amount,
        expense_category,
        payment_type,
        expense_created_date,
        expense_description
    )
    VALUES(%s,%s,%s,%s,%s,%s)
    """, (
        payload["expense_title"],
        payload["expense_amount"],
        payload["expense_category"],
        payload["payment_type"],
        payload["expense_created_date"],
        payload["expense_description"]
    ))

    conn.commit()
    conn.close()

    return {"message": "Expense Added"}

# ===================== VIEW =====================
@app.get("/get_expenses")
def get_expenses():

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expense_tracker ORDER BY id DESC")

    data = cursor.fetchall()

    conn.close()

    return {"expenses": data}

# ===================== SINGLE =====================
@app.get("/get_expense/{id}")
def get_expense(id: int):

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expense_tracker WHERE id=%s", (id,))
    data = cursor.fetchone()

    conn.close()

    return {"expense": data}

# ===================== UPDATE =====================
@app.put("/update_expense/{id}")
def update_expense(id: int, payload: dict):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expense_tracker
    SET expense_title=%s,
        expense_amount=%s,
        expense_category=%s,
        payment_type=%s,
        expense_created_date=%s,
        expense_description=%s
    WHERE id=%s
    """, (
        payload["expense_title"],
        payload["expense_amount"],
        payload["expense_category"],
        payload["payment_type"],
        payload["expense_created_date"],
        payload["expense_description"],
        id
    ))

    conn.commit()
    conn.close()

    return {"message": "Expense Updated"}

# ===================== DELETE =====================
@app.delete("/delete_expense/{id}")
def delete_expense(id: int):

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expense_tracker WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return {"message": "Expense Deleted"}

# ===================== ANALYSIS =====================
@app.get("/summary")
def summary():

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT expense_category, SUM(expense_amount) as total
    FROM expense_tracker
    GROUP BY expense_category
    """)

    data = cursor.fetchall()

    conn.close()

    return {"summary": data}
