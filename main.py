import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import argparse
from lib.crawler.crawler import crawl_eksi
from lib.crawler.crawler_updated import crawl_eksi_updated
from lib.db.connections import PGSQLConnection



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from eksisozluk.com')
    parser.add_argument('--local', action='store_true', help='Local option for paths and driver.')
    parser.add_argument('--custom_driver', type=str, help='Driver path.')
    args = parser.parse_args()

    load_dotenv()

    # Old crawl using Selenium is deprecated:
    # entries = crawl_eksi(args)

    # New crawler using requests which is faster and more stable:
    entries = crawl_eksi_updated()

    # Pre-process entries:
    entries['created_on'] = pd.to_datetime('now', utc=True)
    entries['created_on'] = entries['created_on'].astype(str)
    entries['created_on'] = entries['created_on'].apply(lambda x: x.split(' ', 2)[0])

    entries.rename(columns={'title': 'entry_title', 'entries': 'entry_record'}, inplace=True)

    psql_conn = PGSQLConnection(conn_url=os.getenv('CONN_URI'))

    psql_conn.upload_table(entries, 'eksi_daily', data_append=True)
    # psql_conn.insert_data(entries, 'eksi_daily')

