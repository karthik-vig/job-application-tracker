from flask import Flask, render_template, request
from database import DatabaseHandler                                      
                            
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    jobInofList = [ {'job': 'auditor', 'company': 'kpmg', 'salary': 50000}, 
    {'job': 'auditor2', 'company': 'pwc', 'salary': 45000}]
    #'''
    if request.method == 'POST':
        searchFilters = {'searchText': request.form['searchText'],
                        'salary': { 'min': request.form['salaryMin'],
                                    'max': request.form['salaryMax']
                                    },
                        'jobStartDate': request.form['jobStartDate'],
                        'applicationStatus': request.form['applicationStatus'],
                        'jobLocation': request.form['jobLocation']
                        }
    #'''
    print(searchFilters)
    return render_template('index.html', jobInfoList=jobInofList,
                             jobLocations=['glasgow', 'edingburgh'])