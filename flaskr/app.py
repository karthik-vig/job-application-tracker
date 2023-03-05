from flask import Flask, render_template, request
from flaskwebgui import FlaskUI
import waitress
from database import DatabaseHandler                                      
                            
app = Flask(__name__)
databaseHandlerObj = DatabaseHandler()
searchFilters = None

def startFlask(**kwargs):
    app = kwargs['app']
    host = kwargs['host']
    port = kwargs['port']
    waitress.serve(app, host=host, port=port)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    global searchFilters
    jobInfoList = None
    if searchFilters:
        jobInfoList = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
    jobLocations = databaseHandlerObj.getSearchFilterLimits()['allJobLocations']
    return render_template('index.html', jobInfoList=jobInfoList,
                             jobLocations=jobLocations)


@app.route('/addJobInfo', methods=['GET'])
def addJobInfo():
    return render_template('addJobInfo.html')


@app.route('/modifyJobInfo', methods=['GET'])
def modifyJobInfo():
    id = request.args.get('id')
    searchFilters = {'id': id}
    jobInfo = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
    if str(type(jobInfo)) == "<class 'list'>":
        jobInfo = jobInfo[0]
    return render_template('modifyJobInfo.html', jobInfo=jobInfo)


@app.route('/seeJobInfo', methods=['GET'])
def seeJobInfo():
    id = request.args.get('id')
    searchFilters = {'id': id}
    jobInfo = databaseHandlerObj.retrieveRows(searchFilters=searchFilters)
    if str(type(jobInfo)) == "<class 'list'>":
        jobInfo = jobInfo[0]
    return render_template('seeJobInfo.html', jobInfo=jobInfo)


@app.route('/redirectIndex', methods=['POST'])
@app.route('/redirectAddJobInfo', methods=['POST'])
@app.route('/redirectModifyJobInfo', methods=['POST'])
@app.route('/redirectDeleteEntry', methods=['GET'])
@app.route('/redirect', methods=['POST'])
def redirect():
    requestUrl = str(request.url_rule)
    urlToGet = '/index'
    global searchFilters
    if requestUrl == '/redirectIndex':
        searchFilters = getSearchFilters()
    elif requestUrl == '/redirectAddJobInfo':
        jobInfo = getAddJobInfo()
        databaseHandlerObj.addRow(jobInfo=jobInfo)
    elif requestUrl == '/redirectModifyJobInfo':
        modifiedJobInfo = getModifiedJobInfo()
        id = modifiedJobInfo['id']
        databaseHandlerObj.updateRow(id=id, modificationValues=modifiedJobInfo)
    elif requestUrl == '/redirectDeleteEntry':
        id = request.args.get('id')
        databaseHandlerObj.deleteRow(id=id)

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
                        'notes': request.form['notes'],
                    }
    return modifiedJobInfo


if __name__ == "__main__":
    guiApp = FlaskUI(server=startFlask,
                    server_kwargs={
                    'app': app,
                    'port': 5000,
                    'host': '0.0.0.0'
                    },
                    width=1200,
                    height=800
                    )
    guiApp.run()