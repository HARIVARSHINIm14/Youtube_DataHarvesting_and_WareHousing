#libraries
from googleapiclient.discovery import build
from pymongo import MongoClient
import mysql.connector 
import pandas as pd
from datetime import datetime,timedelta
import streamlit as st
import re


api_key = 'AIzaSyDOnFiW_rjgZw0QDxP7AVb_sPVT-VKu8_Q'
youtube = build('youtube', 'v3', developerKey=api_key)
#AIzaSyDOnFiW_rjgZw0QDxP7AVb_sPVT-VKu8_Q

#channel id details
def channel_info(channel_id):
    api_key = 'AIzaSyBUXV5TdB6IKZRnGxX1Hr798CVM_rfzA8Q'
    youtube = build("youtube", "v3", developerKey=api_key)

    response = youtube.channels().list(
        id=channel_id,
        part='snippet,statistics,contentDetails'
    )

    channel_data = response.execute()
    for i in channel_data['items']:
        data=dict(Channel_Name=i['snippet']['title'],
                Channel_Id=i['id'],
                Subscribers=i['statistics']['subscriberCount'],
                Views=i['statistics']['viewCount'],
                Total_Videos=i['statistics']['videoCount'],
                Channel_Description=i['snippet']['description'],
                Playlist_Id=i['contentDetails']['relatedPlaylists']['uploads']
                )
    return data

#playlist information
def channel_playlist(channel_ids):
    next_page_token = None
    
    playlist = []

    while True:
        request = youtube.playlists().list(
                part='snippet,contentDetails',
                channelId=channel_ids,
                maxResults=50,
                pageToken=next_page_token
        )
        channel_data = request.execute()

        for item in channel_data['items']:
            data = dict(
                Playlist_Id=item['id'],
                Title=item['snippet']['title'],
                Channel_Id=item['snippet']['channelId'],
                Channel_Name=item['snippet']['channelTitle'],
                PublishedAt=item['snippet']['publishedAt'],
                Video_Count=item['contentDetails']['itemCount']
            )
            playlist.append(data)
        
        next_page_token = channel_data.get('nextPageToken')
        if next_page_token is None:
            break

    return playlist

#video details
def channel_vids(channel_id):
    videos=[]
    channel_data=youtube.channels().list(id=channel_id,part='contentDetails').execute()
    Playlist_Id=channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_PageToken = None 
    while True:
        channel_data1=youtube.playlistItems().list(part='snippet',playlistId=Playlist_Id,maxResults=50,pageToken=next_PageToken).execute()
        for i in range(len(channel_data1['items'])):
            videos.append(channel_data1['items'][i]['snippet']['resourceId']['videoId'])
        next_PageToken=channel_data1.get('nextPageToken')
    #if all videos are retrieved at the end no video then break the while loop
        if next_PageToken is None:
            break
    return videos

#to get all vidoes
def channel_videos(videos):
    video_data = []
    for video_s in videos:
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_s
        )
        channel_id = request.execute()

        for item in channel_id["items"]:
            data = dict(
                Channel_Name=item['snippet']['channelTitle'],
                Channel_Id=item['snippet']['channelId'],
                Video_Id=item['id'],
                Title=item['snippet']['title'],
                Tags=item['snippet'].get('tags'),
                Thumbnails=item['snippet']['thumbnails']['default']['url'],
                Description=item['snippet'].get('description'),
                Published_date=item['snippet']['publishedAt'],
                Duration=item['contentDetails']['duration'],
                Views=item['statistics'].get('viewCount'),
                Likes=item['statistics'].get('likeCount'),
                Comments=item['statistics'].get('commentCount'),
                Favourite_Count=item['statistics']['favoriteCount'],
                Definition=item['contentDetails']['definition'],
                Caption=item['contentDetails']['caption']
            )
            video_data.append(data)
    return video_data


