

WITH count_apts AS (
    SELECT
        planta,
        COUNT(*) AS suma_pisos_planta
    FROM
        catastro.tipo15_su
    WHERE
        parcela IN (SELECT gmlid FROM citydb.cityobject)
        AND parcela = :parcela
    AND clave_grupo_uso = 'V'
    GROUP BY planta
)

SELECT
    CASE
        WHEN planta = (SELECT min(planta) FROM count_apts) THEN 'BF'
        WHEN planta = (SELECT max(planta) FROM count_apts) THEN 'TF'
        ELSE 'IF'
    END AS GROUP_APT,
    COUNT(
        CASE
            WHEN planta = (SELECT min(planta) FROM count_apts) THEN planta
            WHEN planta = (SELECT max(planta) FROM count_apts) THEN planta
            ELSE planta
        END
    ) AS count_plantes,

    SUM(
        CASE
            WHEN planta = (SELECT min(planta) FROM count_apts) THEN suma_pisos_planta
            WHEN planta = (SELECT max(planta) FROM count_apts) THEN suma_pisos_planta
            ELSE suma_pisos_planta
        END
    ) AS SUM_pisos
FROM count_apts
GROUP BY GROUP_APT;