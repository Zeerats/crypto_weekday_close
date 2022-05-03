import pandas as pd
import plotly.graph_objects as go


csv_file = './datasets/coin_Bitcoin.csv'

df = pd.read_csv(csv_file)


df['Date'] = pd.to_datetime(df['Date'])
df['Weekday'] = df['Date'].dt.day_name()


df_list = list(df['Close'])
red_green = [0]

for i, x in enumerate(df_list):      
    if i == 0 or i == (len(df_list)): 
        pass
    else:
        pre = df_list[i-1]                    
        if pre > x:          
            red_green.append('red')
        else:
            red_green.append('green')

df['Color'] = red_green

weekdays_red = {
    'Monday':0,
    'Tuesday':0,
    'Wednesday':0,
    'Thursday':0,
    'Friday':0,
    'Saturday':0,
    'Sunday':0
}

weekdays_green = {
    'Monday':0,
    'Tuesday':0,
    'Wednesday':0,
    'Thursday':0,
    'Friday':0,
    'Saturday':0,
    'Sunday':0
}

for index, row in df.iterrows():
    if row['Color'] == 'red':
        weekdays_red[row['Weekday']] += 1
    else:
        weekdays_green[row['Weekday']] += 1

df2 = pd.DataFrame()
df2['Weekday'] = weekdays_green
df2.index = [x for x in range(1, len(df2.values)+1)]

for index, key in enumerate(weekdays_red):
    df2.at[index+1, 'red'] = weekdays_red[key]
    
for index, key in enumerate(weekdays_green):
    df2.at[index+1, 'green'] = weekdays_green[key]


fig = go.Figure(data=[
      go.Bar(name='Positive', x=df2['Weekday'], y=df2['green'], marker=dict(color='#31DA6E')),
      go.Bar(name='Negative', x=df2['Weekday'], y=df2['red'], marker=dict(color='#E8205A'))
      ])

fig.update_yaxes(type="log")
fig.update_layout(barmode='group', title='ETH - POSITIVE VS. NEGATIVE CLOSE | AGAINST PREVIOUS DAY CLOSE (2013-2021) | LOGARITHMIC SCALE', template='plotly_dark')
fig.write_html('plot.html', auto_open=True)