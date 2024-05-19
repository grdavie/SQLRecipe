# Overview

This Personal Recipe Manager is a Python GUI application developed using Tkinter and SQLite. It allows users to add, search, delete, and update recipes within their personal recipe database. The search function enables users to search by recipe title and tags, and also filter results by the date they were added.

This project was selected to demonstrate the basics of creating a Python GUI application that interacts with a relational database, showcasing CRUD (Create, Read, Update, Delete) operations.


# Relational Database

The application uses SQLite 3 as its database system, containing a single table to manage recipes. The user interface allows users to create and manage multiple recipes.

# Development Environment

IDE: 
- Visual Studio Code
    - Version: 1.88.1 (Universal)
    - Date: 2024-04-10T17:42:52.765Z
    - Electron: 28.2.8
    - ElectronBuildId: 27744544
    - Chromium: 120.0.6099.291
    - Node.js: 18.18.2
    - V8: 12.0.267.19-electron.0
    - OS: Darwin arm64 23.3.0

Programming Language:
- Python 3.11.5
    - Sqlite 3.43.2 2023-10-10
    - tkinter
    - tkcalendar

# Useful Websites

- [Sqlite3 Python Library](https://docs.python.org/3/library/sqlite3.html)
- [Tkinter Python Library](https://docs.python.org/3/library/tkinter.html)
- [Tkcalendar Create Date Picker](https://www.geeksforgeeks.org/create-a-date-picker-calendar-tkinter/)

# Future Work

- Improve the GUI appearance and add scrolling functionality
- Create an additional table to store user information, enabling multiple users to collaborate and track changes
- Implement an API to allow users to search for and store external recipes
