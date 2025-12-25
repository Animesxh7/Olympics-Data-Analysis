import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,help
from help import medal_tally
import plotly
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.header('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)
df = df.loc[:, ~df.columns.duplicated()]

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = help.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)
    medal_tally  = help.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'All' and selected_country == 'All':
        st.title("Overall Tally")
    if selected_year != 'All' and selected_country == 'All':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'All' and selected_country != 'All':
        st.title(selected_country + " overall performance")
    if selected_year != 'All' and selected_country != 'All':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    st.sidebar.header('Overall Analysis')
    editions = df['Year'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    st.title("Top Stats")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Cities")
        st.title(cities)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Sports")
        st.title(sports)
    with col2:
        st.header("Events")
        st.title(events)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_every_year = help.data_every_year(df,'region')
    fig = px.line(nations_every_year, x='Year', y='region')
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)
    events_every_year = help.data_every_year(df, 'Event')
    fig = px.line(events_every_year, x='Year', y='Event')
    st.title('Events held Over the Years')
    st.plotly_chart(fig)
    athletes_every_year = help.data_every_year(df, 'Name')
    fig = px.line(athletes_every_year, x='Year', y='Name')
    st.title('Total Athletes Over the Years')
    st.plotly_chart(fig)
    st.title('No. of Events Over the Years(Every Sport)')
    fig , ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                cmap='cividis', annot=True, fmt='d')
    st.pyplot(fig)
    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'All')
    selected_sport = st.selectbox('Select Sport',sport_list)
    x = help.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country',country_list)
    country_df = help.year_wise_medal(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal Tally Over the Years')
    st.plotly_chart(fig)
    st.title(selected_country + ' excels in the following Sports')
    pt = help.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)
    st.title("Top 10 Athletes of the " + selected_country)
    top10_df = help.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna().astype(float).tolist()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().astype(float).tolist()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().astype(float).tolist()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().astype(float).tolist()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'All')
    selected_sport = st.sidebar.selectbox('Select Sport', sport_list)
    temp_df = help.weight_v_height(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],hue = temp_df['Medal'],style = temp_df['Sex'],s = 60)
    st.title('Height vs Weight of Athletes')
    st.pyplot(fig)
    st.title("Men Vs Women Participation Over the Years")
    final_df = help.men_vs_women(df)
    fig = px.line(final_df, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



