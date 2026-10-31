import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db():
    conn = sqlite3.connect("posts.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    keyword = request.args.get("keyword", "")

    if request.method == "POST":
        image = request.files.get("image")
        filename = None

        if image and image.filename != "":
            filename = image.filename
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn.execute(
            """
            INSERT INTO posts (myname, email, message_main, image, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
            """,
            (
                request.form["myname"],
                request.form["email"],
                request.form["message"],
                filename
            )
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    if keyword:
        posts = conn.execute(
            """
            SELECT * FROM posts
            WHERE myname LIKE ? OR message_main LIKE ?
            ORDER BY created_at DESC
            """,
            (f"%{keyword}%", f"%{keyword}%")
        ).fetchall()
    else:
        posts = conn.execute(
            "SELECT * FROM posts ORDER BY created_at DESC"
        ).fetchall()

    conn.close()
    return render_template("index.html", posts=posts, keyword=keyword)

@app.route("/edit/<int:id>")
def edit(id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", post=post)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()

    myname = request.form["myname"]
    email = request.form["email"]
    message = request.form["message"]

    image = request.files.get("image")
    if image and image.filename != "":
        filename = image.filename
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    else:
        filename = post["image"]

    conn.execute(
        "UPDATE posts SET myname=?, email=?, message_main=?, image=? WHERE id=?",
        (myname, email, message, filename, id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/like/<int:id>", methods=["POST"])
def like(id):
    conn = get_db()
    conn.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
