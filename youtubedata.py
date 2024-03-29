# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
import plotly.graph_objects as go
import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
# Setting up page configuration
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Harivarshini M",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by Harivarshini M!"""})

st.sidebar.header(" 👋:violet[Hello! Welcome to the dashboard]")

mydb = sql.connect(host="localhost",
                   user="root",
                   password="12345",
                   database= "PhonePe"
                  )
mycursor = mydb.cursor(buffered=True)

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected=="Home":
    st.image("C:/Users/hariv/OneDrive/Desktop/Data Science/Python/Phone_Pe/images/phonepe-logo-icon.webp", width=100)
    st.title("PhonePe - Data Visualization and Exploration ")
    st.markdown("### :chart_with_upwards_trend: :violet[Data Visualization and Exploration using Streamlit and Plotly]")
    col1,col2 = st.columns([4,2],gap="medium")
    with col1:
        
        st.markdown("####  :In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
        st.markdown("### :violet[Technologies used :]") 

        st.markdown("#### :Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, Plotly")

        
    with col2:
        st.image(r"C:\\Users\\hariv\\OneDrive\\Desktop\\Data Science\\Python\\Phone_Pe\\images\\data analaysis.gif")
    

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        st.image(r'C:\\Users\\hariv\\OneDrive\\Desktop\\Data Science\\Python\\Phone_Pe\\images\\topcharts.gif')

    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    Year = st.selectbox("Year",list(range(2018,2023)))
    Quarter = st.selectbox("Quarter", list(range(1,5)))
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        def create_donut_chart(df, title):
            fig = go.Figure(data=[go.Pie(labels=df['Label'], values=df['Total_Amount'], hole=0.4)])
            fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=px.colors.sequential.Agsunset))
            fig.update_layout(title=title)
            return fig
                    
