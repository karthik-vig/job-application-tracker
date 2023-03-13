from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship
import datetime



# This class is used for formatting the data from the flask to 
# a data format that can be entered into the database using 
# SQLAlchemy.
class DataFormatting:
    # converts international date to datetime object.
    def strToDatetime(self, strDate: str):
        if strDate:
            dateYYYYMMDD = list( map( int, strDate.split('-') ) )
            return datetime.date(dateYYYYMMDD[0], dateYYYYMMDD[1], dateYYYYMMDD[2])
        else:
            return None
    
    # Recursively converts all empty string and empty bytes to None in the given dict.
    def convertDictEmptyValueToNull(self, jobInfo: dict):
        jobInfoKeys = jobInfo.keys()
        for key in jobInfoKeys:
            if str(type(jobInfo[key])) == "<class 'dict'>":
                jobInfo[key] = self.convertDictEmptyValueToNull(jobInfo=jobInfo[key])
            jobInfo[key] = None if (jobInfo[key] == '' or jobInfo[key] == b'') else jobInfo[key]
        if 'job' in jobInfoKeys and jobInfo['job'] == None:
            jobInfo['job'] = ''
        if 'company' in jobInfoKeys and jobInfo['company'] == None:
            jobInfo['company'] = ''
        return jobInfo

    # Extracts the column value for each row from the SQLAlchemy database and puts them
    # in python dict.
    # TableName argument is used to convert to appropriate dicts.
    def convertRowsToPrimitive(self, rows, tableName):
        rowList = []
        for row in rows:
            row = row[0]
            if tableName == 'JobTrackerTable':
                rowInfo = self._constructJobTrackerPrimitive(row=row)
            elif tableName == 'FileTrackerTable':
                rowInfo = self._constructFileTrackerPrimitive(row=row)
            rowList.append(rowInfo)
        return rowList

    # Internal function used by convertRowsToPrimitive() to construct the dict
    # for JobTrackerTable row values.
    def _constructJobTrackerPrimitive(self, row):
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
        jobInfo = self._convertJobInfoNullToEmptyStr(jobInfo=jobInfo)
        return jobInfo
    
    # All values in the dict that is None is replaced with an empty string.
    # Specifically Works on values from JobTrackerTable
    def _convertJobInfoNullToEmptyStr(self, jobInfo: dict) -> dict:
        exemptFields = ['id', 'job', 'company', 'startJobTrackDate', 'modifiedJobTrackDate']
        for key in jobInfo.keys():
            if key not in exemptFields:
                jobInfo[key] = '' if jobInfo[key] == None else jobInfo[key]
        return jobInfo

    # Internal function used by convertRowsToPrimitive() to construct the dict
    # for FileTrackerTable row values.
    def _constructFileTrackerPrimitive(self, row):
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
        self._convertFileInfoNullToEmptyVal(fileInfo=fileInfo)
        return fileInfo

    # All values in the dict that is None is replaced with an empty string if the key is 'name'
    # else if the key is 'data' it is replaced with empty bytes.
    # Specifically Works on values from FileTrackerTable
    def _convertFileInfoNullToEmptyVal(self, fileInfo: dict) -> dict:
        for key in fileInfo.keys():
            if str(type(fileInfo[key])) == "<class 'dict'>":
                fileInfo[key] = self._convertFileInfoNullToEmptyVal(fileInfo=fileInfo[key])
                continue
            fileInfo[key] = '' if (key == 'name' and fileInfo[key] == None) else fileInfo[key]
            fileInfo[key] = b'' if (key == 'data' and fileInfo[key] == None) else fileInfo[key]
        return fileInfo

    # Converts job location data (from JobTrackerTable) from SQLAlchemy database to list format. 
    def convertJobLocationToPrimitive(self, allJobLocations):
        jobLocationsList = []
        for row in allJobLocations:
            if row.jobLocation != None:
                jobLocation = str(row.jobLocation).lower()
                jobLocationsList.append(jobLocation)
            jobLocationsList = list(set(jobLocationsList))
        return jobLocationsList



