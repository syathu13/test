import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar  ,Calendar,Tab
import streamlit.components.v1 as components
from pathlib import Path
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------------------------



st.header("Outboud Dashboard")
df=pd.read_excel(
        io="MHE Production.xlsx",
        engine="openpyxl",
        sheet_name="Active pics",
        skiprows=0,
        usecols="A:G",
        nrows=190000
)
df.info()



#----------------calender heatmap---------------------------------
pick_by_day=df.groupby(by='Date').sum()[['PICKS']].round(0)
pick_by_day=pick_by_day.reset_index()


data=pick_by_day [['Date','PICKS']].values.tolist()

maxpick=df['PICKS'].max()
minpick=20000



total_pickby_day=(
   Calendar()
    .add('', data, calendar_opts=opts.CalendarOpts(range_=['2023']))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='Total Picked Line Day By Day   AA    ,A1  ,B3  &   G1', subtitle='Year View'),
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
#---------------Save report HTML ------------
tab=Tab(page_title='heat map calender ')
tab.add(total_pickby_day," ")
tab.render(Path.cwd() / 'heatmapcalnder.html')

#--------------load HTML data into App------
with st.expander('Day By Day Total Pick Lines'):
    HtmlFile = open("heatmapcalnder.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    print(source_code)
    components.html(source_code,height = 320)

#--------------Side bar datas Date picker------------------



st.sidebar.header("Filters here ")

date1 = st.sidebar.date_input(
    "Select Data",
    )
zone=st.sidebar.multiselect(
"select zone :",
options=df["AREA"].unique(),
default=df["AREA"].unique()
)


#------------------Filer data frame------------------
df_selection_sidebar=df.query(
                        "AREA == @zone & Date == @date1"
)
#--------CSS-----------------------------------------



st.markdown("""
<style>
.minhed {
    font-size:16px !important;
    color:red;
    font-weight: bold;
    font-size: 30px;

}
table{
            background-color: orange;
        }
</style>
""", unsafe_allow_html=True)



#-------------header layout-----------

col1,col2,col3,col4=st.columns(4)
# top Pickers each Area
cola, colb, colc = st.columns(3)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




#--------------------B3---------------------------
b_3_top=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='B3') ].nlargest(3, 'PICKS')
b_3_top=b_3_top[['USER','PICKS']]
b_3_top.reset_index (drop=True, inplace=True)
b3pickers=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='B3') ]
with col1:
    b3pickers=b3pickers[['USER','PICKS']]
    st.dataframe(b3pickers,200,200)


#--------------------AA---------------------------
aa_top=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='AA') ].nlargest(3, 'PICKS')
aa_top=aa_top[['USER','PICKS']]
aa_top.reset_index (drop=True, inplace=True)
aapickers=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='AA') ]

with col2:
    aapickers=aapickers[['USER','PICKS']]
    st.dataframe(aapickers,200,200)
#--------------------A1---------------------------

a1_top=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='A1') ].nlargest(1, 'PICKS')
a1_top=a1_top[['USER','PICKS']]
a1_top.reset_index (drop=True, inplace=True)
a1pickers=df_selection_sidebar.loc[(df_selection_sidebar['AREA']=='A1') ]
with col3:
    a1pickers=a1pickers[['USER','PICKS']]
    st.dataframe(a1pickers,200,200)
#--------------------G1---------------------------

#g1_top=g1_top[['USER','PICKS']]
#g1_top.reset_index (drop=True, inplace=True)
#with col4:
#st.markdown('<p class="subheader">Top G1 Picker </p>', unsafe_allow_html=True)
#st.write(g1_top.iloc[0].to_string(index=False))
total_line=df_selection_sidebar['PICKS'].sum()

pivoted = df_selection_sidebar.pivot_table(index="USER", columns="AREA", values="PICKS",aggfunc= 'sum',margins = True, margins_name='Total')
df1=pivoted.fillna('0').astype(int)
    #st.dataframe(df1,200,200)





#----------------------Pivot with conditions

df_styled=df1.style.apply(lambda x: ["background: white"
                                    if (colname=='B3' and value==0 )
                                    else"background: red"
                                    if (colname=='B3' and value<720 )
                                    else  "background: yellow"
                                    if (colname=='B3' and value<920)
                                    else "background: green"
                                    if (colname=='B3' and value>920)
                                    else "background: white"
                                    if (colname=='AA' and value==0 )
                                    else "background: red"
                                    if (colname=='AA' and value<350)
                                    else "background: yellow"
                                    if (colname=='AA' and value<450)
                                    else "background: green"
                                    if (colname=='AA' and value>450)
                                    else "background: white"
                                    if (colname=='A1' and value==0 )
                                    else "background: red"
                                    if (colname=='A1' and value<350)
                                    else "background: yellow"
                                    if (colname=='A1' and value<450)
                                    else "background: green"
                                    if (colname=='A1' and value>450)
                                    else "background: green"
                                    if (colname=='G1' and value>350)


                                    else "background: white"
                                    for colname,value in x.iteritems()], axis = 1)\
                                    .set_properties(**{
                                    'border-color': 'blue',
                                    "border": "2px double gray",
                                    "color": "black",
                                    "font-size": "11px"               })


colaaa, colbbb= st.columns(2)







with cola:
        st.markdown('<p class="minhed">Top B3 Picker </p>', unsafe_allow_html=True)
        st.write(b_3_top.iloc[0].to_string(index=False))
with colb:
        st.markdown('<p class="minhed">Top AA Picker </p>', unsafe_allow_html=True)
        st.write(aa_top.iloc[0].to_string(index=False))
with colc:
        st.markdown('<p class="minhed">Top A1 Picker </p>', unsafe_allow_html=True)
        st.write(a1_top.iloc[0].to_string(index=False))
#--------secound set metric-------------
col1, col2, col3 = st.columns(3)

picks=df_selection_sidebar['PICKS'].sum()

total_picker=df_selection_sidebar['USER'].nunique()
target=picks-14000;
target_pickers=total_picker-32
col1.metric("Target 14K lines/shift",int(picks),int(target) )
col2.metric("Total acive pickers",total_picker , target_pickers)
#col3.metric("Total Units", "86%", "4%")
#---------------------
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            background-color:red
            </style>
            """

#---------------------


with col3:
    over_view=df_selection_sidebar.groupby(by='AREA',as_index=False).sum().sort_values(by=['PICKS'])
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(over_view)

#-------------------------------------------
col_left_ga, col_right_ga = st.columns(2)


fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = df_selection_sidebar['PICKS'].sum(),
        mode = "gauge+number+delta",
        title = {'text': "Total Lines Picked By day"},
        delta = {'reference': 13000},
        gauge = {'axis': {'range': [None, 22000]},
                'steps' : [
                    {'range': [0, 15000], 'color': "lightgray"},
                    {'range': [15000, 22000], 'color': "gray"}],
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 1, 'value': 14000}}))
with col_left_ga:
    with st.expander('gague'):
        st.plotly_chart(fig, use_container_width=True)
with col_right_ga:
    df_styled.to_html(r'pick_line_table.html')
    with st.expander('Picks By User '):
        HtmlFile = open("pick_line_table.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 320,scrolling=True)




with st.expander('Chart '):
    long_df = df
    fig1 = px.bar(df_selection_sidebar, x="USER", y="PICKS", color="AREA", title="Long-Form Input")
    st.plotly_chart(fig1, use_container_width=True)