#comments details
def channel_comments(videos):
    Comment_data=[]
    try:
        for video_id in videos:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50
            )
            channel_data = request.execute()
            for item in channel_data['items']:
                data = dict(
                    Comment_Id=item['snippet']['topLevelComment']['id'],
                    Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'],
                    Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    Comment_Published=item['snippet']['topLevelComment']['snippet']['publishedAt']
                )
                Comment_data.append(data)
    except:
        pass
    return Comment_data
#mongo connections
connections=MongoClient("mongodb://localhost:27017")
db = connections['Youtube_data']
def channels(channel_id):
    ch_detail=channel_info(channel_id)
    ch_playlist=channel_playlist(channel_id)
    ch_videoid=channel_vids(channel_id)
    ch_video=channel_videos( ch_videoid)
    ch_comment=channel_comments( ch_videoid)
    col=db['channels']
    col.insert_one({"channel_information":ch_detail,"playlist_information":ch_playlist,"video_information":ch_video,"comment_information":ch_comment})
    return "upload completed successfully"
    

#table creation, playlist, videos, comments
def channeli_table():
    mydb = mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="12345",
                                    database="you_tube")
    mycursor = mydb.cursor()
  
    try:
        create_query ='''create table if not exists channeli(Channel_Name varchar(100),
                                                                Channel_Id varchar(80) primary key,
                                                                Subscribers bigint,
                                                                Views bigint,
                                                                Total_Videos int,
                                                                Channel_Description text,
                                                                Playlist_Id varchar(100))'''
        

        mycursor.execute(create_query)
        mydb.commit()
    except:
        print("channel tables are created")

    ch_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for ch_data in col.find({},{'_id':0,'channel_information':1}):
        ch_list.append(ch_data['channel_information'])
    df=pd.DataFrame(ch_list)   


    for index,row in df.iterrows():
        inser_query='''insert ignore into channeli(Channel_Name,
                                                    Channel_Id,
                                                    Subscribers,
                                                    Views,
                                                    Total_Videos,
                                                    Channel_Description,
                                                    Playlist_Id)
                                                    
                                                    values(%s,%s,%s,%s,%s,%s,%s)'''
        values=(row['Channel_Name'],
                row['Channel_Id'],
                row['Subscribers'],
                row['Views'],
                row['Total_Videos'],
                row['Channel_Description'],
                row['Playlist_Id'])
        try:
            mycursor.execute(inser_query,values)
            mydb.commit()
        except:
            print("values are inserted")


#playlist information
def channeli_playlist():
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="12345",
                                database="you_tube")
    mycursor = mydb.cursor()   

    create_query ='''create table if not exists playlisti(Playlist_Id varchar(100) primary key,
                                                            Title varchar(100),
                                                            Channel_Id varchar(100),
                                                            Channel_Name varchar(100),
                                                            PublishedAt timestamp,
                                                            Video_Count int)'''


    mycursor.execute(create_query)
    mydb.commit()
    pl_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for pl_data in col.find({},{'_id':0,'playlist_information':1}):
        for i in range(len(pl_data['playlist_information'])):
            pl_list.append(pl_data['playlist_information'][i])
    df1=pd.DataFrame(pl_list)
    

    for index,row in df1.iterrows():
            published_at = datetime.strptime(row['PublishedAt'], '%Y-%m-%dT%H:%M:%SZ')#used to convert string into date time object 

            formatted_published_at = published_at.strftime('%Y-%m-%d %H:%M:%S')#data time object is then changed based on format used in strftime

            
            inser_query='''insert ignore into playlisti(Playlist_Id,
                                                Title,
                                                Channel_Id,
                                                Channel_Name,
                                                PublishedAt,
                                                Video_Count)
                                                
                                                
                                                values(%s,%s,%s,%s,%s,%s)'''
            
            
            values=(row['Playlist_Id'],
                    row['Title'],
                    row['Channel_Id'],
                    row['Channel_Name'],
                    formatted_published_at,
                    row['Video_Count'])
        
            mycursor.execute(inser_query,values)
            mydb.commit()
    


