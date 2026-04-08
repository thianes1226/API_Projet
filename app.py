
from flask import Flask, jsonify, request
import psycopg2
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

## Fonction pour se connecter à la base de données
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sarr",
        user="postgres",
        password="thiane1226"
    )
## les routes de mon API
@app.route('/')
def hello():
    """
    Page d'accueil
    ---
    responses:
      200:
        description: API fonctionne
    """
    return "Hello, thiane ! bienvenue dans mon API Flask"

## recupérer toutes les personnes
@app.route('/people/person')
def get_people():
    """
    Récupérer toutes les personnes
    ---
    tags:
      - Personnes
    responses:
      200:
        description: Liste des personnes
    """
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


## recupérer une personne par ID
@app.route('/people/person/<int:id>')
def get_person(id):
    """
    Récupérer une personne par ID
    ---
    tags:
      - Personnes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la personne
    responses:
      200:
        description: Personne trouvée
      404:
        description: Personne non trouvée
    """
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


## ajouter une personne
@app.route('/people/person/add')
def add_person():
    """
    Ajouter une personne
    ---
    tags:
      - Personnes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            lname:
              type: string
              example: Sarr
            fname:
              type: string
              example: Ali
    responses:
      201:
        description: Personne ajoutée
    """
    data = request.get_json()
    lname = data.get('lname')
    fname = data.get('fname')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO person (lname, fname, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)",
        (lname, fname)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Person ajoutée avec succès"}), 201


## supprimer une personne
@app.route('/people/person/dellete/<int:id>')
def delete_person(id):
    """
    Supprimer une personne
    ---
    tags:
      - Personnes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Personne supprimée
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM person WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Person supprimée"}), 200


if __name__ == '__main__':
    app.run(debug=True)