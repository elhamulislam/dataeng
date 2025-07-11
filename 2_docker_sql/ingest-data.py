#!/usr/bin/env python
# coding: utf-8

from time import time

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    filename = "output.csv" if url.endswith(".csv") else "output.parquet"
    os.system(f"wget {url} -O {filename}")

    if filename.endswith(".parquet"):
        df = pd.read_parquet(filename)
        df.to_csv("output.csv", index=False)
        filename = "output.csv"


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(filename, iterator=True, chunksize=100000)


    df = next(df_iter)

    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        t_start = time()
        df = next(df_iter)
        if 'tpep_pickup_datetime' in df.columns:
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        if 'tpep_dropoff_datetime' in df.columns:
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk..., took %.3f second' % (t_end - t_start))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')

    parser.add_argument ('--user', help='user name for postgres')
    parser.add_argument ('--password', help='password for postgres')
    parser.add_argument ('--host', help='host for postgres')
    parser.add_argument( '--port', help= 'port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument ('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)