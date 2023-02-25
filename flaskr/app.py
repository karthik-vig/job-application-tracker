from flask import Flask, render_template, request
from database import DatabaseHandler                                      
                            
app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    jobInofList = [ {'job': 'auditor', 'company': 'kpmg', 'salary': 50000}, 
    {'job': 'auditor2', 'company': 'pwc', 'salary': 45000}]
    return render_template('index.html', jobInfoList=jobInofList,
                             jobLocations=['glasgow', 'edingburgh'])


@app.route('/addJobInfo', methods=['GET', 'POST'])
def addJobInfo():
    if request.method == 'POST':
        jobInfo = {'job': request.form['job'],
                    'company': request.form['company'],
                    'salary': request.form['salary'],
                    'jobLocation': request.form['jobLocation'],
                    'jobStartDate': request.form['jobStartDate'],
                    'jobApplicationClosingDate': request.form['jobApplicationClosingDate'],
                    'applicationStatus': request.form['applicationStatus'],
                    'notes': request.form['notes']
                    }
    return render_template('addJobInfo.html')


@app.route('/redirectIndex', methods=['POST'])
def redirect():
    requestUrl = str(request.url_rule)
    if requestUrl == '/redirectIndex':
        urlToGet = requestUrl
        searchFilters = getSearchFilters()
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
    print(searchFilters)
    return searchFilters