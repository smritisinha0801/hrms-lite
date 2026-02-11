from flask import Flask
from flask_cors import CORS
from routes import api
from db import engine
from models import Base

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Ensure tables exist (safe for this assignment)
    Base.metadata.create_all(bind=engine)

    app.register_blueprint(api, url_prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    from config import Config
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

@app.get("/")
def home():
    return {"message": "HRMS Lite API is running. Use /api/health"}, 200
