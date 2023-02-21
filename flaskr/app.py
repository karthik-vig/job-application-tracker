import flask
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import Session, registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

class JobInfoTable(Base):
    __tablename__ = 'JobTrackerTable'
    id = Column(Integer, primary_key=True)
    job = Column(String(50))
    company = Column(String(100))
    salary = Column(Integer)
    location = Column(String(100))
    jobStartDate = Column(Date)
    jobApplicationClosingDate = Column(Date)
    status = Column(String(20))
    notes = Column(String(2000))
    startJobTrackDate = Column(Date)
    modifiedJobTrackDate = Column(Date)
    def __repr__(self):
        return f"Table recording all job tracking information"

class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///jobDatabase.db", echo=True, future=True)

    def addRow(self, JobInfo: dict):
        pass

    def deleteRow(self, id: int):
        pass

    def updateRow(self, id: int, columnValues: dict):
        pass

    def retreiveRows(self, id: int, searchFilters: dict) -> dict:
        pass


if __name__ == "__main__":
    pass