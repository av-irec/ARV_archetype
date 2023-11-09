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


def getSurfaces_ARV_1building(hostname,database,username,pwd,port_id,ref_cat):
    areabyCadastralcode = {}
    distributionRatio = {}
    ref_use = {}

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
        
        cur.execute('SELECT count(*) FROM citydb.building')  # Number of buildings in the DDBB
        num_buildings = 1
        areas = "SELECT sum(citydb.ST_3DArea(geometry)) FROM citydb.surface_geometry WHERE gmlid LIKE %s AND gmlid LIKE %s "  # SQL statment to get the areas according to type (floor-roof-wall)
        ref_cat_sql = "SELECT gmlid FROM citydb.cityobject WHERE id = %s AND gmlid = %s"  #  Get the  ref_cat of the buildings in the DDBB
        areabyCadastralcode[str(ref_cat)] = {}    # Dict with ref_cat as key. Within each ref_cat (key) another dict with surface type as key 

        for i in range(1,num_buildings+1):   # Loop to fill the dict "areabyCadastralcode" created in the previous loop
            ref_cat_comp = '%' + str(ref_cat) + '%'
            tuple_aux = (str(ref_cat_comp),'%floor%')
            cur.execute(areas,tuple_aux)    # Execute the SQL statment with str(i) -> cityobject_id and %floor$ -> LIKE statment
            area_floor = cur.fetchall()
            tuple_aux = (str(ref_cat_comp),'%roof%')
            cur.execute(areas,tuple_aux)
            area_roof = cur.fetchall()
            tuple_aux = (str(ref_cat_comp),'%wall%')
            try:
                cur.execute(areas,tuple_aux)
                area_wall = cur.fetchall()
            except:
                cur.execute("rollback")
                area_wall = [(0,)]                              
            areabyCadastralcode[ref_cat]['floor'] = area_floor[0][0]/2
            areabyCadastralcode[ref_cat]['roof'] = area_roof[0][0]/2
            areabyCadastralcode[ref_cat]['wall'] = area_wall[0][0]/2
            areabyCadastralcode[ref_cat]['total'] =area_floor[0][0] + area_roof[0][0] + area_wall[0][0]


        
        
        distribution_SQL = "SELECT parcela, referencia_catastral, coef_propiedad_divhor,clave_grupo_uso FROM catastro.tipo15_su WHERE parcela = %s"
        cur.execute(distribution_SQL,(str(ref_cat),))
        distributionBase = cur.fetchall()     # Get partition coefficient from cadaster DDBB
        for i in distributionBase:            # Generation of dict with the cadastral reference as a key (14 - building level)   
            distributionRatio[i[0]] = {}
            ref_use[i[0]] = {}
        for i in distributionBase:            # Generation of dict within "distributionRatio + ref_use" with the cadastral reference as a key (20 - dwelling level)
            distributionRatio[i[0]].setdefault(i[1],i[2])  
            ref_use[i[0]].setdefault(i[1],i[3]) 

        
            
        return areabyCadastralcode, distributionRatio, ref_use # 3 dicts outputs

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
    ref_cat = '1701521DD7810B'
    areabyCadastralcode, distributionRatio, ref_use = getSurfaces_ARV_1building(hostname,database,username,pwd,port_id,ref_cat) #SQL script
    print(areabyCadastralcode,distributionRatio,ref_use)
    
        
        
       
