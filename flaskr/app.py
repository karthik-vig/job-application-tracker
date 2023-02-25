from flask import Flask, render_template, request
from database import DatabaseHandler                                      
                            
app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
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
    return render_template('index.html', jobInfoList=jobInofList,
                             jobLocations=['glasgow', 'edingburgh'])


@app.route('/addJobInfo', methods=['GET'])
def addJobInfo():
    return render_template('addJobInfo.html')


@app.route('/modifyJobInfo/', methods=['GET'])
def modifyJobInfo():
    id = request.args.get('id')
    print(id)
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
    return render_template('modifyJobInfo.html', jobInfo=jobInfo)


@app.route('/seeJobInfo/', methods=['GET'])
def seeJobInfo():
    id = request.args.get('id')
    print(id)
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
    return render_template('seeJobInfo.html', jobInfo=jobInfo)


@app.route('/redirectIndex', methods=['POST'])
@app.route('/redirectAddJobInfo', methods=['POST'])
@app.route('/redirectModifyJobInfo', methods=['POST'])
@app.route('/redirectDeleteEntry/', methods=['GET'])
@app.route('/redirect', methods=['POST'])
def redirect():
    requestUrl = str(request.url_rule)
    urlToGet = '/index'
    if requestUrl == '/redirectIndex':
        searchFilters = getSearchFilters()
        print(searchFilters)
    elif requestUrl == '/redirectAddJobInfo':
        jobInfo = getAddJobInfo()
        print(jobInfo)
    elif requestUrl == '/redirectModifyJobInfo':
        modifiedJobInfo = getModifiedJobInfo()
        print(modifiedJobInfo)
    elif requestUrl == '/redirectDeleteEntry/':
        id = request.args.get('id')
        print(id)

    return render_template('redirect.html', urlToGet=urlToGet)


def getSearchFilters():
    searchFilters = {'searchText': request.form['searchText'],
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
    modifiedJobInfo = { 'job': request.form['job'], 
                        'company': request.form['company'], 
                        'salary': request.form['salary'],
                        'jobLocation': request.form['jobLocation'],
                        'jobStartDate': request.form['jobStartDate'],
                        'jobApplicationClosingDate': request.form['jobApplicationClosingDate'],
                        'applicationStatus': request.form['applicationStatus'],
                        'notes': request.form['job'],
                    }
    return modifiedJobInfo