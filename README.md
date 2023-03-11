# Job Application Tracker
An application for keep tracker of jobs applied and what files where used to apply to those jobs. The data is stored locally on the system in the form of a sqlite database.

# Content:
1. Requirements
    1. Python Packages
    2. Necessary Installations
2. User Manual
    1. Index Page
    2. Add Job Information Page
    3. Modify Job Information page
    4. See Job Infromation page
4. Data Structures
5. Function Description
6. Overall Program Structure
7. References


# Requirements:

This section covers the python interpretor and packages necessary to run the source code.

## Python Packages:

The list of necessary packages are as follows:

- altgraph==0.17.3
- auto-py-to-exe==2.32.0
- cffi==1.15.1
- click==8.1.3
- clr-loader==0.2.5
- colorama==0.4.6
- Eel==0.14.0
- Flask==2.2.3
- flaskwebgui==1.0.3
- future==0.18.3
- gevent==22.10.2
- gevent-websocket==0.10.1
- greenlet==2.0.2
- importlib-metadata==6.0.0
- itsdangerous==2.1.2
- Jinja2==3.1.2
- MarkupSafe==2.1.2
- pefile==2023.2.7
- proxy-tools==0.1.0
- psutil==5.9.4
- pycparser==2.21
- pyinstaller==5.8.0
- pyinstaller-hooks-contrib==2023.0
- pyparsing==3.0.9
- pywin32-ctypes==0.2.0
- SQLAlchemy==2.0.4
- typing_extensions==4.5.0
- waitress==2.1.2
- Werkzeug==2.2.3
- whichcraft==0.6.1
- zipp==3.14.0
- zope.event==4.6
- zope.interface==5.5.2

The main packages to be installed are: Flask, waitress, SQLAlchemy, Flaskwebgui. Other packages such as pyinstaller and auto-py-to-exe were used to package the application as an exe file. The application was made using python 3.9.13.

## Necessary Installations:

For the application to work lastest edge runtime has to be installed in the windows machine. This should be an issue for windows 10 and 11. However, for old version of windows it maybe required to perform a manual installation of the edge runtime.


# User manual:

This section deals with the usage of the job application tracker software for the end user. It explains the assumptions and usage for each of its interactive elements.

## Index Page:

The landing page is the index page. This page is the entry point of the program, as well as the page that exclusively leads to other pages for the purpose of adding an entry, modifying an existing entry or getting the information in an existing entry. The index page also provides the search functionality, along with the search results pane.

