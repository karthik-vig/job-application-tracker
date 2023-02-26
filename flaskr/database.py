from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_
from sqlalchemy.orm import Session, registry
import datetime



class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///jobDatabase.db", echo=True, future=True)
        self.mapper_registry = registry()
        self.Base = self.mapper_registry.generate_base()
        with self.engine.connect() as databaseConnection:
            if self.engine.dialect.has_table(databaseConnection, "JobTrackerTable"):
                self.JobTrackerTable = self.getTable()
            else:
                self.JobTrackerTable = self.createTable()
            databaseConnection.commit()

    def createTable(self):
        class JobTrackerTable(self.Base):
            __tablename__ = "JobTrackerTable"
            id = Column(Integer, primary_key=True, autoincrement=True)
            job = Column(String(50))
            company = Column(String(100))
            salary = Column(Integer)
            jobLocation = Column(String(100))
            jobStartDate = Column(Date)
            jobApplicationClosingDate = Column(Date)
            applicationStatus = Column(String(20))
            notes = Column(String(10000))
            startJobTrackDate = Column(Date)
            modifiedJobTrackDate = Column(Date)
            def __repr__(self):
                return f"Table recording all job tracking information"
        self.mapper_registry.metadata.create_all(self.engine)
        return JobTrackerTable

    def getTable(self):
        class JobTrackerTable(self.Base):
            __table__ = Table("JobTrackerTable", 
                              self.mapper_registry.metadata, 
                              autoload_with=self.engine)
        return JobTrackerTable

    def addRow(self, jobInfo: dict):
        with Session(self.engine) as session:
            jobInfo['jobStartDate'] = self.strToDatetime(jobInfo['jobStartDate'])
            jobInfo['jobApplicationClosingDat'] = self.strToDatetime(jobInfo['jobApplicationClosingDat'])
            rowToInsert = self.JobTrackerTable(job = jobInfo['job'],
                                               company = jobInfo['company'],
                                               salary = jobInfo['salary'],
                                               jobLocation = jobInfo['jobLocation'],
                                               jobStartDate = jobInfo['jobStartDate'],
                                               jobApplicationClosingDate = jobInfo['jobApplicationClosingDate'],
                                               applicationStatus = jobInfo['applicationStatus'],
                                               notes = jobInfo['notes'],
                                               startJobTrackDate = func.current_date(),
                                               modifiedJobTrackDate = func.current_date())
            session.add(rowToInsert)
            session.commit()

    def strToDatetime(self, strDate: str):
        dateYYYYMMDD = list( map( int, strDate.split('-') ) )
        return datetime.date(dateYYYYMMDD[0], dateYYYYMMDD[1], dateYYYYMMDD[2])

    def deleteRow(self, id: int):
        with Session(self.engine) as session:
            queryRowToDelete = session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == id)
            rowToDelete = session.execute(queryRowToDelete).first()
            #session.delete(rowToDelete)
            session.delete(rowToDelete[0])
            session.commit()

    def updateRow(self, id: int, modificationValues: dict):
        with Session(self.engine) as session:
            session.execute( update(self.JobTrackerTable)
                            .where(self.JobTrackerTable.id == id)
                            .values(job = modificationValues['job'],
                                    company = modificationValues['company'],
                                    salary = modificationValues['salary'],
                                    jobLocation = modificationValues['jobLocation'],
                                    jobStartDate = modificationValues['jobStartDate'],
                                    jobApplicationClosingDate = modificationValues['jobApplicationClosingDate'],
                                    applicationStatus = modificationValues['applicationStatus'],
                                    notes = modificationValues['notes'],
                                    modifiedJobTrackDate = func.current_date())
                            )
            session.commit()

    def retrieveRows(self, searchFilters: dict) -> list:
        with Session(self.engine) as session:
            queryStatement = self.buildQueryStatement(searchFilters=searchFilters, session=session)
            rows = session.execute(queryStatement)
            rowList = self.convertRowsToPrimitive(rows)
        return rowList

    def buildQueryStatement(self, searchFilters: dict, session):
        queryStatement = session.query(self.JobTrackerTable).filter( or_( self.JobTrackerTable.job.like(f"%{searchFilters['searchText']}%"),
                                                     self.JobTrackerTable.company.like(f"%{searchFilters['searchText']}%") )
                                                   )                                           
        if searchFilters['salary']:
            queryStatement = queryStatement.filter(self.JobTrackerTable.salary >= searchFilters['salary']['min'],
                                                        self.JobTrackerTable.salary <= searchFilters['salary']['max']
                                                        )
            
        if searchFilters['jobStartDate']:
            queryStatement = queryStatement.filter(self.JobTrackerTable.jobStartDate >= searchFilters['jobStartDate'])
        if searchFilters['applicationStatus']:
            queryStatement = queryStatement.filter(self.JobTrackerTable.applicationStatus == searchFilters['applicationStatus'])
        if searchFilters['jobLocation']:
            queryStatement = queryStatement.filter(self.JobTrackerTable.jobLocation == searchFilters['jobLocation'])
        return queryStatement

    def convertRowsToPrimitive(self, rows):
        rowList = []
        for row in rows:
            row = row[0]
            rowList.append( {
                'id': row.id,
                'job': row.job,
                'company': row.company,
                'salary': row.salary,
                'jobLocation': row.jobLocation,
                'jobStartDate': row.jobStartDate,
                'jobApplicationClosingDate': row.jobApplicationClosingDate,
                'applicationStatus': row.applicationStatus,
                'notes': row.notes,
                'startJobTrackDate': row.startJobTrackDate,
                'modifiedJobTrackDate': row.modifiedJobTrackDate
            } )
        return rowList

    def getSearchFilterLimits(self) -> dict:
        searchFilterLimits = {"salaryMin": None,
                              "salaryMax": None,
                              "allJobLocations": []
                              }
        minSalarySelectStatement = select(func.min(self.JobTrackerTable.salary)).scalar_subquery()
        maxSalarySelectStatement = select(func.max(self.JobTrackerTable.salary)).scalar_subquery()
        allJobLocationsSelectStatement = select(self.JobTrackerTable.jobLocation).distinct()
        with Session(self.engine) as session:
            searchFilterLimits['salaryMin'] = session.execute(minSalarySelectStatement)
            searchFilterLimits['salaryMax'] = session.execute(maxSalarySelectStatement)
            searchFilterLimits['allJobLocations'] = session.execute(allJobLocationsSelectStatement)
        return searchFilterLimits     