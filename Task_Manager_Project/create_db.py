from app import db, app  # Import Flask app and SQLAlchemy db from app.py

# Flask app ke context ke andar tables create karna zaroori hai
with app.app_context():
    db.create_all()
    print("✅ Database and tables created successfully.")
