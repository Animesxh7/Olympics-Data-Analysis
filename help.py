from os import rename
import numpy as np
from analysis import athlete_df
def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'All' and country == 'All':
        temp_df = medal_df
    elif year == 'All' and country != 'All':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'All' and country == 'All':
        temp_df = medal_df[medal_df['Year'] == year]
    else :
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x
def medal_tally(df):
    Medal_Tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    Medal_Tally = Medal_Tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    Medal_Tally['total'] = Medal_Tally['Gold'] + Medal_Tally['Silver'] + Medal_Tally['Bronze']
    return Medal_Tally
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'All')
    country = np.unique(df['region'].dropna().tolist())
    country = country.tolist()
    country.insert(0, 'All')
    return years,country
def data_every_year(df,col):
    nations_every_year = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_every_year.rename(columns={'count': col}, inplace=True)
    return nations_every_year
def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'All':
        temp_df = temp_df[temp_df['Sport'] == sport]
    vc = temp_df['Name'].value_counts().reset_index()
    vc.columns = ['Name', 'Medals']
    top_players = (vc.head(15).merge(df,on='Name',how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name'))
    return top_players
def year_wise_medal(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pt
def most_successful_countrywise(df,selected_country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == selected_country]
    vc = temp_df['Name'].value_counts().reset_index()
    vc.columns = ['Name', 'Medals']
    top_players = (vc.head(10).merge(df,on='Name',how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name'))
    return top_players
def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = men.merge(women, on='Year', how='left')
    final_df.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final_df