#video n comment details
# video details
# Modify the channeli_video function
def channeli_video():
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345", database="you_tube")
    mycursor = mydb.cursor()
    create_query = '''create table if not exists videosi(
                        Channel_Name varchar(100),
                        Channel_Id varchar(100),
                        Video_Id varchar(30) primary key,
                        Title varchar(150),
                        Tags text,
                        Thumbnails varchar(200),
                        Description text,
                        Published_date timestamp,
                        Duration time,
                        Views bigint,
                        Likes bigint,
                        Comments int,
                        Favourite_Count int,
                        Definition varchar(20),
                        Caption varchar(50)
                    )'''

    mycursor.execute(create_query)
    mydb.commit()

    vi_list = []
    db = connections['Youtube_data']
    col = db['channels']

    for vi_data in col.find({}, {'_id': 0, 'video_information': 1}):
        for i in range(len(vi_data['video_information'])):
            vi_list.append(vi_data['video_information'][i])

    df2 = pd.DataFrame(vi_list)
    
    for index, row in df2.iterrows():
        tags_str = ', '.join(row['Tags']) if isinstance(row['Tags'], list) else str(row['Tags'])#separating tags using commas

        # Handling duration format PT10M5S
        duration_str = row['Duration']
        duration = timedelta()

        if 'H' in duration_str:
            hours_part = duration_str.split('H')[0].lstrip('PT')
            duration += timedelta(hours=int(hours_part))

        if 'M' in duration_str:
            minutes_part = duration_str.split('H')[-1].split('M')[0].lstrip('PT')
            duration += timedelta(minutes=int(minutes_part))

        if 'S' in duration_str:
            seconds_part = duration_str.split('M')[-1].split('S')[0].lstrip('PT')
            duration += timedelta(seconds=int(seconds_part))

        # Removing the 'Z' from the Published_date
        published_date_str = re.sub(r'[^0-9T:-]', '', row['Published_date'])#removing the speacial character
        published_date = datetime.strptime(published_date_str, '%Y-%m-%dT%H:%M:%S')

        if row['Views'] is not None:
            row['Views'] = int(row['Views'])

        inser_query = '''insert ignore into videosi(Channel_Name,
                                                    Channel_Id,
                                                    Video_Id,
                                                    Title,
                                                    Tags,
                                                    Thumbnails,
                                                    Description,
                                                    Published_date,
                                                    Duration,
                                                    Views,
                                                    Likes,
                                                    Comments,
                                                    Favourite_Count,
                                                    Definition,
                                                    Caption)
                            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        values = (row['Channel_Name'],
                  row['Channel_Id'],
                  row['Video_Id'],
                  row['Title'],
                  tags_str,
                  row['Thumbnails'],
                  row['Description'],
                  published_date,
                  duration,
                  row['Views'],
                  row['Likes'],
                  row['Comments'],
                  row['Favourite_Count'],
                  row['Definition'],
                  row['Caption'])

        mycursor.execute(inser_query, values)
        mydb.commit()


        

#comment informations
def channeli_comment():
    mydb = mysql.connector.connect(host="localhost",
                                            user="root",
                                            password="12345",
                                            database="you_tube")
    mycursor = mydb.cursor()  
    create_query ='''create table if not exists commenti(Comment_Id varchar(100) primary key,
                                                        Video_Id varchar(50),
                                                        Comment_Text text,
                                                        Comment_Author varchar(150),
                                                        Comment_Published timestamp)'''
        
        
    mycursor.execute(create_query)
    mydb.commit()


    com_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for com_data in col.find({},{'_id':0,'comment_information':1}):
        for i in range(len(com_data['comment_information'])):
            com_list.append(com_data['comment_information'][i])
    df3=pd.DataFrame(com_list)

    for index, row in df3.iterrows():
        inser_query = '''insert ignore into commenti(Comment_Id,
                                            Video_Id,
                                            Comment_Text,
                                            Comment_Author,
                                            Comment_Published)
                        values(%s,%s,%s,%s,%s)'''

        # Convert Comment_Published to MySQL datetime format
        formatted_comment_published = datetime.strptime(row['Comment_Published'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')

        values = (row['Comment_Id'],
                row['Video_Id'],
                row['Comment_Text'],
                row['Comment_Author'],
                formatted_comment_published)  # Use the formatted datetime here

        
        mycursor.execute(inser_query, values)
        mydb.commit()

#all channels
def tab():
    channeli_table()
    channeli_playlist()
    channeli_video()
    channeli_comment()
    return "tables are created successfully"

#to show all the details
#1.channels
def show_channel():
    ch_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for ch_data in col.find({},{'_id':0,'channel_information':1}):
        ch_list.append(ch_data['channel_information'])
    df=st.dataframe(ch_list)  

    return df 

#2.Playlist
def show_playlist():
    pl_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for pl_data in col.find({},{'_id':0,'playlist_information':1}):
        for i in range(len(pl_data['playlist_information'])):
            pl_list.append(pl_data['playlist_information'][i])
    df1=st.dataframe(pl_list)
    return df1
#3.Viedos
def show_video():
    vi_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for vi_data in col.find({},{'_id':0,'video_information':1}):
        for i in range(len(vi_data['video_information'])):
            vi_list.append(vi_data['video_information'][i])
    df2=st.dataframe(vi_list)

    return df2
#4.Comments
def show_comment():
    com_list=[]
    db = connections['Youtube_data']
    col=db['channels']
    for com_data in col.find({},{'_id':0,'comment_information':1}):
        for i in range(len(com_data['comment_information'])):
            com_list.append(com_data['comment_information'][i])
    df3=st.dataframe(com_list)

    return df3
#displaying it in Streamlit(side bars)
with st.sidebar:
    st.header("YouTube Data Harvesting and Warehousing :")
    st.caption("Explores YouTube trends using Python, MySQL, MongoDB, and Streamlit. Gather data efficiently, store it smartly, and visualize insights easily")
    st.title(":black[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    st.header("Skill Gained: ")
    st.caption("Scripting in Python")
    st.caption("Data Collection")
    st.caption("MongoDB")
    st.caption("API integration")
    st.caption("Data Management using MongoDB and SQL")


channel_identity=st.text_input("Enter the channel ID")#channel id
#button
if st.button("Collect and Store Data in the Database:"):
    ch_iden=[]#ch_ids
    db = connections['Youtube_data']
    col=db['channels']
    for ch_data in col.find({},{'_id':0,'channel_information':1}):
        ch_iden.append(ch_data['channel_information']['Channel_Id'])
    if channel_identity in ch_iden:
        st.success("Channel details of the given channel id already existed")
    else:
        insert=channels(channel_identity)
        st.success(insert)
#button
if st.button("Move to SQL"):
    status=tab()
    st.write(status)
#radio buttons
show_table=st.radio("Select the table for displaying :",("Channels","Playlists","Videos","Comments"))

if show_table=="Channels":
    show_channel()

elif show_table=="Playlists":
    show_playlist()

elif show_table == "Videos":
    show_video()

elif show_table=="Comments":
    show_comment()

#sqlconnections
mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="12345",
                                database="you_tube")
mycursor = mydb.cursor()
#answering the questions using dropdown feature
question=st.selectbox("Choose your question",("1.What are the names of all the videos and their corresponding channels?",
                                              "2.Which channels have the most number of videos, and how many videos do they have?",
                                              "3.What are the top 10 most viewed videos and their respective channels?",
                                              "4.How many comments were made on each video, and what are their corresponding video names?",
                                              "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                                              "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                              "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                                              "8.What are the names of all the channels that have published videos in the year 2022?",
                                              "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                              "10.Which videos have the highest number of comments, and what are their corresponding channel names?"))

if question=="1.What are the names of all the videos and their corresponding channels?":
    query_1='''SELECT title AS videos, channel_name AS channelname FROM videosi'''
    mycursor.execute(query_1)
    t1=mycursor.fetchall()
    df_1=pd.DataFrame(t1,columns=['Video Name','Channel Name'])
    st.write(df_1)

elif question=="2.Which channels have the most number of videos, and how many videos do they have?":
    query_2='''select channel_name as channelname,total_videos as no_videos from channeli
    order by total_videos desc'''   
    mycursor.execute(query_2)
    t2=mycursor.fetchall()
    df_2=pd.DataFrame(t2,columns=['Channel Name','No of Videos'])
    st.write(df_2)

elif question=="3.What are the top 10 most viewed videos and their respective channels?":
    query_3='''select views as views, channel_name as channelname, title as videotitle from videosi 
    where views is not null order by views desc limit 10'''   
    mycursor.execute(query_3)
    t3=mycursor.fetchall()
    df_3=pd.DataFrame(t3,columns=['Views','Channel Name','Video Title'])
    st.write(df_3)

elif question=="4.How many comments were made on each video, and what are their corresponding video names?":
    query_4='''select comments as no_comments, title as videotitle from videosi where comments is not null'''   
    mycursor.execute(query_4)
    t4=mycursor.fetchall()
    df_4=pd.DataFrame(t4,columns=['No of Comments','Video Title'])
    st.write(df_4)

elif question=="5.Which videos have the highest number of likes, and what are their corresponding channel names?":
    query_5='''select title as videotitle,channel_name as channelname, likes as likecount
                from videosi where likes is not null order by likes desc'''   
    mycursor.execute(query_5)
    t5=mycursor.fetchall()
    df_5=pd.DataFrame(t5,columns=['Video Title','Channel Name','Like Count'])
    st.write(df_5)

elif question=="6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
    query_6='''select likes as likecount, title as videotitle from videosi'''   
    mycursor.execute(query_6)
    t6=mycursor.fetchall()
    df_6=pd.DataFrame(t6,columns=['Like Count','Video Title'])
    st.write(df_6)

elif question== "7.What is the total number of views for each channel, and what are their corresponding channel names?":
    query_7='''select channel_name as channelanme, views as totalviews from channeli'''   
    mycursor.execute(query_7)
    t7=mycursor.fetchall()
    df_7=pd.DataFrame(t7,columns=['Channel Name','Total Views'])
    st.write(df_7)

elif question=="8.What are the names of all the channels that have published videos in the year 2022?" :                                        
    query_8='''select title as video_title,published_date as videorelease,channel_name as channelname from videosi where extract(year from published_date)=2022'''   
    mycursor.execute(query_8)
    t8=mycursor.fetchall()
    df_8=pd.DataFrame(t8,columns=['Video Title','Published Date','Channel Name'])
    st.write(df_8)

elif question=="9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":                                             
    query_9='''select channel_name AS channelname, SEC_TO_TIME(AVG(duration)) AS averageduration from videosi group by channel_name'''   
    mycursor.execute(query_9)
    t9=mycursor.fetchall()
    df_9=pd.DataFrame(t9,columns=['Channel Name','Average Duration'])
    T9=[]
    for index,row in df_9.iterrows():
        channel_title=row['Channel Name'] 
        avg_duration=row['Average Duration']
        avg_str=str(avg_duration)
        T9.append(dict(channeltitle=channel_title,avg=avg_str))
    df_99=pd.DataFrame(T9)
    st.write(df_99)

elif question=="10.Which videos have the highest number of comments, and what are their corresponding channel names?":                                             
    query_10='''select title as videotitle, channel_name as channelname, comments as comments from videosi where comments
                is not null order by comments desc '''   
    mycursor.execute(query_10)
    t10=mycursor.fetchall()
    df_10=pd.DataFrame(t10,columns=['Video Title','Channel Name','Comments'])
    st.write(df_10)
