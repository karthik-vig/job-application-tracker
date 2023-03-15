from io import BytesIO
from flask import Flask, render_template, request, send_file
from flaskwebgui import FlaskUI
import waitress
from database import DatabaseHandler                                      


class UserInterface:
    # Initialize flask and object for database handling.
    # SearchFilters was made global, so that is can presist between
    # pages and users don't have to re-enter.
    app = Flask(__name__)
    databaseHandlerObj = DatabaseHandler()
    searchFilters = None

    def __init__(self):
        guiApp = FlaskUI(server=self._startWaitress,
                        server_kwargs={
                        'app': UserInterface.app,
                        'port': 5000,
                        'host': 'localhost'
                        },
                        width=1200,
                        height=800
                        )
        guiApp.run()


    # The waitress will act as the server to improve performance.
    def _startWaitress(self, **kwargs):
        app = kwargs['app']
        host = kwargs['host']
        port = kwargs['port']
        waitress.serve(app, host=host, port=port)


    # The entry / index page.
    # Contains the search filter inputs and panel to show the results
    # for the search.
    # Also this is the page from which all other pages can be accessed.
    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    def index():
        jobInfoList = None
        resultStatDict = None
        if UserInterface.searchFilters:
            jobInfoList, resultStatDict = UserInterface.databaseHandlerObj.searchJobTrackerTableRows(searchFilters=UserInterface.searchFilters)
        jobLocations = UserInterface.databaseHandlerObj.getSearchFilterLimits()['allJobLocations']
        return render_template('index.html', jobInfoList=jobInfoList,
                                             jobLocations=jobLocations,
                                             searchFilters=UserInterface.searchFilters,
                                             resultStatDict=resultStatDict)


    # Get the page to add an new entry into the database.
    @app.route('/addJobInfo', methods=['GET'])
    def addJobInfo():
        return render_template('addJobInfo.html')


    # Get the page to modify an existing entry in the database.
    # Can modify all or spcific values (except: id, added date and modified date)
    # The files can be opened, modified or deleted.
    @app.route('/modifyJobInfo', methods=['GET'])
    def modifyJobInfo():
        id = request.args.get('id')
        jobTrackerInfo = UserInterface.databaseHandlerObj.getRowsOnID(id=id, tableName='JobTrackerTable')
        fileTrackerInfo = UserInterface.databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
        if str(type(jobTrackerInfo)) == "<class 'list'>":
            jobTrackerInfo = jobTrackerInfo[0]
        if str(type(fileTrackerInfo)) == "<class 'list'>":
            fileTrackerInfo = fileTrackerInfo[0]
        jobInfo = {}
        jobInfo.update(jobTrackerInfo)
        jobInfo.update(fileTrackerInfo)
        return render_template('modifyJobInfo.html', jobInfo=jobInfo)


    # Get the page to see information on a specific job entry.
    # Get the necessar frow from database using id.
    @app.route('/seeJobInfo', methods=['GET'])
    def seeJobInfo():
        id = request.args.get('id')
        jobTrackerInfo = UserInterface.databaseHandlerObj.getRowsOnID(id=id, tableName='JobTrackerTable')
        fileTrackerInfo = UserInterface.databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
        if str(type(jobTrackerInfo)) == "<class 'list'>": # the returned value is list of one item; to get the item this is done.
            jobTrackerInfo = jobTrackerInfo[0]
        if str(type(fileTrackerInfo)) == "<class 'list'>": # the returned value is list of one item; to get the item this is done.
            fileTrackerInfo = fileTrackerInfo[0]
        jobInfo = {}
        jobInfo.update(jobTrackerInfo)
        jobInfo.update(fileTrackerInfo)
        return render_template('seeJobInfo.html', jobInfo=jobInfo)


    # Get file resume, coverletter and extra file for download from the database
    # using a id. Which file is needed at the moment is based on the url.
    @app.route('/resumeFile/<id>', methods=['GET'])
    @app.route('/coverLetterFile/<id>', methods=['GET'])
    @app.route('/extraFile/<id>', methods=['GET'])
    def getFiles(id):
        requestUrl = str(request.url_rule)
        fileTrackerInfo = UserInterface.databaseHandlerObj.getRowsOnID(id=id, tableName='FileTrackerTable')
        if str(type(fileTrackerInfo)) == "<class 'list'>":
            fileTrackerInfo = fileTrackerInfo[0]
        if requestUrl == '/resumeFile/<id>':
            # set file name and data for resume file
            fileName = fileTrackerInfo['resumeFile']['name']
            fileData = fileTrackerInfo['resumeFile']['data']
            return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)
        if requestUrl == '/coverLetterFile/<id>':
            # set file name and data for cover letter file
            fileName = fileTrackerInfo['coverLetterFile']['name']
            fileData = fileTrackerInfo['coverLetterFile']['data']
            return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)
        if requestUrl == '/extraFile/<id>':
            # set file name and data for extra file
            fileName = fileTrackerInfo['extraFile']['name']
            fileData = fileTrackerInfo['extraFile']['data']
            return send_file(BytesIO(fileData), download_name=fileName, as_attachment=True)


    # The redirect page is used for the POST -> redirect -> GET cycle
    # as well as to collect and the form values being submitted.
    # This function collect and process information from all form submit
    # and returns to the index page.
    @app.route('/redirectIndex', methods=['POST'])
    @app.route('/redirectAddJobInfo', methods=['POST'])
    @app.route('/redirectModifyJobInfo', methods=['POST'])
    @app.route('/redirectDeleteEntry', methods=['GET'])
    @app.route('/redirect', methods=['POST'])
    def redirect():
        requestUrl = str(request.url_rule)
        urlToGet = '/index'
        if requestUrl == '/redirectIndex':
            UserInterface.searchFilters = UserInterface._getSearchFilters()
        elif requestUrl == '/redirectAddJobInfo':
            jobInfo = UserInterface._getAddJobInfo()
            UserInterface.databaseHandlerObj.addRow(jobInfo=jobInfo)
        elif requestUrl == '/redirectModifyJobInfo':
            modifiedJobInfo = UserInterface._getModifiedJobInfo()
            id = modifiedJobInfo['id']
            UserInterface.databaseHandlerObj.updateRow(id=id, modificationValues=modifiedJobInfo)
        elif requestUrl == '/redirectDeleteEntry':
            id = request.args.get('id')
            UserInterface.databaseHandlerObj.deleteRow(id=id)

        return render_template('redirect.html', urlToGet=urlToGet)


    # Construct the searchFilter dict for the database Handler Object
    def _getSearchFilters():
        searchFilters = { 
                        'searchText': request.form['searchText'],
                        'salary': { 'min': request.form['salaryMin'],
                                    'max': request.form['salaryMax']
                                    },
                        'jobStartDate': request.form['jobStartDate'],
                        'applicationStatus': request.form['applicationStatus'],
                        'jobLocation': request.form['jobLocation']
                        }
        return searchFilters


    # Construct the add job info. dict for the database Handler Object
    def _getAddJobInfo():
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


    # Construct the modified value dict for the database Handler Object
    def _getModifiedJobInfo():
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
                                        },
                            'resumeFileDelete': request.form.get('resumeFileDelete'),
                            'coverLetterFileDelete': request.form.get('coverLetterFileDelete'),
                            'extraFileDelete': request.form.get('extraFileDelete')
                        }
        return modifiedJobInfo


# In production flaskwebgui will be used along with waitress.
if __name__ == "__main__":
    userInterfaceObj = UserInterface()