![indexPage](https://user-images.githubusercontent.com/113319059/224440927-5ef57239-ae91-43f2-8754-0a6a3ab81b6c.png)
Figure 1. The Main / Index page

### Search Filter Pane:

The search filter pane contains all the options to find a specific entry in the application. The "search box" does a case insensitive comparisson for job and company values only and not other values. The "Job Start After" filter finds the entry with a job start date that is equivalent or after the entred value in this field. The "Salary" filter can be used with either min or max or both. It finds the entries with values equivalent or greater than the min and less or equal to the max. The "Status" field is a list with options. We can select a application status here to search based on it. They possible values are: "Applied", "They Rejected", "I Rejected" and "Successful". The "Job Loation" field is a text box where we can either enter the entire location or a parat of it. Then it is compared in a case insensitive manner with the database. We can mix and match any combination of the search filter inputs to search. When searching with empty values in all the search filter fields, the application shows the entries in the order they were entered.

### Search Result Pane:

This pane contains the result of the search as cards. Each card is an added Entry. The card contains information to see at a glance like the job, company, salary and status. It also contains buttons to modify the information in the card, see all the information about the entry or delete the entry.

## Add Job Information Page:

This page contains the fields: job, company, salary, location, job start date, job application closing date, status, notes, resume file, cover letter file, extra file. These fields are type locked as appropriate. The salary fields only takes in integer value. The fields relating to date only take date as an input. The file fields allow us to choose and add files to be locally stored in the database. The reset button for each file entry can be used to clear the current file selection. All the fields can be empty and entry can still be added into the database.

![addJobInfoPage](https://user-images.githubusercontent.com/113319059/224444910-e76fd000-fb6e-4954-8000-50458db1de53.png)
Figure 2. The Add Job Information Page

## See Job Information Page:

This page allows the information in a job entry to be safely seen without the risk of altering the information by mistake. Everything in this page is readonly. Missing values are displayed as empty fields and in the case of the files, it is shown as "No File.". If the files exist then they can be retrieved from the database and opened by clicking the "Open" button in the respective file fields. This page also contains additional information about the entry, namely the "added date" and the "last modified date" fields. 

![seeJobInfoPage](https://user-images.githubusercontent.com/113319059/224445278-442d8c7e-b52e-47fa-b9a7-12d9bf3de233.png)
Figure 3. The See Job Information Page

## Modify Job Information Page:

This page allows for the modification of existing job entries. This page is very similar to "See Job Information Page", but the fields are modifiable. Once, again the fields contain type check (same as "Add Job Information Page"). However, the fields "added date" and "last modified date" are not modifiable. The three file fields: "Resume File", "Cover Letter File" and "Extra File" there are three buttons and one checkbox. The choose button is used to select a new file to be upload as a replacement to the existing or missing file. The reset button clears any chosen file. The open button does not open the currently chosen file, but the file in the database (if it exist, else "No File." is shown in the place of "Open" button). The Delete checkbox when marked will delete the file in the database.

![modifyJobInfoPage](https://user-images.githubusercontent.com/113319059/224447570-a0e65eae-ccff-4853-864b-843008798d91.png)
Figure 4. Modify Job Information Page

NOTE: only one operation can be done with regards to a given file field (where, one file field is either "Resume File" or "Cover Letter File" or "Extra File"). That is, either a new file can be inserted or the old file (if exist) can be deleted, not both at the same time.

# Data Structures:

This section covers the data structures concerned with moving information between functions and classes. The data structures to be discussed the one used to send search filter parameters, add job infomation to the database, modify the job information, and get information from the database for a query.

### Add New Information Into the Database:

- Name: jobInfo
- Input Parameter For: addRow() in DatabaseHandler class.
- Returned By: None

|Field Name                 |Field Data Type         | Description                                                                                          |
|---------------------------|------------------------|------------------------------------------------------------------------------------------------------|
|job                        |str                     |It can be a empty str or some other string value                                                      |
|company                    |str                     |It can be a empty str or some other string value                                                      |
|salary                     |str                     |It should only contain a string of a integer                                                          |
|jobLocation                |str                     |It can be a empty str or some other string value                                                      |
|jobStartDate               |str                     |It can only be a str of international date format eg: "2023-09-01"                                    |
|jobApplicationClosingDate  |str                     |It can only be a str of international date format eg: "2023-09-01"                                    |
|applicationStatus          |str                     |It can be any string but only 'Applied', 'They Rejected', 'I Rejected' or 'Successful' are considered |
|notes                      |str                     |It can be a empty str or some other string value                                                      |
|resumeFile                 |dict                    |It contains the resume file name and file data as fields                                              |
|coverLetterFile            |dict                    |It contains the cover letter file name and file data as fields                                        |
|extraFile                  |dict                    |It contains the extra file name and file data as fields                                               |

- Name: resumeFile / coverLetterFile / extraFile
- Input Parameter for: Used as a part of various data structures to move file name and data.
- Returned By: None

|Field Name                 |Field Data Type         | Description                                                       |
|---------------------------|------------------------|-------------------------------------------------------------------|
|name                       |str                     |It can only be a str, can be a empty str                           |
|data                       |bytes                   |It can only be bytes with some value or a empty bytes value        |

- Example:
```
{'job': 'test job',
'company': 'test company',
'salary': '30000',
'jobLocation': 'london',
'jobStartDate': '2023-09-01',
'jobApplicationClosingDate': '2023-08-01',
'applicationStatus': 'Applied',
'notes': 'nice job',
'resumeFile': {'name': 'resume file name.pdf',
               'data': b'adfsfdadfsf'
               },
'coverLetterFile': {'name': 'cover letter file.pdf',
                    'data': b'sdafasdfsadf'
                    },
'extraFile': {'name': 'extra file name.pdf',
              'data': b'sdfsdfsfasdfas'
              }
}
```

### Add Modified information into the database:

- Name: modificationValues
- Input Parameter For: updateRow() in DatabaseHandler class.
- Returned By: None

|Field Name                 |Field Data Type         | Description                                                                                          |
|---------------------------|------------------------|------------------------------------------------------------------------------------------------------|
|job                        |str                     |It can be a empty str or some other string value                                                      |
|company                    |str                     |It can be a empty str or some other string value                                                      |
|salary                     |str                     |It should only contain a string of a integer                                                          |
|jobLocation                |str                     |It can be a empty str or some other string value                                                      |
|jobStartDate               |str                     |It can only be a str of international date format eg: "2023-09-01"                                    |
|jobApplicationClosingDate  |str                     |It can only be a str of international date format eg: "2023-09-01"                                    |
|applicationStatus          |str                     |It can be any string but only 'Applied', 'They Rejected', 'I Rejected' or 'Successful' are considered |
|notes                      |str                     |It can be a empty str or some other string value                                                      |
|resumeFile                 |dict                    |It contains the resume file name and file data as fields                                              |
|coverLetterFile            |dict                    |It contains the cover letter file name and file data as fields                                        |
|extraFile                  |dict                    |It contains the extra file name and file data as fields                                               |
|resumeFileDelete           |str / None              |Only when the str value is 'on', it is actually used or else it is taken as false                     |
|coverLetterFileDelete      |str / None              |Only when the str value is 'on', it is actually used or else it is taken as false                     |
|extraFileDelete            |str / None              |Only when the str value is 'on', it is actually used or else it is taken as false                     |


- Name: resumeFile / coverLetterFile / extraFile
- Input Parameter for: Used as a part of various data structures to move file name and data.
- Returned By: None

|Field Name                 |Field Data Type         | Description                                                       |
|---------------------------|------------------------|-------------------------------------------------------------------|
|name                       |str                     |It can only be a str, can be a empty str                           |
|data                       |bytes                   |It can only be bytes with some value or a empty bytes value        |

- Example:
```
{'job': 'test job',
'company': 'test company',
'salary': '30000',
'jobLocation': 'london',
'jobStartDate': '2023-09-01',
'jobApplicationClosingDate': '2023-08-01',
'applicationStatus': 'Applied',
'notes': 'nice job',
'resumeFile': {'name': 'resume file name.pdf',
               'data': b'adfsfdadfsf'
               },
'coverLetterFile': {'name': 'cover letter file.pdf',
                    'data': b'sdafasdfsadf'
                    },
'extraFile': {'name': 'extra file name.pdf',
              'data': b'sdfsdfsfasdfas'
              },
'resumeFileDelete': 'on',
'coverLetterFileDelete': 'on',
'extraFileDelete': 'on'
}
```