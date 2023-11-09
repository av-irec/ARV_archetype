from sqlalchemy import create_engine, text

db_params = {
    'user': 'postgres',
    'password': 'sichuan93',
    'host': 'localhost',
    'port': '5433',  # Replace with the actual port number
    'database': 'ARV_district_buildings',
}

# Construct the SQLAlchemy connection string
db_connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

valid_refcats = []
invalid_refcats = []

# Create a SQLAlchemy engine
engine = create_engine(db_connection_string)

try:
    # Fetch distinct LEFT(gmlid, 14) values from the table
    with engine.connect() as connection:
        distinct_refcats = connection.execute(text("""
            SELECT DISTINCT LEFT(gmlid, 14) as refcat
            FROM citydb.surface_geometry;
        """)).fetchall()

        # Iterate through the distinct refcat values
        for refcat_row in distinct_refcats:
            iterator = refcat_row[0]

            # Construct the SQL query with the current refcat value
            sql_query = text(f"""
                SELECT LEFT(gmlid, 14) as refcat,
                SUM(citydb.st_3darea(geometry)) as area_total,
                SUM(CASE WHEN gmlid LIKE '%roof%' THEN citydb.ST_3DArea(geometry) ELSE 0 END) AS area_roof,
                SUM(CASE WHEN gmlid LIKE '%wall%' THEN citydb.ST_3DArea(geometry) ELSE 0 END) AS area_wall,
                SUM(CASE WHEN gmlid LIKE '%floor%' THEN citydb.ST_3DArea(geometry) ELSE 0 END) AS area_floor
                FROM citydb.surface_geometry
                WHERE LEFT(gmlid, 14) = :iterator
                GROUP BY refcat;
            """).params(iterator=iterator)

            try:
                result = connection.execute(sql_query).fetchone()
            except Exception as query_exception:
                print(f"Error executing SQL query for iterator '{iterator}': {query_exception}")
                continue  # Continue to the next iteration if there's an exception

            # Check if a result is valid or invalid
            if result:
                valid_refcats.append(result[0])  # Appending the refcat to the valid list
            else:
                invalid_refcats.append(iterator)  # Appending the refcat to the invalid list

except Exception as e:
    print(f"Error: {e}")
    # Handle the error gracefully, e.g., logging or specific error handling

# Print the results
print("Valid refcats:", len(valid_refcats))
print("Invalid refcats:", len(invalid_refcats))