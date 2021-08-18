#DROP TABLE

drop_stock_exchange_table = "DROP TABLE IF EXISTS stockexchange"
drop_stock_info_table = "DROP TABLE IF EXISTS stockinfo"
drop_time_table = "DROP TABLE IF EXISTS time"

#CREATE TABLE

stock_exchange_table_create = ("""CREATE TABLE IF NOT EXISTS stockexchange(
    exchange_id BIGSERIAL NOT NULL CONSTRAINT exchange_pk PRIMARY KEY,
    ticker VARCHAR(12) NOT NULL REFERENCES stockinfo(ticker_id),
    date DATE NOT NULL REFERENCES time(exchange_date),
    open_price DECIMAL,
    low_price DECIMAL,
    high_price DECIMAL,
    close_price DECIMAL,
    adjust_close DECIMAL,
    volume DECIMAL
)""")

stock_info_table_create = ("""CREATE TABLE IF NOT EXISTS stockinfo(
    ticker_id VARCHAR(12) NOT NULL CONSTRAINT ticker_pk PRIMARY KEY,
    region VARCHAR(50) NOT NULL,
    exchange VARCHAR(80) NOT NULL UNIQUE,
    currency VARCHAR(10) NOT NULL
)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
    exchange_date DATE NOT NULL CONSTRAINT date_pk PRIMARY KEY,
    day INT NOT NULL CHECK (day >= 0),
	month INT NOT NULL CHECK (month >= 0),
	year INT NOT NULL CHECK (year >= 0),
	weekday VARCHAR(10) NOT NULL,
    is_holiday BOOLEAN NOT NULL
)""")

#INSERT STOCK DATA

stock_exchange_table_insert = ("""INSERT INTO stockexchange VALUES (DEFAULT, %s, %s, %s, %s,%s, %s, %s, %s) """)

#updating stock information
stock_info_table_insert = ("""INSERT INTO stockinfo (ticker_id, region, exchange, currency) VALUES(%s, %s, %s, %s) ON CONFLICT (ticker_id) DO UPDATE SET exchange = EXCLUDED.exchange,currency = EXCLUDED.currency
""")

time_table_insert = ("""INSERT INTO time VALUES (%(exchange_date)s, %(day)s, %(month)s, %(year)s, %(weekday)s, %(is_holiday)s) ON CONFLICT (exchange_date) DO NOTHING;
""")

#QUERY LISTS

create_table_queries = [time_table_create, stock_info_table_create, stock_exchange_table_create]
drop_table_queries = [drop_stock_exchange_table,drop_time_table, drop_stock_info_table]