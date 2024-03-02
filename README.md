# Youtube_DataHarvesting_and_WareHousing
📊YouTube Data Harvest: Explores YouTube trends using Python, MySQL, MongoDB, and Streamlit. Gather data efficiently, store it smartly, and visualize insights easily
Youtube channel details are retrieved using Youtube data API application after getting the key from it . We are processing the channel details using PYTHON programming language, Where it imports various libraries for the given Project such as,

1.from googleapiclient.discovery import build - This library is part of the Google API Client library and is used for interacting with various Google services, such as YouTube in your case. It allows you to create a service object for making API requests and fetching data from Google services.

2.from pymongo import MongoClient - PyMongo is a Python driver for MongoDB, a NoSQL database. It provides a convenient way to interact with MongoDB databases, allowing you to perform operations like inserting, updating, querying, and deleting documents in a MongoDB collection.

3.import mysql.connector - This library provides a Python interface for interacting with MySQL databases. It allows you to connect to a MySQL server, execute SQL queries, and manage database transactions.

4.import pandas as pd - Pandas is a powerful data manipulation library for Python. It provides data structures like DataFrames, which are efficient for handling and analyzing structured data. Pandas simplifies tasks such as cleaning, filtering, aggregating, and visualizing data.

5.from datetime import datetime,timedelta - The datetime module in Python provides classes for working with dates and times. It allows you to create, manipulate, and format dates and times. In your code, it seems to be used for handling date-related operations.The timedelta class is a part of the datetime module in Python and represents the duration or the difference between two dates or times.

6.import streamlit as st - Streamlit is a Python library used for creating web applications with minimal effort. It is particularly well-suited for creating data-centric applications. Streamlit allows you to turn data scripts into shareable web apps quickly, making it easy to visualize and interact with data.

7.import re - The re module is the regular expression module in Python. It provides functions for working with regular expressions, which are powerful tools for pattern matching in strings. In your code, it might be used for string manipulation or validation.

after extracting it , it is saved in MongoDB and then transefered to SQL. once it is all done then finally it is deployed in streamlit application.
