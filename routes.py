from flask import Blueprint, jsonify, request
from database import get_db_connection

routes = Blueprint('routes', __name__)


## Test route
@routes.route('/', methods=['GET'])
def hello():
    return "Bienvenue dans mon API Flask CRUD"


## Ajouter personne
@routes.route('/people/person', methods=['POST'])
def add_person():
    data = request.get_json()

    if not data or not data.get('lname') or not data.get('fname'):
        return jsonify({"error": "lname et fname sont obligatoires"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO person (lname, fname, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)",
        (data['lname'], data['fname'])
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Personne ajoutée avec succès"}), 201

## Toutes les personnes

@routes.route('/people/person', methods=['GET'])
def get_people():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM person;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id": r[0], "lname": r[1], "fname": r[2], "timestamp": str(r[3])}
        for r in rows
    ])



## Une personne par ID
@routes.route('/people/person/<int:id>', methods=['GET'])
def get_person(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM person WHERE id = %s;", (id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Personne non trouvée"}), 404

    return jsonify({
        "id": row[0],
        "lname": row[1],
        "fname": row[2],
        "timestamp": str(row[3])
    })


## Modifier personne
@routes.route('/people/person/<int:id>', methods=['PUT'])
def update_person(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Données manquantes"}), 400

    lname = data.get('lname')
    fname = data.get('fname')

    conn = get_db_connection()
    cur = conn.cursor()

    # vérifier si la personne existe
    cur.execute("SELECT * FROM person WHERE id = %s;", (id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Personne non trouvée"}), 404

    # mise à jour
    cur.execute(
        "UPDATE person SET lname = %s, fname = %s WHERE id = %s",
        (lname, fname, id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Personne modifiée avec succès"}), 200


# =========================
# DELETE - Supprimer personne
# =========================
@routes.route('/people/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM person WHERE id = %s;", (id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Personne non trouvée"}), 404

    cur.execute("DELETE FROM person WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Personne supprimée"}), 200