from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "contacts.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # rows を dict風に扱える
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # 最低限のサーバ側チェック
        if username and email and message:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO contacts (username, email, message, created_at) VALUES (?, ?, ?, ?)",
                (username, email, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()

            return redirect(url_for("list_contacts"))

    # GET or 入力不足の場合はフォーム表示
    return render_template("index.html", submitted=False, username="", email="", message="")


@app.route("/list")
def list_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("list.html", rows=rows)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        message = request.form.get("message")

        cur.execute(
            "UPDATE contacts SET username=?, email=?, message=? WHERE id=?",
            (username, email, message, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("list_contacts"))

    # GET（編集画面表示）
    cur.execute("SELECT * FROM contacts WHERE id=?", (id,))
    row = cur.fetchone()
    conn.close()
    return render_template("edit.html", row=row)
    
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("list_contacts"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

# first commit test
# second commit test222222

