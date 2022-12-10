SET SQL DIALECT 3;



/******************************************************************************/
/****                                Tables                                ****/
/******************************************************************************/


CREATE GENERATOR ID_CADASTRO_IMC;

CREATE TABLE IMC_CADASTRO (
    ID             INTEGER NOT NULL,
    NOME           VARCHAR(100),
    ENDERECO       VARCHAR(100),
    ALTURA         FLOAT,
    PESO           FLOAT,
    IMC_RESULTADO  FLOAT
);



/******************************************************************************/
/****                               Triggers                               ****/
/******************************************************************************/



SET TERM ^ ;



/******************************************************************************/
/****                         Triggers for tables                          ****/
/******************************************************************************/



/* Trigger: TG_CAD_IMC */
CREATE OR ALTER TRIGGER TG_CAD_IMC FOR IMC_CADASTRO
ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
    NEW.ID = GEN_ID(ID_CADASTRO_IMC, 1);
END
^
SET TERM ; ^



/******************************************************************************/
/****                              Privileges                              ****/
/******************************************************************************/




/******************************************************************************/
/****                                Tables                                ****/
/******************************************************************************/



CREATE TABLE IMC_CONDICAO (
    CONDICAO  VARCHAR(100),
    MINIMO    FLOAT,
    MAXIMO    FLOAT,
    ID        INTEGER NOT NULL
);



/******************************************************************************/
/****                             Primary keys                             ****/
/******************************************************************************/

ALTER TABLE IMC_CONDICAO ADD CONSTRAINT IMC_CONDICAO_PK PRIMARY KEY (ID);


/******************************************************************************/
/****                              Populando                               ****/
/******************************************************************************/



INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Muito abaixo do peso', 0, 17, 1);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Abaixo do peso', 17, 18.4899997711182, 2);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Peso normal', 18.5, 24.9899997711182, 3);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Acima do Peso', 25, 29.9899997711182, 4);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Obesidade I', 30, 34.9900016784668, 5);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Obesidade II (severa)', 35, 39.9900016784668, 6);
INSERT INTO IMC_CONDICAO (CONDICAO, MINIMO, MAXIMO, ID)
                  VALUES ('Obesidade III (morbida)', 40, 200, 7);
				  
COMMIT WORK;
