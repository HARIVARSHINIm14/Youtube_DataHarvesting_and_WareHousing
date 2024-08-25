Here's the README with the points structured as lists for better readability:

---

# YouTube Data Harvesting and Warehousing using SQL and Streamlit

## Overview
This project aims to develop a user-friendly Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application utilizes the Google YouTube API to extract detailed information about channels and videos, stores this data in a SQL database, and provides powerful search and retrieval options within the Streamlit app.

## Skills Takeaway
- **Python Scripting**
- **Data Collection**
- **Streamlit**
- **API Integration**
- **Data Management using SQL**

## Domain
- **Social Media**

## Problem Statement
The objective of this project is to create a Streamlit application with the following features:

- **Data Retrieval**: Input a YouTube channel ID and retrieve all relevant data such as channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, and comments using the Google YouTube API.
- **Data Collection**: Collect data for up to 10 different YouTube channels and store them in a data lake by clicking a button.
- **Data Storage**: Store the retrieved data in a MySQL or PostgreSQL database.
- **Data Querying**: Search and retrieve data from the SQL database using various search options, including joining tables to get comprehensive channel details.

## Approach
- **Set up a Streamlit App**: Streamlit is used to create a simple UI where users can enter a YouTube channel ID, view channel details, and select channels to migrate to the data warehouse.
- **Connect to the YouTube API**: The Google API client library for Python is used to make requests to the YouTube API and retrieve channel and video data.
- **Store and Clean Data**: Retrieved data is temporarily stored using pandas DataFrames or other in-memory structures before being migrated to the data warehouse.
- **Migrate Data to a SQL Data Warehouse**: After collecting data for multiple channels, it is migrated to a SQL database (MySQL or PostgreSQL) for storage.
- **Query the SQL Data Warehouse**: SQL queries are used to join tables and retrieve specific channel data based on user input, leveraging SQLAlchemy for database interactions.
- **Display Data in Streamlit**: The retrieved data is displayed in the Streamlit app using its data visualization features, allowing for detailed analysis through charts and graphs.

## Results
This project successfully creates a Streamlit application that enables users to extract YouTube channel data, store it in a SQL database, and perform advanced queries to retrieve and analyze the data.

## References
- **Streamlit Documentation**: [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- **YouTube API Reference**: [Google YouTube API](https://developers.google.com/youtube/v3/getting-started)
- **API Data Collection Reference**: Colab Notebook

---

This structure should make the README easier to read and follow. Let me know if you'd like to add or change anything!
