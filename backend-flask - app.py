from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "helmet_sales")
    )


@app.route("/api/helmets")
def get_helmets():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, price, image_url FROM helmets"
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)


@app.route("/api/contact", methods=["POST"])
def save_contact():

    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    message = data.get("message")

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO contacts(name, phone, message)
        VALUES (%s, %s, %s)
        """,
        (name, phone, message)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Contact submitted successfully"
    })


@app.route("/api/health")
def health():

    return jsonify({
        "status": "Backend is running"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
