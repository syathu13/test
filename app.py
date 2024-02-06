import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar  ,Calendar,Tab
import streamlit.components.v1 as components

from pathlib import Path



st.set_page_config(
                    layout="wide"
                    )

df=pd.read_excel(
        io="test.xlsx",
        engine="openpyxl",
        sheet_name="ap",
        skiprows=0,
        usecols="A:G",
        nrows=190000
)
df.info()



pick_by_day=df.groupby(by='Date').sum()[['PICKS']].round(0)
pick_by_day=pick_by_day.reset_index()
pick_by_day.head(5)

data=pick_by_day [['Date','PICKS']].values.tolist()
data
maxpick=df['PICKS'].max()
minpick=20000
maxpick


pick_cal=(
   Calendar()
    .add('', data, calendar_opts=opts.CalendarOpts(range_=['2023','2022']))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='PICK Calendar', subtitle='LINES'),
        legend_opts=opts.LegendOpts(is_show=False),
        visualmap_opts=opts.VisualMapOpts(
                max_=maxpick,
                min_=minpick,
                orient='horizontal',
                is_piecewise=False,
                pos_top='230px',
                pos_left='100px',
        )
    )

)
tab=Tab(page_title='test ')
tab.add(pick_cal,'pc')

tab.render(Path.cwd() / 'sa2.html')
#-------------------------------------------------------
stc=(


)


#----- side bar for page ---------
st.sidebar.header("Filters here ")

zone=st.sidebar.multiselect(
"select zone :",
options=df["AREA"].unique(),
default=df["AREA"].unique()
)


date1 = st.sidebar.date_input(
    "Select Data",
    )
#--------layout-----


HtmlFile = open("sa1.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
print(source_code)
components.html(source_code,height = 320)

col1,col2,col3=st.columns(3)
#--------------Queary

df_selection=df.query(
                        "AREA == @zone & Date == @date1"

)
#----data-frame








df_display=df_selection[["USER","AREA","PICKS"]]
topb3 =df.nlargest(1, ['PICKS'] )
with col1:

    st.write("TOP PICKER B3: ")


    st.dataframe(df_display,350,200)
    #table with and hight


pivoted = df_selection.pivot_table(index="USER", columns="AREA", values="PICKS",aggfunc= 'sum',margins = True, margins_name='Total')
pivoted
df1=pivoted.tail(10).fillna('0').astype(int)


with col3:
    st.write("TOP PICKER AA : ")
    st.dataframe(df1.fillna(''),400,200)






ch=df_selection[["USER","AREA","PICKS"]]
st.bar_chart(ch,x='USER',y='PICKS')



above_920= df_display[df_display["PICKS"] > 920 ]



with col2:
    st.write("TOP PICKER A1: ")
    st.dataframe(above_920,350,200)


    #-----------------




#st.title("Outbound KPI")  # add a title
#st.write(df)  #
#dest.bar_chart(data=df)
