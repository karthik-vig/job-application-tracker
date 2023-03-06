from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_
from sqlalchemy.orm import Session, registry
import datetime



class DataFormatting:
    def strToDatetime(self, strDate: str):
        if strDate:
            dateYYYYMMDD = list( map( int, strDate.split('-') ) )
            return datetime.date(dateYYYYMMDD[0], dateYYYYMMDD[1], dateYYYYMMDD[2])
        else:
            return None
    
    def convertJobInfoEmptyStrToNull(self, jobInfo: dict):
        jobInfoKeys = jobInfo.keys()
        for key in jobInfoKeys:
            jobInfo[key] = None if jobInfo[key] == '' else jobInfo[key]
        if 'job' in jobInfoKeys and jobInfo['job'] == None:
            jobInfo['job'] = ''
        if 'company' in jobInfoKeys and jobInfo['company'] == None:
            jobInfo['company'] = ''
        return jobInfo

    def convertJobInfoNullToEmptyStr(self, jobInfo: dict):
        exemptFields = ['id', 'job', 'company', 'startJobTrackDate', 'modifiedJobTrackDate']
        jobInfokeys = jobInfo.keys()
        for key in jobInfokeys:
            if key not in exemptFields:
                jobInfo[key] = '' if jobInfo[key] == None else jobInfo[key]
        return jobInfo

    def convertRetrieveRowsToPrimitive(self, rows):
        rowList = []
        for row in rows:
            row = row[0]
            jobInfo = {
                'id': row.id,
                'job': row.job,
                'company': row.company,
                'salary': row.salary,
                'jobLocation': row.jobLocation,
                'jobStartDate': str(row.jobStartDate),
                'jobApplicationClosingDate': str(row.jobApplicationClosingDate),
                'applicationStatus': row.applicationStatus,
                'notes': row.notes,
                'startJobTrackDate': str(row.startJobTrackDate),
                'modifiedJobTrackDate': str(row.modifiedJobTrackDate)
            }
            jobInfo = self.convertJobInfoNullToEmptyStr(jobInfo=jobInfo)
            rowList.append(jobInfo)
        return rowList

    def convertJobLocationToPrimitive(self, allJobLocations):
        jobLocationsList = []
        for row in allJobLocations:
            if row.jobLocation != None:
                jobLocationsList.append(row.jobLocation)
        return jobLocationsList



