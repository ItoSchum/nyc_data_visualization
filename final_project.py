import psycopg2
import pandas as pd
import numpy as np
import os
import lxml
import plotly.express as px
import plotly.graph_objects as go


def crime_query(conn):
    df = pd.read_sql_query("select * from airquality_indicator;", conn, index_col='indicator_id')

    while True:
        print('1. Crime statics by crime.\n'
              '2. Crime statics by months.\n'
              '3. Crime Statics by hours.\n'
              '4. Crime statics by map.\n'
              'q. quit')
        choise = input('Input Here:')
        if choise == '1':
            query = "SELECT cd.ky_cd, ofns_desc, law_cat_cd, count(cmplnt_num) " \
                    "FROM crime c " \
                    "JOIN crime_desc cd " \
                    "ON (c.ky_cd=cd.ky_cd) " \
                    "GROUP BY cd.ky_cd, ofns_desc, law_cat_cd " \
                    "ORDER BY count desc;"
            df = pd.read_sql_query(query,
                                   conn)
            print(df)
            fig = px.bar(df, x='ofns_desc', y='count',
                         color='ofns_desc', barmode='relative',
                         hover_data=['law_cat_cd'],
                         labels={'pop': 'New York City Crime Data'})

            fig.show()
        elif choise == '2':
            query = "select TO_CHAR(cmplnt_fr_dt, 'Month') as cmplnt_year, count(*) from crime group by cmplnt_year;"
            df = pd.read_sql_query(query,
                                   conn)
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
            law = ['MISDEMEANOR', 'VIOLATION', 'FELONY']
            law_num = int(
                input('Which of the crime type you want to see?\n1.Misdemeanor\n2.Violation\n3.Felony\nEnter here:'))
            data_per = int(input('How many data you want to see?(Enter a integer less than 100000)\n Enter here:'))
            mapbox_public_token = 'pk.eyJ1IjoiZ3Vvb29vb2ppbmciLCJhIjoiY2szeGF6M3dmMDA1YzNtbGkzdm5rcGpqZSJ9.i6dEynHbMFZkg9kjVzp9Vg'
            px.set_mapbox_access_token(mapbox_public_token)
            query = "select geo.cmplnt_num, geo.boro_nm, geo.latitude, geo.longtitude, cd.law_cat_cd " \
                    "FROM( select geo.cmplnt_num, c.ky_cd, geo.boro_nm, geo.latitude, geo.longtitude " \
                    "from  crime_geo geo " \
                    "JOIN crime c " \
                    "ON (geo.cmplnt_num=c.cmplnt_num)) geo " \
                    "JOIN (select * from crime_desc " \
                    "where law_cat_cd=%(type)s) cd " \
                    "ON (geo.ky_cd=cd.ky_cd);"
            df = pd.read_sql_query(query, conn, params={'type': law[law_num - 1]})
            df = df.sample(data_per)

            fig = px.scatter_mapbox(df, lat='latitude', lon='longtitude',
                                    color='boro_nm',
                                    opacity=0.8,
                                    hover_data=['law_cat_cd'],
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
    acode = ['UHF42', 'Rorough']
    while True:
        print("Which of the area code you want to see?\n1. UHF42\n2. Borough\nq. Quit")
        area = int(input('Enter here:'))
        if area != 1 and area != 2:
            break
        query = "SELECT geo_entity_name, sum(data_valuemessage) FROM " \
                "airquality aq JOIN airquality_geo geo " \
                "ON (aq.indicator_data_id=geo.indicator_data_id) " \
                "WHERE geo_type_name=%(code)s " \
                "GROUP BY geo_entity_name " \
                "ORDER BY sum DESC;"
        df = pd.read_sql_query(query,
                               conn,
                               params={'code': acode[area - 1]})
        print(df)
        fig = px.bar(df, x='geo_entity_name', y='sum',
                     color='geo_entity_name',
                     barmode='relative',
                     labels={'pop': 'New York City Air Quality Data'})
        fig.show()


if __name__ == '__main__':
    conn_string = "host='localhost' dbname='project' user='postgres' password='j'"
    conn = psycopg2.connect(conn_string)

    airquality_query(conn)

    # crime_query(conn)
    # DELETE FROM CRIME WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
    # DELETE FROM crime_geo WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
