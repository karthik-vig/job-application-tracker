import flask
from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update
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
            id = Column(Integer, primary_key=True, autoincrement=True)
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

    def addRow(self, jobInfo: dict):
        with Session(self.engine) as session:
            rowToInsert = self.JobTrackerTable(job = jobInfo['job'],
                                               company = jobInfo['company'],
                                               salary = jobInfo['salary'],
                                               location = jobInfo['location'],
                                               jobStartDate = jobInfo['jobStartDate'],
                                               jobApplicationClosingDate = jobInfo['jobApplicationClosingDate'],
                                               status = jobInfo['status'],
                                               notes = jobInfo['notes'],
                                               startJobTrackDate = func.current_date(),
                                               modifiedJobTrackDate = func.current_date())
            session.add(rowToInsert)
            session.commit()

    def deleteRow(self, id: int):
        with Session(self.engine) as session:
            rowToDelete = session.get(self.JobTrackerTable, id)
            session.delete(rowToDelete)
            session.commit()

    def updateRow(self, id: int, modificationValues: dict):
        with Session(self.engine) as session:
            session.execute( update(self.JobTrackerTable)
                            .where(self.JobTrackerTable.id == id)
                            .values(job = modificationValues['job'],
                                    company = modificationValues['company'],
                                    salary = modificationValues['salary'],
                                    location = modificationValues['location'],
                                    jobStartDate = modificationValues['jobStartDate'],
                                    jobApplicationClosingDate = modificationValues['jobApplicationClosingDate'],
                                    status = modificationValues['status'],
                                    notes = modificationValues['notes'],
                                    modifiedJobTrackDate = func.current_date())
                            )
            session.commit()

    def retreiveRows(self, id: int, searchFilters: dict) -> dict:
        pass


if __name__ == "__main__":
    pass