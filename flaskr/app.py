from flask import Flask, render_template, request
from database import DatabaseHandler                                      
                            
app = Flask(__name__)
databaseHandlerObj = DatabaseHandler()
jobInfoList = None

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    '''
    jobInofList = [ {   'id': 1,
                        'job': 'auditor', 
                        'company': 'kpmg', 
                        'salary': 50000,
                        'jobLocation': 'glasgow',
                        'jobStartDate': '2023-05-01',
                        'jobApplicationClosingDate': '2023-04-01',
                         'applicationStatus': 'Applied',
                         'notes': 'nice job'
                        }, 
                        {'id': 2,
                        'job': 'auditor2',
                         'company': 'pwc',
                          'salary': 45000,
                          'jobLocation': 'london',
                        'jobStartDate': '2023-05-01',
                        'jobApplicationClosingDate': '2023-04-01',
                         'applicationStatus': 'Applied',
                         'notes': 'nicer job'
                        } 
                ]
    '''
    global jobInfoList
    jobLocations = databaseHandlerObj.getSearchFilterLimits()['allJobLocations']
    return render_template('index.html', jobInfoList=jobInfoList,
                             jobLocations=jobLocations)


@app.route('/addJobInfo', methods=['GET'])
def addJobInfo():
    return render_template('addJobInfo.html')


@app.route('/modifyJobInfo/', methods=['GET'])
def modifyJobInfo():
    id = request.args.get('id')
    print(id)
    searchFilters = {'id': id}
    '''
    jobInfo = { 'job': 'auditor', 
                'company': 'kpmg', 
                'salary': 50000,
                'jobLocation': 'glasgow',
                'jobStartDate': '2023-05-01',
                'jobApplicationClosingDate': '2023-04-01',
                'statusApplied': '',
                'statusIReject': '',
                'statusTheyReject': 'selected',
                'statusSuccess': '',
                'notes': 'nice job',
                'startJobTrackDate': '2023-02-24',
                'modifiedJobTrackDate': '2023-02-25'
                }
    '''
    jobInfo = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
    if str(type(jobInfo)) == "<class 'list'>":
        jobInfo = jobInfo[0]
    jobInfo['statusApplied'] = ''
    jobInfo['statusIReject'] = ''
    jobInfo['statusTheyReject'] = ''
    jobInfo['statusSuccess'] = ''
    if jobInfo['applicationStatus'] == 'Applied':
        jobInfo['statusApplied'] = 'selected'
    elif jobInfo['applicationStatus'] == 'I Rejected':
        jobInfo['statusIReject'] = 'selected'
    elif jobInfo['applicationStatus'] == 'They Rejected':
        jobInfo['statusTheyReject'] = 'selected'
    elif jobInfo['applicationStatus'] == 'Succesful':
        jobInfo['statusSuccess'] = 'selected'
    return render_template('modifyJobInfo.html', jobInfo=jobInfo)


@app.route('/seeJobInfo/', methods=['GET'])
def seeJobInfo():
    id = request.args.get('id')
    print(id)
    searchFilters = {'id': id}
    '''
    jobInfo = { 'job': 'auditor', 
                'company': 'kpmg', 
                'salary': 50000,
                'jobLocation': 'glasgow',
                'jobStartDate': '2023-05-01',
                'jobApplicationClosingDate': '2023-04-01',
                'applicationStatus' : 'Success',
                'notes': 'nice job',
                'startJobTrackDate': '2023-02-24',
                'modifiedJobTrackDate': '2023-02-25'
                }
    '''
    jobInfo = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
    if str(type(jobInfo)) == "<class 'list'>":
        jobInfo = jobInfo[0]
    return render_template('seeJobInfo.html', jobInfo=jobInfo)


@app.route('/redirectIndex', methods=['POST'])
@app.route('/redirectAddJobInfo', methods=['POST'])
@app.route('/redirectModifyJobInfo', methods=['POST'])
@app.route('/redirectDeleteEntry/', methods=['GET'])
@app.route('/redirect', methods=['POST'])
def redirect():
    requestUrl = str(request.url_rule)
    urlToGet = '/index'
    global jobInfoList
    if requestUrl == '/redirectIndex':
        searchFilters = getSearchFilters()
        print(searchFilters)
        jobInfoList = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
        print(jobInfoList)
    elif requestUrl == '/redirectAddJobInfo':
        jobInfo = getAddJobInfo()
        print(jobInfo)
        databaseHandlerObj.addRow(jobInfo=jobInfo)
    elif requestUrl == '/redirectModifyJobInfo':
        modifiedJobInfo = getModifiedJobInfo()
        print(modifiedJobInfo)
        id = modifiedJobInfo['id']
        databaseHandlerObj.updateRow(id=id, modificationValues=modifiedJobInfo)
    elif requestUrl == '/redirectDeleteEntry/':
        id = request.args.get('id')
        print(id)
        databaseHandlerObj.deleteRow(id=id)
        jobInfoList = None

    return render_template('redirect.html', urlToGet=urlToGet)


def getSearchFilters():
    searchFilters = { 'id': '',
                    'searchText': request.form['searchText'],
                    'salary': { 'min': request.form['salaryMin'],
                                'max': request.form['salaryMax']
                                },
                    'jobStartDate': request.form['jobStartDate'],
                    'applicationStatus': request.form['applicationStatus'],
                    'jobLocation': request.form['jobLocation']
                    }
    return searchFilters


def getAddJobInfo():
    jobInfo = {'job': request.form['job'],
        'company': request.form['company'],
        'salary': request.form['salary'],
        'jobLocation': request.form['jobLocation'],
        'jobStartDate': request.form['jobStartDate'],
        'jobApplicationClosingDate': request.form['jobApplicationClosingDate'],
        'applicationStatus': request.form['applicationStatus'],
        'notes': request.form['notes']
        }
    return jobInfo


def getModifiedJobInfo():
    modifiedJobInfo = { 'id': request.form['id'],
                        'job': request.form['job'], 
                        'company': request.form['company'], 
                        'salary': request.form['salary'],
                        'jobLocation': request.form['jobLocation'],
                        'jobStartDate': request.form['jobStartDate'],
                        'jobApplicationClosingDate': request.form['jobApplicationClosingDate'],
                        'applicationStatus': request.form['applicationStatus'],
                        'notes': request.form['job'],
                    }
    return modifiedJobInfo


if __name__ == "__main__":
    app.config['debug'] = True
    #print(jobLocations)
    app.run()