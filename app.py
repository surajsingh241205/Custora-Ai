import os
from flask import Flask
from config import Config
from extensions import db, login_manager
from dotenv import load_dotenv
load_dotenv()
print("Loaded Key:", os.getenv("GROQ_API_KEY"))
load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models AFTER initializing app
    from models.user import User

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app


app = create_app()

if __name__ == "__main__":
    # Use the PORT environment variable provided by Render, default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    # Must bind to 0.0.0.0 to be accessible on Render
    app.run(host="0.0.0.0", port=port)