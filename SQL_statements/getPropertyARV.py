# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:31:45 2022

@author: srabadan
"""

# >>>>>>> SQL BASIC STATMENTS <<<<<<<

# DELETE FROM 'table_name' --> Remove data from a table
# DROP TABLE IF EXISTS 'table_name' --> Remove the tabla and the data
# CREATE TABLE IF NOT EXISTS 'table_name' (columns) --> columns must be (variable typevar); typevar = int, varchar, geometry
# INSERT INTO 'table_name' (columns) VALUES (...) --> (...) =  %s if the value has to change or the value if it is constant
# SELECT * FROM 'table_name' WHERE 'conditions' + cur.fetchall() --> Read the data form the database

# >>>>>>> SQL-cur/con BASIC COMMANDS <<<<<<<

# cur.execute(SQL STATMENT) --> Execute directly a SQL statment

# cur.execute(X,Y) --> Inside a loop
# --> X = SQL statement with values to be changed
# --> Y = tuple with values

# con.commint() --> Refresh tables in PostgreSQL --> Must appear after each change in the databases.

# >>>>>>> PostgreSQL - PostGIS BASIC STATMENTS <<<<<<<

# SELECT ST_AsText(geometry) FROM 'table_name' WHERE 'conditions' + cur.fetcall() --> Read the geometry as a POLYGONS
# SELECT ST_3DExtent(geometry) FROM 'table_name' WHERE 'conditions' + cur.fetcall() --> Calculate box containing a Geometry (all rows of the table)
# SELECT ST_Xmax(ST_3DExtent(geometry)) FROM 'table_name' WHERE 'conditions' + curfetcall() --> Calculate max/min(x,y,z) from a 3Dbox

# >>>>>>> 3DCityDB tables <<<<<<< 

# 1) citydb.cityobject -> All the objects in the geometry (POLYGONZ + BUILDINGS)
# 2) citydb.surface_geometry -> Composition of surfaces
# 3) citydb.building -> Definition of buidings
# 4) citydb.thematic_surface -> Definition of types of polygons (wall - roof - floor)


def getProperty_ARV(hostname,database,username,pwd,port_id):

    import psycopg2             # SQL librarie
    cur = None                  # Conection cursor (psycopg2)
    conn = None                 # Conection (psycopg2)
    try:                        # All SQL statements must be in a 'try' statement. If an error occurs, display the error at the end.
        conn = psycopg2.connect(  # Use 'conn' to conect .py to PostgreSQL
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        cur = conn.cursor()       # cur will be our variable to make SQL statments
        
        cur.execute("SELECT ref_cat, destino, cif, apenom FROM social.propietarios WHERE destino = 'Residencial' ")  # Number of buildings in the DDBB
        property_output = cur.fetchall()    
        dict_owner = {}
        list_cif = ['A','B','C','D','E','F','G','H','J','N','P','Q','R','S','U','V','W']       # List of CIF first letter 
    
        
        for i in property_output:            
            dict_owner.setdefault(i[0],)
            dict_owner[i[0]] = {'ref_use' : i[1], 'cif' : i[2], 'owner' : i[3], 'entity':0}
            if dict_owner[i[0]]['cif'][0] in list_cif:
                dict_owner[i[0]]['entity'] = 'legal'
            else:
                dict_owner[i[0]]['entity'] = 'owner'
        dict_owner_def = {}        
        for i in dict_owner:
            dict_owner_def.setdefault(i[:14],{})
        ref_cat_keys = dict_owner_def.keys()    
        for i in dict_owner:
            for j in ref_cat_keys:
                if j in i:
                    dict_owner_def[j].setdefault(str(i),dict_owner[i])
                  
            
        return dict_owner_def

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
       


if __name__ == '__main__':
    hostname = "172.16.27.100"      # Database in the PC
    database = "ARV_district_buildings"   # Set the database
    username = "postgres"       # Username in PostgreSQL
    pwd = "GeoTerm2023@@"                # Passwod in PostgreSQL
    port_id = 5432              # Port in PostgreSQL
    dict_owner_def = getProperty_ARV(hostname,database,username,pwd,port_id) #SQL script
    print(dict_owner_def)
        
    
        
        
       
