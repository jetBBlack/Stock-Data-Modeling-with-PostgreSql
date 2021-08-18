import pandas as pd
import psycopg2
import psycopg2.extras
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from sql_queries import *

def extract_load_stock_data(cur, conn):
    stock_exchange_df = pd.read_csv('data/indexData.csv')
    stock_info_df = pd.read_csv('data/indexInfo.csv')
    
    for value in stock_info_df.values:
        region, exchange, ticker_id, currency = value
        stock_info_data = (ticker_id, region, exchange, currency)

        #insert stock info data
        cur.execute(stock_info_table_insert, stock_info_data)
        conn.commit()

    print("Stock info insert succesful\n")
    
    # for value in stock_exchange_df.values:
    #     ticker, date, open_price, high_price, low_price, close_price, adj_close, volume = value
    #     stock_exchange_data = (ticker, date, open_price, high_price, low_price, close_price, adj_close, volume)
        
    #     #insert stock exchange data
    #     cur.execute(stock_exchange_table_insert, stock_exchange_data)
    #     conn.commit()

    stock_exchange_data = [{
                        'ticker':value[0], 
                        'date':value[1],
                        'open_price':value[2], 
                        'high_price':value[3], 
                        'low_price':value[4], 
                        'close_price':value[5], 
                        'adj_close':value[6], 
                        'volume':value[7]} for value in stock_exchange_df.values]

    psycopg2.extras.execute_batch(cur, stock_exchange_table_insert, stock_exchange_data)
    print("Exchange data insert succesful\n")


def process_time_date(cur,conn):
    df = pd.read_csv('data/indexData.csv')
    #convert string to datetime
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

    cal = calendar()
    holidays = cal.holidays(start=df["Date"].min(), end = df['Date'].max())

    #extract year, month, day, weekday, holiday from date column
    df['Year'] = df['Date'].dt.year
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Weekday'] = df['Date'].dt.day_name()
    df['Is_holiday'] = df['Date'].isin(holidays)

    time_df = df[['Date','Day','Month','Year','Weekday','Is_holiday']]
    
    #insert one-by-one is very slow
    # for value in time_df.values:
    #     exchange_date, year, month, day, weekday, is_holiday = value
    #     time_data = (exchange_date, day, month, year, weekday, is_holiday) 

    #     cur.execute(time_table_insert, time_data)
    #     conn.commit()
    all_time_data = [{
                    'exchange_date': value[0],
                    'day':value[1],
                    'month':value[2],
                    'year':value[3],
                    'weekday':value[4],
                    'is_holiday':value[5]} for value in time_df.values]
    
    psycopg2.extras.execute_batch(cur,time_table_insert, all_time_data)
    print('SUCCESS TO INSERT TIME TABLE')

def main():
    conn = psycopg2.connect("host=localhost dbname=stockhistory user=postgres password = bloodyangel23")
    cur = conn.cursor()

    process_time_date(cur,conn)
    extract_load_stock_data(cur,conn)

    conn.close()

     
if __name__ == "__main__":
    main()
    print("\n\nFinished processing!!!\n\n")
