from io import BytesIO
from flask import Flask, render_template, request, send_file
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
        jobInfoList = databaseHandlerObj.searchJobTrackerTableRows(searchFilters=searchFilters)
    jobLocations = databaseHandlerObj.getSearchFilterLimits()['allJobLocations']
    return render_template('index.html', jobInfoList=jobInfoList,
                             jobLocations=jobLocations)


@app.route('/addJobInfo', methods=['GET'])
def addJobInfo():
    return render_template('addJobInfo.html')


@app.route('/modifyJobInfo', methods=['GET'])
def modifyJobInfo():
    id = request.args.get('id')
    jobTrackerInfo = databaseHandlerObj.getRowsOnID(id=id, tableName='JobTrackerTable')
    fileTrackerInfo = databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
    if str(type(jobTrackerInfo)) == "<class 'list'>":
        jobTrackerInfo = jobTrackerInfo[0]
    if str(type(fileTrackerInfo)) == "<class 'list'>":
        fileTrackerInfo = fileTrackerInfo[0]
    jobInfo = {}
    jobInfo.update(jobTrackerInfo)
    jobInfo.update(fileTrackerInfo)
    return render_template('modifyJobInfo.html', jobInfo=jobInfo)


@app.route('/seeJobInfo', methods=['GET'])
def seeJobInfo():
    id = request.args.get('id')
    jobTrackerInfo = databaseHandlerObj.getRowsOnID(id=id, tableName='JobTrackerTable')
    fileTrackerInfo = databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
    if str(type(jobTrackerInfo)) == "<class 'list'>":
        jobTrackerInfo = jobTrackerInfo[0]
    if str(type(fileTrackerInfo)) == "<class 'list'>":
        fileTrackerInfo = fileTrackerInfo[0]
    jobInfo = {}
    jobInfo.update(jobTrackerInfo)
    jobInfo.update(fileTrackerInfo)
    '''
    # temp. remove latter
    jobInfo['resumeFile'] = {}
    jobInfo['resumeFile']['name'] = 'temp file name'
    jobInfo['coverLetterFile'] = {}
    jobInfo['coverLetterFile']['name'] = 'temp file name'
    jobInfo['extraFile'] = {}
    jobInfo['extraFile']['name'] = 'temp file name'
    '''
    return render_template('seeJobInfo.html', jobInfo=jobInfo)


@app.route('/resumeFile/<id>', methods=['GET'])
@app.route('/coverLetterFile/<id>', methods=['GET'])
@app.route('/extraFile/<id>', methods=['GET'])
def getFiles(id):
    requestUrl = str(request.url_rule)
    fileTrackerInfo = databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
    if str(type(fileTrackerInfo)) == "<class 'list'>":
        fileTrackerInfo = fileTrackerInfo[0]
    if requestUrl == '/resumeFile/<id>':
        # code to get filename and filedata based on id for resumeFile
        fileName = fileTrackerInfo['resumeFile']['name']
        fileData = fileTrackerInfo['resumeFile']['data']
        return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)
    if requestUrl == '/coverLetterFile/<id>':
        # code to get filename and filedata based on id for coverLetterFiel
        fileName = fileTrackerInfo['coverLetterFile']['name']
        fileData = fileTrackerInfo['coverLetterFile']['data']
        return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)
    if requestUrl == '/extraFile/<id>':
        # code to get filename and filedata based on id for extraFile
        fileName = fileTrackerInfo['extraFile']['name']
        fileData = fileTrackerInfo['extraFile']['data']
        return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)

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
                'notes': request.form['notes'],
                'resumeFile': {'name': request.files['resumeFile'].filename,
                               'data': request.files['resumeFile'].read()
                               },
                'coverLetterFile': {'name': request.files['coverLetterFile'].filename,
                                    'data': request.files['coverLetterFile'].read()
                                    },
                'extraFile': {'name': request.files['extraFile'].filename,
                              'data': request.files['extraFile'].read()
                              }
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
                        'resumeFile': {'name': request.files['resumeFile'].filename,
                                        'data': request.files['resumeFile'].read()
                                        },
                        'coverLetterFile': {'name': request.files['coverLetterFile'].filename,
                                            'data': request.files['coverLetterFile'].read()
                                            },
                        'extraFile': {'name': request.files['extraFile'].filename,
                                      'data': request.files['extraFile'].read()
                                      }
                    }
    return modifiedJobInfo


if __name__ == "__main__":
    app.config['debug'] = True
    app.run()
    '''
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
    '''