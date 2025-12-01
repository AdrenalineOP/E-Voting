from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# Create SQLite engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


def create_db_and_tables():
    """
    Create all database tables
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for getting database sessions
    """
    with Session(engine) as session:
        yield session
