import flask
from sqlalchemy import create_engine, Column, Integer, String, Date, Table
from sqlalchemy.orm import Session, registry



class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///jobDatabase.db", echo=True, future=True)
        self.mapper_registry = registry()
        self.Base = self.mapper_registry.generate_base()
        if self.engine.dialect.has_table(self.engine, "JobTrackerTable"):
            self.JobTrackerTable = self.getTable()
        else:
            self.JobTrackerTable = self.createTable()

    def createTable(self):
        class JobTrackerTable(self.Base):
            __tablename__ = "JobTrackerTable"
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
        self.mapper_registry.metadata.create_all()
        return JobTrackerTable

    def getTable(self):
        class JobTrackerTable(self.Base):
            __table__ = Table("JobTrackerTable", 
                              self.mapper_registry.metadata, 
                              autoload_with=self.engine)
        return JobTrackerTable

    def addRow(self, JobInfo: dict):
        with Session(self.engine) as session:
            pass

    def deleteRow(self, id: int):
        pass

    def updateRow(self, id: int, columnValues: dict):
        pass

    def retreiveRows(self, id: int, searchFilters: dict) -> dict:
        pass


if __name__ == "__main__":
    pass