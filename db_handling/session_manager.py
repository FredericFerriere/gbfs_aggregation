from pathlib import Path
from sqlmodel import Session, create_engine


def initialise_engine():
    full_path = "sqlite:///" + str(Path.cwd().parent) + "\\sql_db\\gbfs.db"
    engine = create_engine(full_path)
    return engine


class SessionManager:
    engine = initialise_engine()

    @staticmethod
    def create_session():
        return Session(SessionManager.engine)
