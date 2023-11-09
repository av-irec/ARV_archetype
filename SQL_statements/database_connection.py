from urllib.parse import quote_plus
from sqlalchemy import create_engine

db_params = {'user' : 'postgres',
'password' : 'GeoTerm2023@@',
'host' : '172.16.27.100' , # Usually 'localhost' if the database is running on your local machine
'port' : '5432',  # The default port for PostgreSQL is 5432
'database' : 'ARV_district_buildings'}

quoted_password = quote_plus(db_params['password'])
# Construct the SQLAlchemy connection string
db_connection_string = f"postgresql://{db_params['user']}:{quoted_password}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

engine = create_engine(db_connection_string)
