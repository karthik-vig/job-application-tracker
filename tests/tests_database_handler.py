from sqlalchemy import create_engine, Column, Integer, String, Date, Table, func, update, select, or_, and_, ForeignKey, LargeBinary
from sqlalchemy.orm import Session, registry, relationship
import copy
import datetime
import unittest
import datetime
import sys
sys.path.append('./flaskr/')
from database import DatabaseHandler

engine = create_engine("sqlite+pysqlite:///jobDatabase.db", echo=False, future=True)
mapper_resgistry = registry()
Base = mapper_resgistry.generate_base()

class JobTrackerTable(Base):
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
    
class FileTrackerTable(Base):
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


def getFiledata(path):
    data = None
    with open(path, 'rb') as file:
        data = file.read()
    return data



def insertRowIntoDatabase():
    jobTrackerTableRowsValue =[('test job', 'test company', 50000, 'london', datetime.date(2023,9,1), datetime.date(2023,8,1), 'Successful', 'nice notes',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 2', 'test company 2', 60000, 'Glasgow', datetime.date(2023,10,1), datetime.date(2023,9,1), 'Applied', 'nice notes 2',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 3', 'test company 3', 70000, 'london', datetime.date(2023,11,1), datetime.date(2023,10,1), 'Successful', 'nice notes 3',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 4', 'test company 4', 80000, 'edinburgh', datetime.date(2023,12,1), datetime.date(2023,11,1), 'I Rejected', 'nice notes 4',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 5', 'test company 5', 90000, 'glasgow', datetime.date(2023,7,1), datetime.date(2023,6,1), 'They Rejected', 'nice notes 5',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 6', 'test company 6', 100000, 'Norwich', datetime.date(2023,4,25), datetime.date(2023,4,10), 'I Rejected', 'nice notes 6',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 7', 'test company 7', 85000, 'manchester', datetime.date(2023,9,25), datetime.date(2023,8,10), 'Applied', 'nice notes 7',  datetime.date(2023,3,9),  datetime.date(2023,3,9)),
                                ('test job 8', 'test company 8', 40000, 'norwich', datetime.date(2023,5,10), datetime.date(2023,5,1), 'They Rejected', 'nice notes 8',  datetime.date(2023,3,9),  datetime.date(2023,3,9))
                                ]
    # insert the row into table
    commonFilePath = 'C:\\Users\\karthik\\Desktop'
    resumeFileName = '99-bottles of OOP.pdf'
    resumeFilePath = commonFilePath + '\\' + resumeFileName
    coverLetterFileName = 'autoencoder based clustering.pdf'
    coverLetterFilePath = commonFilePath + '\\' + coverLetterFileName
    extraFileName = 'Eclipse IDE Tutorial.pdf'
    extraFilePath  = commonFilePath + '\\' + extraFileName
    with Session(engine) as session:
        for row in jobTrackerTableRowsValue:
            jobTrackerTablerow = JobTrackerTable(job = row[0],
                                                company = row[1],
                                                salary = row[2],
                                                jobLocation = row[3],
                                                jobStartDate = row[4],
                                                jobApplicationClosingDate = row[5],
                                                applicationStatus = row[6],
                                                notes = row[7],
                                                startJobTrackDate = row[8],
                                                modifiedJobTrackDate = row[9]
                                                )
            fileTrackerTableRow = FileTrackerTable(
                                                    resumeFilename = resumeFileName,
                                                    resumeFileData = getFiledata(resumeFilePath),
                                                    coverLetterFilename = coverLetterFileName,
                                                    coverLetterFileData = getFiledata(coverLetterFilePath),
                                                    extraFilename = extraFileName,
                                                    extraFileData = getFiledata(extraFilePath),
                                                    jobTracker = jobTrackerTablerow
                                                )
            session.add(jobTrackerTablerow)
            session.commit()
            session.add(fileTrackerTableRow)
            session.commit()


