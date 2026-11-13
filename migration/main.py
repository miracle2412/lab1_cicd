from alembic import command
from alembic.config import Config


def run_migrations():
    print("Starting database migrations...")

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    print("Database migrations completed successfully.")


if __name__ == "__main__":
    run_migrations()