SELECT 'mur' as tipus,
       convecional_eco,
       opcion,
       espesor_w as espesor,
       espesor_mm,
       cost_instal_lat_euro_m2 as cost

from archetype.murs

WHERE arquetipo = :Arquetipo

UNION

SELECT 'coberta'               as tipus,
       convecional_eco,
       opcion,
       espesor_r               as espesor,
       espesor_aïllament_mm    as espesosr_mm,
       cost_instal_lat_euro_m2 as cost
from archetype.cobertes
WHERE arquetipo = :Arquetipo

UNION

SELECT 'finestra'               as tipus,
       convecional_eco,
       '0' as opcion,
       '0 '              as espesor,
       0    as espesosr_mm,
       cost_instal_lat_euro_m2 as cost
from archetype.finestres
WHERE arquetipo = 'All'

UNION

SELECT 'forjat'               as tipus,
       convecional_eco,
       '0' as opcion,
       espesor_s             as espesor,
       espesor_mm    as espesosr_mm,
       cost_instal_lat_euro_m2 as cost
from archetype.forjats
WHERE arquetipo = :Arquetipo