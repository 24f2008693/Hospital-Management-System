from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    # Check if an admin already exists
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@hms.com",
            role="admin"
        )
        admin.set_password("admin123")  # Default password
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
    else:
        print("⚠️ Admin already exists!")
