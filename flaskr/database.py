from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship
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
            if str(type(jobInfo[key])) == "<class 'dict'>":
                jobInfo[key] = self.convertJobInfoEmptyStrToNull(jobInfo=jobInfo[key])
            jobInfo[key] = None if (jobInfo[key] == '' or jobInfo[key] == b'') else jobInfo[key]
        if 'job' in jobInfoKeys and jobInfo['job'] == None:
            jobInfo['job'] = ''
        if 'company' in jobInfoKeys and jobInfo['company'] == None:
            jobInfo['company'] = ''
        return jobInfo

    def convertJobInfoNullToEmptyStr(self, jobInfo: dict) -> dict:
        exemptFields = ['id', 'job', 'company', 'startJobTrackDate', 'modifiedJobTrackDate']
        for key in jobInfo.keys():
            if key not in exemptFields:
                jobInfo[key] = '' if jobInfo[key] == None else jobInfo[key]
        return jobInfo

    def convertFileInfoNullToEmptyVal(self, fileInfo: dict) -> dict:
        for key in fileInfo.keys():
            if str(type(fileInfo[key])) == "<class 'dict'>":
                fileInfo[key] = self.convertFileInfoNullToEmptyVal(fileInfo=fileInfo[key])
                continue
            fileInfo[key] = '' if (key == 'name' and fileInfo[key] == None) else fileInfo[key]
            fileInfo[key] = b'' if (key == 'data' and fileInfo[key] == None) else fileInfo[key]
        return fileInfo


    def convertRowsToPrimitive(self, rows, tableName):
        rowList = []
        for row in rows:
            row = row[0]
            if tableName == 'JobTrackerTable':
                rowInfo = self.constructJobTrackerPrimitive(row=row)
            elif tableName == 'FileTrackerTable':
                rowInfo = self.constructFileTrackerPrimitive(row=row)
            rowList.append(rowInfo)
        return rowList

    def constructJobTrackerPrimitive(self, row):
        jobInfo = { 'id': row.id,
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
        return jobInfo

    def constructFileTrackerPrimitive(self, row):
        fileInfo = {'resumeFile': {'name': row.resumeFilename,
                                'data': row.resumeFileData
                                },
                    'coverLetterFile': {'name': row.coverLetterFilename,
                                        'data': row.coverLetterFileData
                                        },
                    'extraFile': {'name': row.extraFilename,
                                'data': row.extraFileData
                                }
                    }
        self.convertFileInfoNullToEmptyVal(fileInfo=fileInfo)
        return fileInfo

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
        self.JobTrackerTable, self.FileTrackerTable = self.createTables()
        self.mapper_registry.metadata.create_all(self.engine)

    def createTables(self):
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
            fileTracker = relationship("FileTrackerTable", back_populates="jobTracker")
            def __repr__(self):
                return f"Table recording all job tracking information"
            
        class FileTrackerTable(self.Base):
            __tablename__ = "FileTrackerTable"
            id = Column(Integer, ForeignKey("JobTrackerTable.id"), primary_key=True)
            resumeFilename = Column(String(100), nullable=True)
            resumeFileData = Column(LargeBinary, nullable=True)
            coverLetterFilename = Column(String(100), nullable=True)
            coverLetterFileData = Column(LargeBinary, nullable=True)
            extraFilename = Column(String(100), nullable=True)
            extraFileData = Column(LargeBinary, nullable=True)
            jobTracker = relationship("JobTrackerTable", back_populates="fileTracker")
            def __repr__(self):
                return f"Table related to JobTrackerTable. Records the uploaded file data." 
        return JobTrackerTable, FileTrackerTable    

    def addRow(self, jobInfo: dict):
        if jobInfo['applicationStatus'] not in self.possibleApplicationStatus:
            jobInfo['applicationStatus'] = ''
        jobInfo = self.dataFormattingObj.convertJobInfoEmptyStrToNull(jobInfo=jobInfo)
        with Session(self.engine) as session:
            jobInfo['jobStartDate'] = self.dataFormattingObj.strToDatetime(jobInfo['jobStartDate'])
            jobInfo['jobApplicationClosingDate'] = self.dataFormattingObj.strToDatetime(jobInfo['jobApplicationClosingDate'])
            jobTrackerRowToInsert = self.JobTrackerTable(job = jobInfo['job'],
                                                        company = jobInfo['company'],
                                                        salary = jobInfo['salary'],
                                                        jobLocation = jobInfo['jobLocation'],
                                                        jobStartDate = jobInfo['jobStartDate'],
                                                        jobApplicationClosingDate = jobInfo['jobApplicationClosingDate'],
                                                        applicationStatus = jobInfo['applicationStatus'],
                                                        notes = jobInfo['notes'],
                                                        startJobTrackDate = func.current_date(),
                                                        modifiedJobTrackDate = func.current_date())
            fileTrackerRowToInsert = self.FileTrackerTable(resumeFilename = jobInfo['resumeFile']['name'],
                                                           resumeFileData = jobInfo['resumeFile']['data'],
                                                           coverLetterFilename = jobInfo['coverLetterFile']['name'],
                                                           coverLetterFileData = jobInfo['coverLetterFile']['data'],
                                                           extraFilename = jobInfo['extraFile']['name'],
                                                           extraFileData = jobInfo['extraFile']['data'],
                                                           jobTracker = jobTrackerRowToInsert)
            session.add(jobTrackerRowToInsert)
            session.commit()
            session.add(fileTrackerRowToInsert)
            session.commit()

    def deleteRow(self, id: str):
        id = int(id)
        with Session(self.engine) as session:
            session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == id).delete()
            session.query(self.FileTrackerTable).filter(self.FileTrackerTable.id == id).delete()
            session.commit()

    def updateRow(self, id: str, modificationValues: dict):
        id = int(id)
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

            if modificationValues['resumeFileDelete'] == 'on':
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(resumeFilename = None,
                                        resumeFileData = None
                                        )
                                )
            elif modificationValues['resumeFile']['name'] != None \
                                and modificationValues['resumeFile']['data'] != None:
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(resumeFilename = modificationValues['resumeFile']['name'],
                                        resumeFileData = modificationValues['resumeFile']['data']
                                        )
                                )

            if modificationValues['coverLetterFileDelete'] == 'on':
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(coverLetterFilename = None,
                                        coverLetterFileData = None
                                        )
                                )
            elif modificationValues['coverLetterFile']['name'] != None \
                                and modificationValues['coverLetterFile']['data'] != None:
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(coverLetterFilename = modificationValues['coverLetterFile']['name'],
                                        coverLetterFileData = modificationValues['coverLetterFile']['data']
                                        )
                                )
                
            if modificationValues['extraFileDelete'] == 'on':
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(extraFilename = None,
                                        extraFileData = None
                                        )
                                ) 
            elif modificationValues['extraFile']['name'] != None \
                                and modificationValues['extraFile']['data'] != None:
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(extraFilename = modificationValues['extraFile']['name'],
                                        extraFileData = modificationValues['extraFile']['data']
                                        )
                                ) 
            session.commit()

    def getRowsOnID(self, id: str, tableName: str) -> list:
        id = int(id)
        with Session(self.engine) as session:
            if tableName == 'JobTrackerTable':
                queryStatement = session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == id)
            elif tableName == 'FileTrackerTable':
                queryStatement = session.query(self.FileTrackerTable).filter(self.FileTrackerTable.id == id)
            else:
                return []
            rows = session.execute(queryStatement)
            rowList = self.dataFormattingObj.convertRowsToPrimitive(rows=rows, tableName=tableName)
        return rowList

    def searchJobTrackerTableRows(self, searchFilters: dict) -> list:
        with Session(self.engine) as session:
            queryStatement = self.buildSearchQueryStatement(searchFilters=searchFilters, session=session)
            rows = session.execute(queryStatement)
            rowList = self.dataFormattingObj.convertRowsToPrimitive(rows=rows, tableName='JobTrackerTable')
        return rowList

    def buildSearchQueryStatement(self, searchFilters: dict, session):
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