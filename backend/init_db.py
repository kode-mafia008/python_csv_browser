"""
Database initialization script
Creates database tables and seeds an admin user
"""
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def init_db():
    """Initialize database with tables and admin user"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()

        if not admin:
            print("Creating admin user...")
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created")
            print("  Username: admin")
            print("  Password: admin123")
        else:
            print("✓ Admin user already exists")

    finally:
        db.close()

    print("\n✓ Database initialization complete!")


if __name__ == "__main__":
    init_db()
