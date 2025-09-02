import logging

from sqlmodel import Session, SQLModel

from db_handling.session_manager import SessionManager

logger = logging.getLogger(__name__)


def create_db_and_tables():
    SQLModel.metadata.create_all(SessionManager.engine)


def add_record(session: Session, record: SQLModel):
    # TO DO: add multiple records version
    try:
        session.add(record)
        session.commit()
        session.refresh(record)
    except Exception as error:
        logger.log(level=logging.INFO, msg="DB update error", exc_info=True)
    return
