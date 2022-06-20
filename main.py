import pandas as pd
import numpy as np
import os
import sys
from dotenv import load_dotenv
import argparse
from lib.crawler.crawler import crawl_eksi
from lib.db.connections import PGSQLConnection
import datetime



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from eksisozluk.com')
    parser.add_argument('--local', action='store_true', help='Local option for paths and driver.')
    args = parser.parse_args()

    load_dotenv()

    entries = crawl_eksi(args)

    # Pre-process entries:
    # entries['created_on'] = pd.to_datetime('now', utc=True)
    # entries['created_on'] = entries['created_on'].astype(str)
    # entries['created_on'] = entries['created_on'].apply(lambda x: x.split(' ', 2)[0])
    print(entries.head(5))
    print(entries.shape)

    entries.rename(columns={'title': 'entry_title', 'entries': 'entry_record'}, inplace=True)

    psql_conn = PGSQLConnection(conn_url=os.getenv('CONN_URI'))

    psql_conn.upload_table(entries, 'eksi_entries')

