from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import extras

app = Flask(__name__)
CORS(app)

# ── Database Configuration ──────────────────────────────────────────────────
# Ensure these match your local PostgreSQL setup exactly!
DB_CONFIG = {
    "host": "localhost",
    "database": "airplane_db",
    "user": "postgres",
    "password": "1234"  # <--- Change this to your PG password
}

def get_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)

# ── POST /add  →  Insert a new ticket ───────────────────────────────────────
@app.route("/add", methods=["POST"])
def add_ticket():
    try:
        data = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO ticket (booking_date, class, fare) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data["booking_date"], data["class"], data["fare"]))
        
        conn.commit()
        return jsonify({"message": "Ticket booked successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# ── GET /tickets  →  Fetch all tickets ──────────────────────────────────────
@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        conn = get_connection()
        # RealDictCursor allows us to return data as a dictionary (JSON-friendly)
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        
        # Mapping ticket_no to 'id' to match your frontend JS
        cursor.execute("SELECT ticket_no as id, booking_date, class, fare FROM ticket ORDER BY ticket_no DESC")
        tickets = cursor.fetchall()
        
        # PostgreSQL DATE and DECIMAL types need to be strings/floats for JSON
        for t in tickets:
            t['booking_date'] = str(t['booking_date'])
            t['fare'] = float(t['fare'])
            
        return jsonify(tickets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# ── PUT /update/<id>  →  Update class and fare ──────────────────────────────
@app.route("/update/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    try:
        data = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "UPDATE ticket SET class = %s, fare = %s WHERE ticket_no = %s"
        cursor.execute(sql, (data["class"], data["fare"], ticket_id))
        
        conn.commit()
        return jsonify({"message": f"Ticket {ticket_id} updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# ── DELETE /delete/<id>  →  Delete a ticket ─────────────────────────────────
@app.route("/delete/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM ticket WHERE ticket_no = %s", (ticket_id,))
        conn.commit()
        
        return jsonify({"message": f"Ticket {ticket_id} cancelled successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# ── Start Server ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("✈️ Backend is live at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)