class DatabaseHandler:
    def __init__(self):
        self.dataFormattingObj = DataFormatting()
        self.possibleApplicationStatus = ['Applied', 'I Rejected', 'They Rejected', 'Successful']
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
            job = Column(String(50), nullable=False)
            company = Column(String(100), nullable=False)
            salary = Column(Integer, nullable=True)
            jobLocation = Column(String(100), nullable=True)
            jobStartDate = Column(Date, nullable=True)
            jobApplicationClosingDate = Column(Date, nullable=True)
            applicationStatus = Column(String(20), nullable=True)
            notes = Column(String(10000), nullable=True)
            startJobTrackDate = Column(Date, nullable=False)
            modifiedJobTrackDate = Column(Date, nullable=False)
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
        if jobInfo['applicationStatus'] not in self.possibleApplicationStatus:
            jobInfo['applicationStatus'] = ''
        jobInfo = self.dataFormattingObj.convertJobInfoEmptyStrToNull(jobInfo=jobInfo)
        with Session(self.engine) as session:
            jobInfo['jobStartDate'] = self.dataFormattingObj.strToDatetime(jobInfo['jobStartDate'])
            jobInfo['jobApplicationClosingDate'] = self.dataFormattingObj.strToDatetime(jobInfo['jobApplicationClosingDate'])
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

    def deleteRow(self, id: int):
        with Session(self.engine) as session:
            queryRowToDelete = session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == int(id) )
            rowToDelete = session.execute(queryRowToDelete).first()
            session.delete(rowToDelete[0])
            session.commit()

    def updateRow(self, id: int, modificationValues: dict):
        if modificationValues['applicationStatus'] not in self.possibleApplicationStatus:
            modificationValues['applicationStatus'] = ''
        modificationValues = self.dataFormattingObj.convertJobInfoEmptyStrToNull(jobInfo=modificationValues)
        with Session(self.engine) as session:
            session.execute( update(self.JobTrackerTable)
                            .where(self.JobTrackerTable.id == id)
                            .values(job = modificationValues['job'],
                                    company = modificationValues['company'],
                                    salary = modificationValues['salary'],
                                    jobLocation = modificationValues['jobLocation'],
                                    jobStartDate = self.dataFormattingObj.strToDatetime(modificationValues['jobStartDate']),
                                    jobApplicationClosingDate = self.dataFormattingObj.strToDatetime(modificationValues['jobApplicationClosingDate']),
                                    applicationStatus = modificationValues['applicationStatus'],
                                    notes = modificationValues['notes'],
                                    modifiedJobTrackDate = func.current_date())
                            )
            session.commit()

    def retrieveRows(self, searchFilters: dict) -> list:
        with Session(self.engine) as session:
            queryStatement = self.buildSearchQueryStatement(searchFilters=searchFilters, session=session)
            rows = session.execute(queryStatement)
            rowList = self.dataFormattingObj.convertRetrieveRowsToPrimitive(rows)
        return rowList

    def buildSearchQueryStatement(self, searchFilters: dict, session):
        if searchFilters['id'] != '':
            searchFilters['id'] = int( searchFilters['id'] )
            queryStatement = session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == searchFilters['id'])
            return queryStatement
        queryStatement = session.query(self.JobTrackerTable).filter( or_( self.JobTrackerTable.job.like(f"%{searchFilters['searchText']}%"),
                                                     self.JobTrackerTable.company.like(f"%{searchFilters['searchText']}%") )
                                                   )                                           
        if searchFilters['salary']['min'] != '':
            searchFilters['salary']['min'] = int( searchFilters['salary']['min'] )
            queryStatement = queryStatement.filter(self.JobTrackerTable.salary >= searchFilters['salary']['min'])
        if searchFilters['salary']['max'] != '':
            searchFilters['salary']['max'] = int( searchFilters['salary']['max'] )
            queryStatement = queryStatement.filter(self.JobTrackerTable.salary <= searchFilters['salary']['max'])
        if searchFilters['jobStartDate'] != '':
            queryStatement = queryStatement.filter(self.JobTrackerTable.jobStartDate >= self.dataFormattingObj.strToDatetime(searchFilters['jobStartDate']) )
        if searchFilters['applicationStatus'] in self.possibleApplicationStatus:
            queryStatement = queryStatement.filter(self.JobTrackerTable.applicationStatus == searchFilters['applicationStatus'])
        if searchFilters['jobLocation'] != '':
            queryStatement = queryStatement.filter(self.JobTrackerTable.jobLocation.like(f"%{searchFilters['jobLocation']}%"))
        return queryStatement

    def getSearchFilterLimits(self) -> dict:
        searchFilterLimits = {"salary": {'min': None,
                                          'max': None
                                          }, 
                              "allJobLocations": []
                              }
        with Session(self.engine) as session:
            allJobLocationsSelectStatement = session.query(self.JobTrackerTable.jobLocation).distinct()
            searchFilterLimits['salary']['min'] = session.query(func.min(self.JobTrackerTable.salary)).scalar()
            searchFilterLimits['salary']['max'] = session.query(func.max(self.JobTrackerTable.salary)).scalar()
            searchFilterLimits['allJobLocations'] = session.execute(allJobLocationsSelectStatement)
            searchFilterLimits['allJobLocations'] = self.dataFormattingObj.convertJobLocationToPrimitive(searchFilterLimits['allJobLocations'])
        return searchFilterLimits