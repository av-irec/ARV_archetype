
from sqlalchemy import text


class DataProcessor:
    from sqlalchemy import text
    def __init__(self, engine):
        self.engine = engine

    def get_data(self, refcat_value):
        areabyCadastralcode = self._get_areaby_cadastralcode(refcat_value)
        distribution_ratio, ref_use = self._get_distribution_ratio_and_ref_use(refcat_value)
        return areabyCadastralcode, distribution_ratio, ref_use

    def _get_areaby_cadastralcode(self, refcat_value):
        query_refcat = text(
            """
            SELECT refcat, total_area_wall AS wall, floor_area::numeric(10, 2) AS floor, roof_area::numeric(10, 2) AS roof
            FROM visualization.surface_area
            where refcat = :refcat_value
            ;
            """
        )

        with self.engine.connect() as connection:
            result = connection.execute(query_refcat, {'refcat_value': refcat_value})
            areaby_cadastralcode = {}
            for row in result:
                areaby_cadastralcode = {
                    row[0]: {
                        'wall': float(row[1]),
                        'floor': float(row[2]),
                        'roof': float(row[3])
                    }
                }
        return areaby_cadastralcode

    def _get_distribution_ratio_and_ref_use(self, refcat_value):
        distribution_ratio = {}
        ref_use = {}
        query_dwellings = text(
            """    
            SELECT parcela, referencia_catastral, coef_propiedad_divhor,clave_grupo_uso
            FROM catastro.tipo15_su
            WHERE parcela IN (SELECT gmlid FROM citydb.cityobject)
            AND parcela = :refcat_value
            ;
            """
        )

        with self.engine.connect() as connection:
            result = connection.execute(query_dwellings, {'refcat_value': refcat_value})
            for row in result:
                parcela, refcat, coef, clave_grupo_uso = row
                if parcela not in distribution_ratio:
                    distribution_ratio[parcela] = {}
                distribution_ratio[parcela][refcat] = float(coef)
                if parcela not in ref_use:
                    ref_use[parcela] = {}
                ref_use[parcela][refcat] = str(clave_grupo_uso)

        return distribution_ratio, ref_use
