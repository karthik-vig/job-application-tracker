import unittest
import datetime
import sys
sys.path.append('./flaskr/')
from database import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def testAddRetrieveFunctionality(self):
        allApplicationStatus = ['Applied', 'Accepted', 'I Rejected', 'They Rejected']
        jobInfo = { 'job' : 'auditor2',
                    'company': 'kpmg',
                    'salary': 30000,
                    'jobLocation': 'glasgow',
                    'jobStartDate': datetime.date(2023,9,1),
                    'jobApplicationClosingDate': datetime.date(2023,4,10),
                    'applicationStatus': allApplicationStatus[0],
                    'notes': 'the job  pays really well; try really hard to get it'
                  }
        searchFilters = { 'searchText' : 'auditor',
                          'salary': None,
                          'jobStartDate': None,
                          'applicationStatus': None,
                          'jobLocation': None
                        }
        databaseHandlerObj = DatabaseHandler()
        databaseHandlerObj.addRow(jobInfo = jobInfo)
        retrievedRows = databaseHandlerObj.retrieveRows(searchFilters = searchFilters)
        jobInfo['startJobTrackDate'] = datetime.date.today()
        jobInfo['modifiedJobTrackDate'] = datetime.date.today()
        del retrievedRows[-1]['id']
        self.assertEqual(jobInfo, retrievedRows[-1])

    def testUpdateFunctionality(self):
        allApplicationStatus = ['Applied', 'Accepted', 'I Rejected', 'They Rejected']
        jobInfo = { 'job' : 'auditor2',
            'company': 'kpmg',
            'salary': 30000,
            'jobLocation': 'glasgow',
            'jobStartDate': datetime.date(2023,9,1),
            'jobApplicationClosingDate': datetime.date(2023,4,10),
            'applicationStatus': allApplicationStatus[0],
            'notes': 'the job  pays really well; try really hard to get it'
            }
        searchFilters = { 'searchText' : '',
                    'salary': None,
                    'jobStartDate': None,
                    'applicationStatus': None,
                    'jobLocation': None
                }
        databaseHandlerObj = DatabaseHandler()
        retrievedRows = databaseHandlerObj.retrieveRows(searchFilters = searchFilters)
        id = retrievedRows[-1]['id']
        modificationValues = retrievedRows[-1]
        del modificationValues['id']
        del modificationValues['modifiedJobTrackDate']
        modificationValues['salary'] = 50000
        databaseHandlerObj.updateRow(id = id, modificationValues = modificationValues)
        updatedRetrievedRows = databaseHandlerObj.retrieveRows(searchFilters = searchFilters)
        updatedRow  = updatedRetrievedRows[-1]
        del updatedRow['id']
        del updatedRow['modifiedJobTrackDate']
        self.assertEqual(modificationValues, updatedRow)

    def testDeleteFunctionality(self):
        allApplicationStatus = ['Applied', 'Accepted', 'I Rejected', 'They Rejected']
        jobInfo = { 'job' : 'auditor2',
            'company': 'kpmg',
            'salary': 30000,
            'jobLocation': 'glasgow',
            'jobStartDate': datetime.date(2023,9,1),
            'jobApplicationClosingDate': datetime.date(2023,4,10),
            'applicationStatus': allApplicationStatus[0],
            'notes': 'the job  pays really well; try really hard to get it'
            }
        searchFilters = { 'searchText' : '',
                    'salary': None,
                    'jobStartDate': None,
                    'applicationStatus': None,
                    'jobLocation': None
                }
        databaseHandlerObj = DatabaseHandler()
        databaseHandlerObj.addRow(jobInfo = jobInfo)
        databaseHandlerObj.addRow(jobInfo = jobInfo)
        retrievedRows = databaseHandlerObj.retrieveRows(searchFilters = searchFilters)
        idBeforeDelte = retrievedRows[-1]['id']
        databaseHandlerObj.deleteRow(id = idBeforeDelte)
        retrievedRows = databaseHandlerObj.retrieveRows(searchFilters = searchFilters)
        idAfterDelete = retrievedRows[-1]['id']
        self.assertNotEqual(idBeforeDelte, idAfterDelete)



if __name__ == "__main__":
    unittest.main() 