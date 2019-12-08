import psycopg2
import pandas as pd
import numpy as np
import os
import lxml
import plotly.express as px
import plotly.graph_objects as go

print('testtesttest')

def crime_query(conn):
    df = pd.read_sql_query("select * from airquality_indicator;", conn, index_col='indicator_id')

    while True:
        print('1. Crime statics by years.\n'
              '2. Crime statics by months.\n'
              '3. Crime Statics by hours.\n'
              '4. Crime statics by map.\n'
              '5. quit')
        choise = input('Input Here:')
        if choise == '1':
            date_method = 'year'
            query = "select date_trunc(%(d_method)s,  cmplnt_fr_dt) as cmplnt_year, count(cmplnt_num) " \
                    "from crime group by cmplnt_year;"
            df = pd.read_sql_query(query,
                                   conn,
                                   params={'d_method': date_method})
            print(df)
            fig = px.bar(df, x='cmplnt_year', y='count',
                            color='cmplnt_year', barmode='relative',
                         labels={'pop':'New York City Crime Data'})

            fig.show()
        elif choise == '2':
            year_num = int(input('Input the specific year'))
            date_method = 'month'
            query = "select date_trunc(%(d_method)s,  cmplnt_fr_dt) as cmplnt_year, count(cmplnt_num) " \
                    "from  (select * from crime where date_part('year', cmplnt_fr_dt)=%(year)s) c " \
                    "group by cmplnt_year;"
            df = pd.read_sql_query(query,
                                   conn,
                                   params={'d_method': date_method, 'year':year_num})
            print(df)
            fig = px.line(df, x='cmplnt_year', y='count')

            fig.show()
        elif choise == '3':
            date_method = 'hour'
            query = "select date_trunc(%(d_method)s,  cmplnt_fr_tm) as cmplnt_hour, count(cmplnt_num) " \
                    "from  crime  " \
                    "group by cmplnt_hour;"
            df = pd.read_sql_query(query,
                                   conn,
                                   params={'d_method': date_method})
            df['cmplnt_hour'] = df['cmplnt_hour'].astype(str).str[-18:-10]
            df['cmplnt_hour'] = pd.to_datetime(df['cmplnt_hour'], format='%H:%M:%S').dt.time
            print(df)
            fig = px.line(df, x='cmplnt_hour', y='count')

            fig.show()
        elif choise == '4':
            year_num = int(input('Input the specific year:'))
            data_per = float(input('Input the percent of data:'))
            mapbox_public_token = 'pk.eyJ1IjoiZ3Vvb29vb2ppbmciLCJhIjoiY2szeGF6M3dmMDA1YzNtbGkzdm5rcGpqZSJ9.i6dEynHbMFZkg9kjVzp9Vg'
            px.set_mapbox_access_token(mapbox_public_token)
            query = "select geo.cmplnt_num, geo.boro_nm, geo.latitude, geo.longtitude " \
                    "from  crime_geo geo " \
                    "JOIN crime c " \
                    "ON (geo.cmplnt_num=c.cmplnt_num) " \
                    "where date_part('year', cmplnt_fr_dt)=%(year)s; "
            df = pd.read_sql_query(query, conn, params={'year':year_num})
            df = df.sample(frac=data_per)

            fig = px.scatter_mapbox(df, lat='latitude', lon='longtitude',
                                    color='boro_nm',
                                    opacity=0.8,
                                    color_continuous_scale=px.colors.cyclical.IceFire,
                                    zoom=10)
            fig.update_layout(
                mapbox_style="dark",
                showlegend=False,
                mapbox_layers=[
                    {
                        "below": 'traces',
                        "sourcetype": "raster",

                    },
                ]
            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 4})
            fig.show()
        else:
            break

def airquality_query(conn):
    df = pd.read_sql_query("select * from airquality_indicator;", conn, index_col='indicator_id')

    # print("1: UHF42")
    # print("2: Borough")
    # area = input('Which of the area you want to check?\nEnter here:')
    # acode = ''
    # if area == '1': acode = 'UHF42'
    # elif area == '2': acode = 'Borough'
    # else:
    #     print('Wrong input')
    #     return
    # print(df)
    # indicatorID = int(input('Which one of the indicator statics you want to check? \nEnter here:'))
    indicatorID = 639
    acode = 'UHF42'
    query = "SELECT aq.indicator_data_id as id, geo.geo_entity_name  FROM " \
            "airquality aq JOIN airquality_geo geo ON (aq.indicator_data_id=geo.indicator_data_id) " \
            "WHERE aq.indicator_id=%(id)s AND geo.geo_type_name=%(code)s AND aq.data_valuemessage>50.0;"
    df = pd.read_sql_query(query,
                           conn,
                           params={'id': indicatorID, 'code': acode})
    print(df)
    fig = px.histogram(df, x='geo_entity_name', y='id',
                       histfunc='count', color='geo_entity_name')
    fig.update_layout(showlegend=True)
    fig.show()


if __name__ == '__main__':
    conn_string = "host='localhost' dbname='project' user='postgres' password='j'"
    conn = psycopg2.connect(conn_string)

    # airquality_query(conn)
    crime_query(conn)
    # DELETE FROM CRIME WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
    # DELETE FROM crime_geo WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
