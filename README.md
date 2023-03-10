# Job Application Tracker
An application for keep tracker of jobs applied and what files where used to apply to those jobs. The data is stored locally on the system in the form of a sqlite database.

# Content:
1. Requirements
    1. Python Packages
    2. Necessary Installations
2. Usage Manual
3. Data Structures
4. Function Description
5. Overall Program Structure
6. References


# Requirements:

This section covers the python interpretor and packages necessary to run the source code.

## Python Packages:

The list of necessary packages are as follows:

- altgraph==0.17.3
- auto-py-to-exe==2.32.0
- bottle==0.12.25
- bottle-websocket==0.2.9
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
- pythonnet==3.0.1
- pywebview==4.0.2
- pywin32-ctypes==0.2.0
- SQLAlchemy==2.0.4
- typing_extensions==4.5.0
- waitress==2.1.2
- Werkzeug==2.2.3
- whichcraft==0.6.1
- zipp==3.14.0
- zope.event==4.6
- zope.interface==5.5.2

The main packages to be installed are: Flask, waitress, SQLAlchemy, Flaskwebgui. Other packages such as pyinstaller and auto-py-to-exe were used to package the application as a exe file. The application was made using python 3.9.13.

## Necessary Installations:

For the application to work lastest edge runtime has to be installed in the windows machine. This should be an issue for windows 10 and 11. However, for old version of windows it maybe required to perform a manual installation of the edge runtime.


# Usage Manual

The landing page is the index page. This page is the entry point of the program, as well as the page that exclusively leads to other pages for the purpose of adding an entry, modifying an existing entry or getting the information in an existing entry. The index page also provides the search functionality, along with the search results pane.
