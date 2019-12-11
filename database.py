#!/usr/local/var/pyenv/shims/python3
#!python3
import psycopg2
import pandas as pd
import numpy as np
import os
import lxml
import plotly.express as px
import plotly.graph_objects as go
import calendar
import pymongo

mapbox_public_token = 'pk.eyJ1IjoiZ3Vvb29vb2ppbmciLCJhIjoiY2szeGF6M3dmMDA1YzNtbGkzdm5rcGpqZSJ9.i6dEynHbMFZkg9kjVzp9Vg'
px.set_mapbox_access_token(mapbox_public_token)

def abnyc_query(conn):
    df = pd.read_sql_query("select * from abnyc;", conn, index_col='id')

    while True:
        print('1. NYC Airbnb statics by minimum nights on map.\n'
              '2. NYC Airbnb statics by availability on map.\n'
              '3. NYC Airbnb statics by reviews on map.\n'
              'q. Quit')
        choice = input('Input Here: ')
        
        size_indicator = ""

        if choice == '1':
            query = "SELECT compound.id, compound.latitude, compound.longitude, nbhd.neighbourhood_group, compound.minimum_nights " \
                    "FROM (" \
                        "SELECT geo.id, geo.latitude, geo.longitude, main.neighbourhood, main.minimum_nights " \
                        "FROM  abnyc_geo AS geo " \
                        "INNER JOIN abnyc AS main " \
                        "ON geo.id = main.id) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM abnyc_nbhd) AS nbhd " \
                        "ON nbhd.neighbourhood = compound.neighbourhood;"

            size_indicator = "minimum_nights"

        elif choice == '2':
            query = "SELECT compound.id, compound.latitude, compound.longitude, nbhd.neighbourhood_group, compound.availability_365 " \
                    "FROM (" \
                        "SELECT geo.id, geo.latitude, geo.longitude, main.neighbourhood, main.availability_365 " \
                        "FROM  abnyc_geo AS geo " \
                        "INNER JOIN abnyc AS main " \
                        "ON geo.id = main.id) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM abnyc_nbhd) AS nbhd " \
                        "ON nbhd.neighbourhood = compound.neighbourhood;"
            
            size_indicator = "availability_365"

        elif choice == '3':
            query = "SELECT compound.id, compound.latitude, compound.longitude, nbhd.neighbourhood_group, compound.number_of_reviews " \
                    "FROM (" \
                        "SELECT geo.id, geo.latitude, geo.longitude, main.neighbourhood, main.number_of_reviews " \
                        "FROM  abnyc_geo AS geo " \
                        "INNER JOIN abnyc AS main " \
                        "ON geo.id = main.id) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM abnyc_nbhd) AS nbhd " \
                        "ON nbhd.neighbourhood = compound.neighbourhood;"

            size_indicator = "number_of_reviews"    

        else:
            break

        df = pd.read_sql_query(query, conn)

        fig = px.scatter_mapbox(df, lat='latitude', lon='longitude',
                                color='neighbourhood_group',
                                size=size_indicator,
                                opacity=0.8,
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

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

def liquor_query(conn):
    df = pd.read_sql_query("select * from abnyc;", conn, index_col='id')

    while True:
        print('1. NYC liquor statics by month on map.\n'
              '2. NYC liquor statics by year on map.\n'
              '3. NYC liquor statics overall on map.\n'
              'q. Quit')
        choice = input('Input Here: ')

        # data_per = int(input('How many data you want to see? (Enter a integer less than 100000)\n Enter here: ')

        if choice == '1':
            year_month = input('Which [YEAR-MONTH] would you like to check?\nEnter here: ')

            query = "SELECT compound.license_serial_number, compound.latitude, compound.longitude, compound.license_effective_date, type.license_type_name " \
                    "FROM (" \
                        "SELECT geo.license_serial_number, geo.latitude, geo.longitude, main.license_class_code, main.license_effective_date " \
                        "FROM  liquor_geo AS geo " \
                        "INNER JOIN ( " \
                            "SELECT * " \
                            "FROM liquor " \
                            "WHERE license_effective_date >= '%(year)s-%(month)s-01' AND license_effective_date < '%(year)s-%(month)s-%(end_day)s') AS main " \
                        "ON geo.license_serial_number = main.license_serial_number) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM liquor_type) AS type " \
                        "ON type.license_class_code = compound.license_class_code;"
            
            year = year_month.split("-")[0]
            month = year_month.split("-")[1]
            month_range = calendar.monthrange(int(year), int(month))
            end_day = month_range[1]

            df = pd.read_sql_query(query, conn, params={'year': int(year), 'month': int(month), 'end_day': end_day})

        elif choice == '2':
            year = int(input('Which [YEAR] would you like to check?\nEnter here: '))

            query = "SELECT compound.license_serial_number, compound.latitude, compound.longitude, compound.license_effective_date, type.license_type_name " \
                    "FROM (" \
                        "SELECT geo.license_serial_number, geo.latitude, geo.longitude, main.license_class_code, main.license_effective_date " \
                        "FROM  liquor_geo AS geo " \
                        "INNER JOIN ( " \
                            "SELECT * " \
                            "FROM liquor " \
                            "WHERE license_effective_date >= '%(year)s-01-01' AND license_effective_date <= '%(year)s-12-31') AS main " \
                        "ON geo.license_serial_number = main.license_serial_number) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM liquor_type) AS type " \
                        "ON type.license_class_code = compound.license_class_code;"

            df = pd.read_sql_query(query, conn, params={'year': year})

        elif choice == '3':
            query = "SELECT compound.license_serial_number, compound.latitude, compound.longitude, compound.license_effective_date, type.license_type_name " \
                    "FROM (" \
                        "SELECT geo.license_serial_number, geo.latitude, geo.longitude, main.license_class_code, main.license_effective_date " \
                        "FROM  liquor_geo AS geo " \
                        "INNER JOIN liquor AS main " \
                        "ON geo.license_serial_number = main.license_serial_number) AS compound " \
                    "INNER JOIN (" \
                        "SELECT * FROM liquor_type) AS type " \
                        "ON type.license_class_code = compound.license_class_code;"

            # size_indicator = "number_of_reviews"    
            df = pd.read_sql_query(query, conn)

        else:
            break

        # df = df.sample(data_per)

        fig = px.scatter_mapbox(df, lat='latitude', lon='longitude',
                                # color='license_effective_date',
                                # size=10,
                                opacity=0.8,
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

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


def crime_query(conn):
    df = pd.read_sql_query("select * from airquality_indicator;", conn, index_col='indicator_id')

    while True:
        print('1. Crime statics by crime.\n'
              '2. Crime statics by months.\n'
              '3. Crime statics by hours.\n'
              '4. Crime statics by map.\n'
              'q. Quit')
        choice = input('Input Here: ')
        
        if choice == '1':
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
        
        elif choice == '2':
            query = "select TO_CHAR(cmplnt_fr_dt, 'Month') as cmplnt_year, count(*) from crime group by cmplnt_year;"
            df = pd.read_sql_query(query,
                                   conn)
            print(df)
            fig = px.line(df, x='cmplnt_year', y='count')

            fig.show()
        
        elif choice == '3':
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
        
        elif choice == '4':
            law = ['MISDEMEANOR', 'VIOLATION', 'FELONY']
            law_num = int(
                input('Which of the crime type you want to see?\n1.Misdemeanor\n2.Violation\n3.Felony\nEnter here: '))
            data_per = int(input('How many data you want to see?(Enter a integer less than 100000)\n Enter here: '))
            
            query = "SELECT geo.cmplnt_num, region.boro_nm, geo.latitude, geo.longitude, cd.law_cat_cd " \
                    "FROM (SELECT geo.cmplnt_num, c.ky_cd, geo.latitude, geo.longitude " \
                        "FROM crime_geo AS geo " \
                        "JOIN crime AS c " \
                        "ON geo.cmplnt_num=c.cmplnt_num) AS geo " \
                    "JOIN (SELECT * " \
                        "FROM crime_desc " \
                        "WHERE law_cat_cd=%(type)s) AS cd " \
                    "ON geo.ky_cd=cd.ky_cd " \
                    "JOIN crime_region AS region " \
                    "ON geo.cmplnt_num=region.cmplnt_num;"

            df = pd.read_sql_query(query, conn, params={'type': law[law_num - 1]})

            df = df.sample(data_per)

            fig = px.scatter_mapbox(df, lat='latitude', lon='longitude',
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
    acode = ['UHF42', 'Borough']
    while True:
        print("Which of the area code you want to see?\n1. UHF42\n2. Borough\nq. Quit")
        area = input('Enter here: ')
        
        if area != '1' and area != '2':
            break
        area = int(area)
        query = "SELECT geo_entity_name, sum(data_valuemessage) FROM " \
                "airquality aq JOIN airquality_geo geo " \
                "ON (aq.indicator_data_id=geo.indicator_data_id) " \
                "WHERE geo_type_name=%(code)s " \
                "GROUP BY geo_entity_name " \
                "ORDER BY sum DESC;"
        df = pd.read_sql_query(query,
                               conn,
                               params={'code': acode[area - 1]})

        fig = px.bar(df, x='geo_entity_name', y='sum',
                     color='geo_entity_name',
                     barmode='relative',
                     labels={'pop': 'New York City Air Quality Data'})
        fig.show()


def crime_airbnb(conn, col, fav):

    while True:
        col.remove()
        crime_bo = [ 'QUEENS', 'MANHATTAN', 'BRONX', 'BROOKLYN', 'STATEN ISLAND']
        an_bo = ['Queens', 'Manhattan', 'Bronx', 'Brooklyn', 'Staten Island']
        print('Enter the number to see the crime and airbnb data on map.\n1.Queens\n'
            '2.Manhattan\n3.Bronx\n4.Brooklyn\n5.Staten Island')
        boro_n = int(input('Enter here: '))
        query1 = 'SELECT * FROM crime_geo g ' \
                'JOIN crime_region r ' \
                'ON (g.cmplnt_num=r.cmplnt_num) ' \
                'WHERE boro_nm = %(boro)s;'
        df1 = pd.read_sql_query(query1, conn, params={'boro':crime_bo[boro_n-1]})
        df1 = df1.sample(5000)
        df1['name'] = df1.shape[0] * ['crime'] 
        data1 = df1.to_dict(orient='records')
        col.insert_many(data1)

        query2 = 'SELECT a.id, g.latitude, g.longitude, n.neighbourhood_group ' \
                'FROM abnyc a, abnyc_geo g, abnyc_nbhd n ' \
                'WHERE a.id=g.id AND a.neighbourhood=n.neighbourhood ' \
                'AND neighbourhood_group = %(boro)s;'
        df2 = pd.read_sql_query(query2, conn, params={'boro':an_bo[boro_n-1]})
        df2['name'] = df2.shape[0] * ['airbnb'] 
        data2 = df2.to_dict(orient='records')
        col.insert_many(data2)

        df = pd.DataFrame(list(col.find()))
        print(df.shape[0])
        fig = px.scatter_mapbox(df, lat='latitude', lon='longitude',
                                color='name',
                                opacity=0.8,
                                hover_data=['id'],
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

        print('Do you have any preference Airbnb? \nEnter Airbnb ID with comma seperate.')
        pre = input('Enter here: ')
        lst = [int(i) for i in pre.split(',')]
        for i in lst:
            query = 'SELECT id, name, host_id, neighbourhood, room_type, price, minimum_nights, number_of_reviews, availability_365 from abnyc WHERE id=%(ids)s;'
            df = pd.read_sql_query(query, conn, params={'ids':i})
            data = df.to_dict(orient='records')
            fav.insert_many(data)
        df = pd.DataFrame(list(fav.find()))
        print(df)
        if input('Press q to quit: ') == 'q':
            break