# Query and create donut charts
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT state, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total DESC LIMIT 10")
            df_state = pd.DataFrame(mycursor.fetchall(), columns=['Label', 'Transactions_Count', 'Total_Amount'])
            fig_state = create_donut_chart(df_state, 'Top 10 States by Total Amount')
            st.plotly_chart(fig_state, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(Count) AS Total_Count, SUM(Amount) AS Total FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total DESC LIMIT 10")
            df_district = pd.DataFrame(mycursor.fetchall(), columns=['Label', 'Transactions_Count', 'Total_Amount'])
            fig_district = create_donut_chart(df_district, 'Top 10 Districts by Total Amount ')
            st.plotly_chart(fig_district, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT pincode, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM top_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY pincode ORDER BY Total DESC LIMIT 10")
            df_pincode = pd.DataFrame(mycursor.fetchall(), columns=['Label', 'Transactions_Count', 'Total_Amount'])
            fig_pincode = create_donut_chart(df_pincode, 'Top 10 Pincodes by Total Amount')
            st.plotly_chart(fig_pincode, use_container_width=True)

        #vertical chart
        df_combined = pd.concat([df_state, df_district, df_pincode], keys=['State', 'District', 'Pincode'])
        fig = px.bar(df_combined, x=df_combined.index.get_level_values(1), y='Total_Amount', color=df_combined.index.get_level_values(0),
                    barmode='group', orientation='v', labels={'Total_Amount': 'Total Amount'},
                    title='Top 10 States, Districts, and Pincodes by Total Amount')
        st.plotly_chart(fig, use_container_width=True)

                    
# Top Charts - USERS          
    if Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")       

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brand_name, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brand_name order by Total_Count desc limit 10")
                df_brand = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig_brand = px.bar(df_brand,
                                x='Brand',
                                y="Total_Users",
                                title='Top 10 Brands',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig_brand, use_container_width=True)   
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(Registerd_User) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df_district = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df_district['Total_Users'] = df_district['Total_Users'].astype(float)
            fig_district = px.bar(df_district,
                                x='District',
                                y='Total_Users',
                                title='Top 10 Districts',
                                color='Total_Users',
                                color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig_district, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df_pincode = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig_pincode = px.bar(df_pincode,
                                x='Pincode',
                                y='Total_Users',
                                title='Top 10 Pincodes',
                                color='Total_Users',
                                color_discrete_sequence=px.colors.sequential.Agsunset)
            st.plotly_chart(fig_pincode, use_container_width=True)

        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select State, sum(Registerd_user) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by State order by Total_Users desc limit 10")
            df_state = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig_state = px.bar(df_state,
                            x='State',
                            y='Total_Users',
                            title='Top 10 States',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig_state, use_container_width=True)

 # MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    st.header("Phone Pe - EXPLORING DATA 🔎")
    col1, col2 = st.columns(2)
    with col1:
        Year = st.slider("Year", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with col2:  
        Type = st.selectbox("Type", ("Transactions", "Users"))
    colu1, colu2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions": 
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with colu1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with colu2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
                    
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        # Pie Chart
        fig = px.pie(df,
              title='Transaction Types vs Total Transactions',
              names="Transaction_type",
              values="Total_Transactions",
              color_discrete_sequence=px.colors.sequential.Agsunset,
              hole=0.3)

        chart = st.plotly_chart(fig, use_container_width=False)
        click = st.button("Click to explode")
        col1, col2 = st.columns(2)
        if click:
            fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                            marker=dict(colors=px.colors.sequential.Agsunset, line=dict(color='#000000', width=2)))
            chart.plotly_chart(fig)
            with col1:
                return_click = st.button("Return to normal")
                if return_click:
                    fig.update_traces(hole=0.3)
                    chart.plotly_chart(fig)
  
        # Function to plot a bar chart
        def plot_bar_chart(df, x_column, y_column, title):
            fig, ax = plt.subplots(figsize=(18, 8))
            sns.barplot(x=x_column, y=y_column, data=df, ax=ax,palette='husl')
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(title)
            ax.tick_params(axis='x', rotation=45)  
            st.pyplot(fig)

        # Function to plot a line chart
        def plot_line_chart(df, x_column, y_column, title):
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=x_column, y=y_column, data=df, ax=ax )
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(title)
            ax.tick_params(axis='x', rotation=45)  # Removed ha='right'
            plt.tight_layout()
            st.pyplot(fig)

        # Ques1: Top Mobile Brands of Transaction Count (Bar Chart)
        def ques1():
            sql_query = """
                SELECT Brand_name, SUM(Count) AS Total_Count
                FROM agg_user
                GROUP BY Brand_name
                ORDER BY Total_Count DESC;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand_name', 'Total_Count'])
            plot_bar_chart(df, 'Brand_name', 'Total_Count', 'Top Mobile Brands of Transaction Count')

        # Ques2: States With Lowest Transaction Amount (Bar Chart)
        def ques2():
            sql_query = """
                SELECT State, SUM(Transaction_amount) AS Total_Amount
                FROM agg_trans
                GROUP BY State
                ORDER BY Total_Amount ASC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Amount'])
            plot_bar_chart(df, 'State', 'Total_Amount', 'States With Lowest Transaction Amount')

        # Ques3: Districts With Highest Transaction Amount (Line Chart)
        def ques3():
            sql_query = """
                SELECT District, SUM(Amount) AS Total_Amount
                FROM map_trans
                GROUP BY District
                ORDER BY Total_Amount DESC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Amount'])
            plot_line_chart(df, 'District', 'Total_Amount', 'Districts With Highest Transaction Amount')

        # Ques4: Top 10 Districts With Lowest Transaction Amount (Bar Chart)
        def ques4():
            sql_query = """
                SELECT District, SUM(Amount) AS Total_Amount
                FROM map_trans
                GROUP BY District
                ORDER BY Total_Amount ASC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Amount'])
            plot_bar_chart(df, 'District', 'Total_Amount', 'Top 10 Districts With Lowest Transaction Amount')

        # Ques5: Top 10 States With App Opens (Line Chart)
        def ques5():
            sql_query = """
                SELECT State, SUM(Appopens) AS Total_Appopens
                FROM map_user
                GROUP BY State
                ORDER BY Total_Appopens DESC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Appopens'])
            plot_line_chart(df, 'State', 'Total_Appopens', 'Top 10 States With App Opens')

        # Ques6: Least 10 States With App Opens (Line Chart)
        def ques6():
            sql_query = """
                SELECT State, SUM(AppOpens) AS Total_AppOpens
                FROM map_user
                GROUP BY State
                ORDER BY Total_AppOpens ASC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_AppOpens'])
            plot_line_chart(df, 'State', 'Total_AppOpens', 'Least 10 States With App Opens')

        # Ques7: States With Lowest Transaction Count (Bar Chart)
        def ques7():
            sql_query = """
                SELECT State, SUM(Transaction_count) AS Total_Transaction_count
                FROM agg_trans
                GROUP BY State
                ORDER BY Total_Transaction_count ASC;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transaction_count'])
            plot_bar_chart(df, 'State', 'Total_Transaction_count', 'States With Lowest Transaction Count')

        # Ques8: States With Highest Transaction Count (Bar Chart)
        def ques8():
            sql_query = """
                SELECT State, SUM(Transaction_count) AS Total_Transaction_count
                FROM agg_trans
                GROUP BY State
                ORDER BY Total_Transaction_count DESC;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transaction_count'])
            plot_bar_chart(df, 'State', 'Total_Transaction_count', 'States With Highest Transaction Count')

        # Ques9: States With Highest Transaction Amount (Line Chart)
        def ques9():
            sql_query = """
                SELECT State, SUM(Transaction_amount) AS Total_Amount
                FROM agg_trans
                GROUP BY State
                ORDER BY Total_Amount DESC
                LIMIT 10;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Amount'])
            plot_line_chart(df, 'State', 'Total_Amount', 'States With Highest Transaction Amount')

        # Ques10: Top 50 Districts With Lowest Transaction Amount (Pie Chart)
        def ques10():
            sql_query = """
                SELECT District, SUM(Amount) AS Total_Amount
                FROM map_trans
                GROUP BY District
                ORDER BY Total_Amount ASC
                LIMIT 50;
                """
            mycursor.execute(sql_query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Amount'])
            plot_bar_chart(df, 'District','Total_Amount', 'Top 50 Districts With Lowest Transaction Amount')

        # Streamlit UI
        st.set_option('deprecation.showPyplotGlobalUse', False)

        ques= st.selectbox("Select the question",('Top Brands Of Mobiles Used','States With Lowest Transaction Amount',
                                        'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                        'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Transaction Count',
                                        'States With Highest Transaction Count','States With Highest Transaction Amount',
                                        'Top 50 Districts With Lowest Transaction Amount'))

        # Call the respective function based on the selected question
        if ques == 'Top Brands Of Mobiles Used':
            ques1()
        elif ques == 'States With Lowest Transaction Amount':
            ques2()
        elif ques == 'Districts With Highest Transaction Amount':
            ques3()
        elif ques == 'Top 10 Districts With Lowest Transaction Amount':
            ques4()
        elif ques == 'Top 10 States With AppOpens':
            ques5()
        elif ques == 'Least 10 States With AppOpens':
            ques6()
        elif ques == 'States With Lowest Transaction Count':
            ques7()
        elif ques == 'States With Highest Transaction Count':
            ques8()
        elif ques == 'States With Highest Transaction Amount':
            ques9()
        elif ques == 'Top 50 Districts With Lowest Transaction Amount':
            ques10()


        

# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="Total_Transactions",
                     y="District",
                     orientation='h',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registerd_user) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registerd_user) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="Total_Users",
                     y="District",
                     orientation='h',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    
# MENU 4 - ABOUT
if selected == "About":
    st.markdown("## :violet[Phone Pe - ABOUT]")
    col1,col2=st.columns(2)
    with col1:
        st.caption('PhonePe is a mobile payment platform using which you can transfer money using UPI, recharge phone numbers, pay utility bills, etc. PhonePe works on the Unified Payment Interface (UPI) system and all you need is to feed in your bank account details and create a UPI ID. There is no need to recharge the wallet, because the money will be directly debited from your bank account at the click of a button in a safe and secure manner')
    
    with col2:
        st.video(r"C:\\Users\\hariv\\OneDrive\\Desktop\\Data Science\\Python\\Phone_Pe\\images\\about.mp4")
    
    st.subheader('Click the button to Download Phone Pe')

    url = "https://play.google.com/store/apps/details?id=com.phonepe.app&hl=en_IN&shortlink=2kk1w03o&c=consumer_app_icon&pid=PPWeb_app_download_page&af_xp=custom&source_caller=ui"
    if st.button("➡️Go to URL"):
          
        webbrowser.open_new_tab(url)
