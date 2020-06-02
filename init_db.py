import psycopg2
from postgis.psycopg import register

# Give the appropriate credentials for your postgresql database
conn = psycopg2.connect(host='*******', user='*****', password='*******', port='****', dbname='*****')
register(conn)
curr = conn.cursor()
