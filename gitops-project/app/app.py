import os
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

NOM = os.environ.get("STUDENT_NOM", "Sy")
PRENOM = os.environ.get("STUDENT_PRENOM", "Aicha")
VERSION = os.environ.get("APP_VERSION", "dev")


@app.get("/")
def home():
    return jsonify(
        message=f"Bienvenue sur la plateforme GitOps de {PRENOM} {NOM}",
        version=VERSION,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200


@app.get("/readyz")
def readyz():
    return jsonify(status="ready"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
