select * from fallas_informaticas;

GRANT SELECT ON FALLAS_INFORMATICAS TO C##AGENTE;

commit

SELECT owner, table_name FROM all_tables WHERE table_name = 'FALLAS_INFORMATICAS';
SELECT table_name FROM user_tables WHERE LOWER(table_name) = 'fallas_informaticas';
SELECT table_name FROM user_tables WHERE LOWER(table_name) = 'FALLAS_INFORMATICAS';

SELECT table_name FROM user_tables;

DROP TABLE FALLAS_INFORMATICAS;


-- Mejor estructura para la tabla
CREATE TABLE FALLAS_INFORMATICAS (
    ID NUMBER GENERATED ALWAYS AS IDENTITY,
    CATEGORIA VARCHAR2(50),  -- Ej: "hardware", "software"
    SUBCATEGORIA VARCHAR2(50),  -- Ej: "pantalla", "almacenamiento"
    SINTOMA VARCHAR2(200) NOT NULL,
    CAUSA_PROBABLE VARCHAR2(200) NOT NULL,
    SOLUCION VARCHAR2(500) NOT NULL,
    PALABRAS_CLAVE VARCHAR2(200) NOT NULL,
    PRIORIDAD NUMBER(1),  -- 1-5 (5 = más urgente)
    PRIMARY KEY (ID)
);


CREATE INDEX IDX_FALLAS_CAT_PRI ON FALLAS_INFORMATICAS (CATEGORIA, PRIORIDAD);

commit

INSERT INTO FALLAS_INFORMATICAS 
(CATEGORIA, SUBCATEGORIA, SINTOMA, CAUSA_PROBABLE, SOLUCION, PALABRAS_CLAVE, PRIORIDAD)
VALUES 
('Hardware', 'Pantalla', 'Pantalla negra al encender', 'Fallo de alimentación o tarjeta gráfica defectuosa', 'Verificar conexiones y probar con otra tarjeta gráfica.', 'pantalla,negra,encender,tarjeta', 4);

INSERT INTO FALLAS_INFORMATICAS 
(CATEGORIA, SUBCATEGORIA, SINTOMA, CAUSA_PROBABLE, SOLUCION, PALABRAS_CLAVE, PRIORIDAD)
VALUES 
('Software', 'Sistema Operativo', 'El sistema se congela', 'Conflicto con drivers o software corrupto', 'Iniciar en modo seguro y desinstalar software reciente.', 'congelado,sistema,drivers,seguro', 3);

INSERT INTO FALLAS_INFORMATICAS 
(CATEGORIA, SUBCATEGORIA, SINTOMA, CAUSA_PROBABLE, SOLUCION, PALABRAS_CLAVE, PRIORIDAD)
VALUES 
('Hardware', 'Disco Duro', 'No se detecta el disco', 'Fallo físico del disco o cables sueltos', 'Revisar conexión SATA o cambiar el disco.', 'disco,no detecta,sata,falla', 5);

Buscar por palabra clave
SELECT * FROM FALLAS_INFORMATICAS 
WHERE LOWER(PALABRAS_CLAVE) LIKE '%pantalla%';

Buscar por categoría y subcategoría
SELECT * FROM FALLAS_INFORMATICAS 
WHERE CATEGORIA = 'Hardware' AND SUBCATEGORIA = 'Pantalla';

UPDATE FALLAS_INFORMATICAS
SET SOLUCION = 'Revisar la fuente de poder y reemplazar la tarjeta gráfica si es necesario.'
WHERE ID = 1;

select * from fallas_informaticas;

SELECT CATEGORIA, COUNT(*) AS TOTAL_FALLAS
FROM FALLAS_INFORMATICAS
GROUP BY CATEGORIA;
