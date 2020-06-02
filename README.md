# Taxi-Ridesharing-Team-6--Big-Data-Analysis

## Instructions:
  - Create a PostGreSQL 12 Database and enable the postgis extension by executing the following command in the query tool (ensure that you have the postgis extension installed, otherwise use the application stack builder bundled with postgresql to install it):
  ```
    create extension postgis;
  ```  
  - Import the tables from the sql files provided in the repository (Ensure that you have the psql command line query tool installed, added to ENV PATH, and then run the following in your regular command line):
  ```
  psql -U db_username -p db_port -d database_name < path to sql file (Enter your db password if prompted to)
  
  ```
  
  - Run the above command for all 4 sql files (*disc_manhattan_points.sql*, *dropoffs_5_table.sql*, *dropoffs_10_table.sql* and  *lag_pt_dist_time.sql*)
  - The Tables will be added to your database for querying
  - Python version used is 3.7.4.
  - Provide the same database credentials in the *init_db.py* file
  - Connect the program environment to the postgresql database and install the psycopg2 library for python.
  - Running the program:
    - To start with, you would need to edit the *main.py* file to open the correct trips file by providing the correct path to it.
    - Change the direction in the main.py file to be either *from* (from laguardia) or *to* (to laguardia)
    - You would also need to edit the *initialize_10min_pools.py* or the *initialize_5min_pools.py* file (whichever pool window size required)
    - In those files, change the path and the pool_info json file name being saved. That file will be overwritten everytime a new pool has finished processing.
    - To enable or disable the optimization mentioned in the report, edit the *process_pools_from_laguardia.py* or the *process_pools_to_laguardia.py* file(as per the trip direction being considered). In this file, you just need to comment or uncomment the indicated lines.
    
    - All the above steps for running the program are provided as inline comments in the code themselves in the appropriate locations.
    
  - After all required pools have finished processing, open the required info file in *main.py* as directed inline, and use the helper functions provided below it to compute the final results (distance saved, trips saved and runtime)
