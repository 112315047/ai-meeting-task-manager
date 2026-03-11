from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from .routes import tasks
from . import database

def create_app():
    app = Flask(__name__)
    CORS(app)

    database.init_app(app)

    app.register_blueprint(tasks.bp)

    @app.route("/health")
    def health():
        return {"status": "healthy"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)