def getRowFromDatabase():
    with Session(engine) as session:
        rows = session.query(JobTrackerTable, FileTrackerTable).all()
        retrievedRowJobInfoList = []
        for row in rows:
            jobTrackerTableRow = row[0]
            fileTrackerTableRow = row[1]
            retrievedRowJobInfo = {'job': str(jobTrackerTableRow.job),
                                    'company': str(jobTrackerTableRow.company),
                                    'salary': str(jobTrackerTableRow.salary),
                                    'jobLocation': str(jobTrackerTableRow.jobLocation),
                                    'jobStartDate': str(jobTrackerTableRow.jobStartDate),
                                    'jobApplicationClosingDate': str(jobTrackerTableRow.jobApplicationClosingDate),
                                    'applicationStatus': str(jobTrackerTableRow.applicationStatus),
                                    'notes': str(jobTrackerTableRow.notes),
                                    'resumeFile': {'name': str(fileTrackerTableRow.resumeFilename),
                                                'data': fileTrackerTableRow.resumeFileData
                                                },
                                    'coverLetterFile': {'name': str(fileTrackerTableRow.coverLetterFilename),
                                                        'data': fileTrackerTableRow.coverLetterFileData
                                                        },
                                    'extraFile': {'name': str(fileTrackerTableRow.extraFilename),
                                                'data': fileTrackerTableRow.extraFileData
                                                }
                                    }
            retrievedRowJobInfoList.append(retrievedRowJobInfo)
    return retrievedRowJobInfoList