# This class interacts with the sqlite database to record and retrive information.
# It uses DataFormatting class through composition.
class DatabaseHandler:
    # initializes the object for DataFormatting class.
    # Setups up connection for SQLAlchemy to connect with sqlite database.
    # Creates / gets the Two tables: JobTrackerTable, FileTrackerTable
    def __init__(self):
        self.dataFormattingObj = DataFormatting()
        self.possibleApplicationStatus = ['Applied', 'I Rejected', 'They Rejected', 'Successful']
        self.engine = create_engine("sqlite+pysqlite:///jobDatabase.db", echo=True, future=True)
        self.mapper_registry = registry()
        self.Base = self.mapper_registry.generate_base()
        self.JobTrackerTable, self.FileTrackerTable = self._createTables()
        self.mapper_registry.metadata.create_all(self.engine)

    # Setup the two tables: JobTrackerTable, FileTrackerTable
    def _createTables(self):
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

    # Add a new row into JobTrakcerTable and FileTrackerTable.
    # jobInfo is a dict that contains the necessary value for all the columns of
    # both the table.
    def addRow(self, jobInfo: dict):
        if jobInfo['applicationStatus'] not in self.possibleApplicationStatus:
            jobInfo['applicationStatus'] = ''
        jobInfo = self.dataFormattingObj.convertDictEmptyValueToNull(jobInfo=jobInfo)
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

    # Delete a specific row from both JobTrackerTable and FileTrackerTable based on id.
    def deleteRow(self, id: str):
        id = int(id)
        with Session(self.engine) as session:
            session.query(self.JobTrackerTable).filter(self.JobTrackerTable.id == id).delete()
            session.query(self.FileTrackerTable).filter(self.FileTrackerTable.id == id).delete()
            session.commit()

    # Update a row value for both tables based on id.
    # the update can be for both tables or JobTrackerTable alone.
    def updateRow(self, id: str, modificationValues: dict):
        id = int(id)
        if modificationValues['applicationStatus'] not in self.possibleApplicationStatus:
            modificationValues['applicationStatus'] = ''
        modificationValues = self.dataFormattingObj.convertDictEmptyValueToNull(jobInfo=modificationValues)
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
            self._updateResumeFile(id=id,
                                  resumeFileDelete=modificationValues['resumeFileDelete'],
                                  resumeFileValue=modificationValues['resumeFile'],
                                  session=session)
            self._updateCoverLetterFile(id=id,
                                       coverLetterFileDelete=modificationValues['coverLetterFileDelete'],
                                       coverLetterFileValue=modificationValues['coverLetterFile'],
                                       session=session)
            self._updateExtraFile(id=id,
                                 extraFileDelete=modificationValues['extraFileDelete'],
                                 extraFileValue=modificationValues['extraFile'],
                                 session=session)
            session.commit()

    # internal function used by updateRow to update resume file name and data in 
    # FileTrackerTable.
    def _updateResumeFile(self, id, resumeFileDelete, resumeFileValue, session):
        if resumeFileDelete == 'on':
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(resumeFilename = None,
                                        resumeFileData = None
                                        )
                                )
        elif resumeFileValue['name'] != None \
                            and resumeFileValue['data'] != None:
            session.execute( update(self.FileTrackerTable)
                            .where(self.FileTrackerTable.id == id)
                            .values(resumeFilename = resumeFileValue['name'],
                                    resumeFileData = resumeFileValue['data']
                                    )
                            )
    # internal function used by updateRow to update cover letter file name and data in 
    # FileTrackerTable.
    def _updateCoverLetterFile(self, id, coverLetterFileDelete, coverLetterFileValue, session):
        if coverLetterFileDelete == 'on':
            session.execute( update(self.FileTrackerTable)
                            .where(self.FileTrackerTable.id == id)
                            .values(coverLetterFilename = None,
                                    coverLetterFileData = None
                                    )
                            )
        elif coverLetterFileValue['name'] != None \
                            and coverLetterFileValue['data'] != None:
            session.execute( update(self.FileTrackerTable)
                            .where(self.FileTrackerTable.id == id)
                            .values(coverLetterFilename = coverLetterFileValue['name'],
                                    coverLetterFileData = coverLetterFileValue['data']
                                    )
                            )

    # internal function used by updateRow to update extra file name and data in 
    # FileTrackerTable.
    def _updateExtraFile(self, id, extraFileDelete, extraFileValue, session):
        if extraFileDelete == 'on':
                session.execute( update(self.FileTrackerTable)
                                .where(self.FileTrackerTable.id == id)
                                .values(extraFilename = None,
                                        extraFileData = None
                                        )
                                ) 
        elif extraFileValue['name'] != None \
                            and extraFileValue['data'] != None:
            session.execute( update(self.FileTrackerTable)
                            .where(self.FileTrackerTable.id == id)
                            .values(extraFilename = extraFileValue['name'],
                                    extraFileData = extraFileValue['data']
                                    )
                            )

    # Get a row based on id and table name.
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

    # search for row(s) in JobTrackerTable using some search filter values in JobTrackerTable
    def searchJobTrackerTableRows(self, searchFilters: dict) -> list:
        with Session(self.engine) as session:
            queryStatement = self._buildSearchQueryStatement(searchFilters=searchFilters, session=session)
            rows = session.execute(queryStatement)
            rowList = self.dataFormattingObj.convertRowsToPrimitive(rows=rows, tableName='JobTrackerTable')
        return rowList

    # Internal function used by searchJobTrackerTableRows to build the select statement
    # based on search filter values entered by the user.
    def _buildSearchQueryStatement(self, searchFilters: dict, session):
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

    # Get the minimum and maximum salary along with unique job locations from the JobTrackerTable
    # in dict form.
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