import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    conn = psycopg2.connect("host=localhost dbname=test user=postgres password = bloodyangel23")
    conn.set_session(autocommit = True)
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS stockhistory")
    cur.execute("CREATE DATABASE stockhistory WITH ENCODING 'utf8' TEMPLATE template0")

    cur.close()

    conn = psycopg2.connect("host=localhost dbname=stockhistory user=postgres password = bloodyangel23")
    cur = conn.cursor()

    return cur, conn

def create_table(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def drop_table(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    cur, conn = create_database()

    drop_table(cur, conn)
    print("Table dropped successfully!!")

    create_table(cur, conn)
    print("Table created succesfully")

    conn.close()

if __name__ == "__main__":
    main()
    