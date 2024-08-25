**YouTube Data Harvesting and Warehousing using SQL and Streamlit**

**Overview**
This project aims to develop a user-friendly Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application utilizes the Google YouTube API to extract detailed information about channels and videos, stores this data in a SQL database, and provides powerful search and retrieval options within the Streamlit app.

**Skills Takeaway**
a.Python Scripting
b.Data Collection
c.Streamlit
d.API Integration
e.Data Management using SQL

**Domain**
Social Media

**Problem Statement**
The objective of this project is to create a Streamlit application with the following features:

a.Data Retrieval: Input a YouTube channel ID and retrieve all relevant data such as channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, and comments using the Google YouTube API.
b.Data Collection: Collect data for up to 10 different YouTube channels and store them in a data lake by clicking a button.
c.Data Storage: Store the retrieved data in a MySQL or PostgreSQL database.
d.Data Querying: Search and retrieve data from the SQL database using various search options, including joining tables to get comprehensive channel details.

**Approach**
a.Set up a Streamlit App: Streamlit is used to create a simple UI where users can enter a YouTube channel ID, view channel details, and select channels to migrate to the data warehouse.
b.Connect to the YouTube API: The Google API client library for Python is used to make requests to the YouTube API and retrieve channel and video data.
c.Store and Clean Data: Retrieved data is temporarily stored using pandas DataFrames or other in-memory structures before being migrated to the data warehouse.
d.Migrate Data to a SQL Data Warehouse: After collecting data for multiple channels, it is migrated to a SQL database (MySQL or PostgreSQL) for storage.
e.Query the SQL Data Warehouse: SQL queries are used to join tables and retrieve specific channel data based on user input, leveraging SQLAlchemy for database interactions.
f.Display Data in Streamlit: The retrieved data is displayed in the Streamlit app using its data visualization features, allowing for detailed analysis through charts and graphs.

**Results**
This project successfully creates a Streamlit application that enables users to extract YouTube channel data, store it in a SQL database, and perform advanced queries to retrieve and analyze the data.

**References**
a.Streamlit Documentation: Streamlit API Reference
b.YouTube API Reference: Google YouTube API
c.API Data Collection Reference: Colab Notebook
