import os
import csv
import time

import psycopg2
import psycopg2.extras
from psycopg2 import sql


# Database connection parameters
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


# Function to batch insert records into the imdb database
def batch_insert(conn, data):
    with conn.cursor() as cursor:
        insert_query = sql.SQL(
            """ INSERT INTO public.imdb (poster_link, series_title, released_year, 
                                        _certificate, runtime, genre, imdb_rating, overview, 
                                        meta_score, director,star1, star2, star3, star4, 
                                        no_of_votes, gross)
                VALUES %s """
        )
        psycopg2.extras.execute_values(
            cursor, insert_query, data, template=None, page_size=100
        )
        conn.commit()


def main():
    conn_str = f"dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}' host='{DB_HOST}' port='{DB_PORT}'"
    conn = psycopg2.connect(conn_str)
    print("Connected to the database!")

    # Main loop to continuously insert records
    try:
        
        directory = "data"

        # iterate over data files in the directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                with open(f, "r", encoding="utf-8") as csvfile:
                    # Read the csv file, and insert records into PostgresDB
                    reader = csv.DictReader(csvfile)
                    records_list = [tuple(r.values()) for r in reader]
                    batch_insert(conn, records_list)

    except Exception as e:
        raise e
    finally:
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