class TestDatabaseHandler(unittest.TestCase):
    def testAddRow(self):
        # drop all tables
        mapper_resgistry.metadata.drop_all(engine)
        # create tables
        mapper_resgistry.metadata.create_all(engine)
        # use database handler object to add a row
        databaseHandlerObj = DatabaseHandler()
        commonFilePath = 'C:\\Users\\karthik\\Desktop'
        resumeFileName = '99-bottles of OOP.pdf'
        resumeFilePath = commonFilePath + '\\' + resumeFileName
        coverLetterFileName = 'autoencoder based clustering.pdf'
        coverLetterFilePath = commonFilePath + '\\' + coverLetterFileName
        extraFileName = 'Eclipse IDE Tutorial.pdf'
        extraFilePath  = commonFilePath + '\\' + extraFileName
        jobInfo = {'job': 'test job 1',
                    'company': 'test company 1',
                    'salary': '60000',
                    'jobLocation': 'glasgow',
                    'jobStartDate': '2023-09-01',
                    'jobApplicationClosingDate': '2023-08-01',
                    'applicationStatus': 'Applied',
                    'notes': 'nice job',
                    'resumeFile': {'name': resumeFileName,
                                'data': getFiledata(resumeFilePath)
                                },
                    'coverLetterFile': {'name': coverLetterFileName,
                                        'data': getFiledata(coverLetterFilePath)
                                        },
                    'extraFile': {'name': extraFileName,
                                'data': getFiledata(extraFilePath)
                                }
                    }
        databaseHandlerObj.addRow(jobInfo=copy.deepcopy(jobInfo))
        # get the the row
        retrievedRowJobInfo = getRowFromDatabase()
        # assert the equality of the row to what we expect
        self.assertEqual(jobInfo, retrievedRowJobInfo[-1])

    
    def testDeleteRow(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # delete the row using database handler object
        obj = DatabaseHandler()
        obj.deleteRow(id='1')
        # get rows from the table, to see if they are deleted
        with Session(engine) as session:
            rows = session.query(JobTrackerTable, FileTrackerTable).all()
        # assert if the retrieved rows are missing the deleted one
        tableIDList = []
        for row in rows:
            tableIDList.append(row[0].id)
            tableIDList.append(row[1].id)
        self.assertNotIn(1, tableIDList)

    #'''
    def testUpdateRow(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # update the row using database handler function
        obj = DatabaseHandler()
        commonFilePath = 'C:\\Users\\karthik\\Desktop'
        resumeFileName = '[ML] A First Course in Machine Learning.pdf'
        resumeFilePath = commonFilePath + '\\' + resumeFileName
        coverLetterFileName = 'Deep-Learning-with-PyTorch.pdf'
        coverLetterFilePath = commonFilePath + '\\' + coverLetterFileName
        extraFileName = 'elements of statistical learning (bible of machine learning part 2).pdf'
        extraFilePath  = commonFilePath + '\\' + extraFileName
        modifiedJobInfo = { 
                            'job': 'test job 2', 
                            'company': 'test company 2', 
                            'salary': '70000',
                            'jobLocation': 'edinburghhhhh',
                            'jobStartDate': '2023-09-02',
                            'jobApplicationClosingDate': '2023-08-02',
                            'applicationStatus': 'Applied',
                            'notes': 'nice job',
                            'resumeFile': {'name': resumeFileName,
                                            'data': getFiledata(resumeFilePath)
                                            },
                            'coverLetterFile': {'name': coverLetterFileName,
                                                'data': getFiledata(coverLetterFilePath)
                                                },
                            'extraFile': {'name': extraFileName,
                                            'data': getFiledata(extraFilePath)
                                            },
                            'resumeFileDelete': None,
                            'coverLetterFileDelete': None,
                            'extraFileDelete': None
                        }
        obj.updateRow(id='1', modificationValues=copy.deepcopy(modifiedJobInfo))
        # assert the update match the expectation.
        retrievedRowJobInfo = getRowFromDatabase()
        expectedRowValues = { 
                            'job': 'test job 2', 
                            'company': 'test company 2', 
                            'salary': '70000',
                            'jobLocation': 'edinburghhhhh',
                            'jobStartDate': '2023-09-02',
                            'jobApplicationClosingDate': '2023-08-02',
                            'applicationStatus': 'Applied',
                            'notes': 'nice job',
                            'resumeFile': {'name': resumeFileName,
                                            'data': getFiledata(resumeFilePath)
                                            },
                            'coverLetterFile': {'name': coverLetterFileName,
                                                'data': getFiledata(coverLetterFilePath)
                                                },
                            'extraFile': {'name': extraFileName,
                                            'data': getFiledata(extraFilePath)
                                            },
                        }
        self.assertEqual(retrievedRowJobInfo[0], expectedRowValues)
    #'''
    #'''
    def testUpdateRowFileTrackerNull(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # update the row using database handler function
        obj = DatabaseHandler()
        commonFilePath = 'C:\\Users\\karthik\\Desktop'
        resumeFileName = '[ML] A First Course in Machine Learning.pdf'
        resumeFilePath = commonFilePath + '\\' + resumeFileName
        coverLetterFileName = 'Deep-Learning-with-PyTorch.pdf'
        coverLetterFilePath = commonFilePath + '\\' + coverLetterFileName
        extraFileName = 'elements of statistical learning (bible of machine learning part 2).pdf'
        extraFilePath  = commonFilePath + '\\' + extraFileName
        modifiedJobInfo = { 
                            'job': 'test job 2', 
                            'company': 'test company 2', 
                            'salary': '70000',
                            'jobLocation': 'edinburghhhhh',
                            'jobStartDate': '2023-09-02',
                            'jobApplicationClosingDate': '2023-08-02',
                            'applicationStatus': 'Applied',
                            'notes': 'nice job',
                            'resumeFile': {'name': resumeFileName,
                                            'data': getFiledata(resumeFilePath)
                                            },
                            'coverLetterFile': {'name': coverLetterFileName,
                                                'data': getFiledata(coverLetterFilePath)
                                                },
                            'extraFile': {'name': extraFileName,
                                            'data': getFiledata(extraFilePath)
                                            },
                            'resumeFileDelete': 'on',
                            'coverLetterFileDelete': 'on',
                            'extraFileDelete': 'on'
                        }
        obj.updateRow(id='1', modificationValues=copy.deepcopy(modifiedJobInfo))
        # assert the update match the expectation.
        retrievedRowJobInfo = getRowFromDatabase()
        expectedRowValues = { 
                            'job': 'test job 2', 
                            'company': 'test company 2', 
                            'salary': '70000',
                            'jobLocation': 'edinburghhhhh',
                            'jobStartDate': '2023-09-02',
                            'jobApplicationClosingDate': '2023-08-02',
                            'applicationStatus': 'Applied',
                            'notes': 'nice job',
                            'resumeFile': {'name': 'None',
                                            'data': None
                                            },
                            'coverLetterFile': {'name': 'None',
                                                'data': None
                                                },
                            'extraFile': {'name': 'None',
                                            'data': None
                                            },
                        }
        self.assertEqual(retrievedRowJobInfo[0], expectedRowValues)
    #'''
    
    def testGetRowOnID(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # get row based on id using database handler class object
        obj = DatabaseHandler()
        jobTrackerTableRow = obj.getRowsOnID(id='1', tableName='JobTrackerTable')
        fileTrackerTableRow = obj.getRowsOnID(id='1', tableName='FileTrackerTable')
        jobInfo = {}
        jobInfo.update(jobTrackerTableRow[0])
        jobInfo.update(fileTrackerTableRow[0])
        # write out the expected row values for the id
        commonFilePath = 'C:\\Users\\karthik\\Desktop'
        resumeFileName = '99-bottles of OOP.pdf'
        resumeFilePath = commonFilePath + '\\' + resumeFileName
        coverLetterFileName = 'autoencoder based clustering.pdf'
        coverLetterFilePath = commonFilePath + '\\' + coverLetterFileName
        extraFileName = 'Eclipse IDE Tutorial.pdf'
        extraFilePath  = commonFilePath + '\\' + extraFileName
        expectedRowValues = {'id': 1,
                            'job': 'test job',
                            'company': 'test company',
                            'salary': 50000,
                            'jobLocation': 'london',
                            'jobStartDate': '2023-09-01',
                            'jobApplicationClosingDate': '2023-08-01',
                            'applicationStatus': 'Successful',
                            'notes': 'nice notes',
                            'startJobTrackDate': '2023-03-09',
                            'modifiedJobTrackDate': '2023-03-09',
                            'resumeFile': {'name': resumeFileName,
                                        'data': getFiledata(resumeFilePath)
                                        },
                            'coverLetterFile': {'name': coverLetterFileName,
                                                'data': getFiledata(coverLetterFilePath)
                                                },
                            'extraFile': {'name': extraFileName,
                                        'data': getFiledata(extraFilePath)
                                        }
                            }
        # assert the values
        self.assertEqual(expectedRowValues, jobInfo)
    

    def testSearchJobTrackerTableRows(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # search JobTrackerTable based on search filters
        obj = DatabaseHandler()
        searchFilters = { 'id': '',
                            'searchText': 'test',
                            'salary': { 'min': 55000,
                                        'max': 96000
                                        },
                            'jobStartDate': '2023-07-01',
                            'applicationStatus': 'Applied',
                            'jobLocation': 'glas'
                            }
        jobTrackerTableSearchRows, resultStatsDict = obj.searchJobTrackerTableRows(searchFilters=searchFilters)
        #('test job 2', 'test company 2', 60000, 'glasgow', datetime.date(2023,10,1), datetime.date(2023,9,1), 'Applied', 'nice notes 2',  datetime.date(2023,3,9),  datetime.date(2023,3,9))
        expectedJobTrackerTableSearchRows = [ { 'id': 2,
                                                'job': 'test job 2',
                                                'company': 'test company 2',
                                                'salary': 60000,
                                                'jobLocation': 'Glasgow',
                                                'jobStartDate': str(datetime.date(2023,10,1)),
                                                'jobApplicationClosingDate': str(datetime.date(2023,9,1)),
                                                'applicationStatus': 'Applied',
                                                'notes': 'nice notes 2',
                                                'startJobTrackDate': str(datetime.date(2023,3,9)),
                                                'modifiedJobTrackDate': str(datetime.date(2023,3,9))
                                                },
                                            ]
        self.assertEqual(jobTrackerTableSearchRows, expectedJobTrackerTableSearchRows)

    def testSearchJobTrackerTableRowsResultStat(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # search JobTrackerTable based on search filters
        obj = DatabaseHandler()
        searchFilters = { 'id': '',
                            'searchText': 'test',
                            'salary': { 'min': 55000,
                                        'max': 96000
                                        },
                            'jobStartDate': '2023-07-01',
                            'applicationStatus': 'Applied',
                            'jobLocation': 'glas'
                            }
        jobTrackerTableSearchRows, resultStatsDict = obj.searchJobTrackerTableRows(searchFilters=searchFilters)
        #('test job 2', 'test company 2', 60000, 'glasgow', datetime.date(2023,10,1), datetime.date(2023,9,1), 'Applied', 'nice notes 2',  datetime.date(2023,3,9),  datetime.date(2023,3,9))
        expectedresultStatsDict = {'salary': {'min': 60000,
                                         'max': 60000
                                         },
                                    'jobStartDate': {'latest': str(datetime.date(2023,10,1)),
                                                    'last': str(datetime.date(2023,10,1))
                                                     }
                                    }
        self.assertEqual(resultStatsDict, expectedresultStatsDict)

    def testGetSearchFiltersLimits(self):
        # drop all table
        mapper_resgistry.metadata.drop_all(engine)
        # create table
        mapper_resgistry.metadata.create_all(engine)
        # insert the row into table
        insertRowIntoDatabase()
        # get the filter limits from database handler class
        obj  = DatabaseHandler()
        searchFilterLimits = obj.getSearchFilterLimits()
        searchFilterLimits['allJobLocations'].sort()
        expectedSearchFilterLimits = {"salary": {'min': 40000,
                                                'max': 100000},
                                       "allJobLocations": ['london', 'glasgow', 'edinburgh', 'norwich', 'manchester']
                                       }
        expectedSearchFilterLimits['allJobLocations'].sort()
        self.assertEqual(searchFilterLimits, expectedSearchFilterLimits)


if __name__ == "__main__":
    unittest.main() 