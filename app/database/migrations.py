import sqlite3


def create_tables(conn: sqlite3.Connection):
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj             TEXT    UNIQUE NOT NULL,
            razao_social     TEXT    NOT NULL,
            nome_fantasia    TEXT,
            cnae             TEXT,
            fpas             TEXT,
            sindicato        TEXT,
            regime_tributario TEXT,
            email            TEXT,
            telefone         TEXT,
            ativo            INTEGER DEFAULT 1,
            created_at       TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nome            TEXT    NOT NULL,
            cpf             TEXT    NOT NULL,
            rg              TEXT,
            cargo           TEXT,
            salario         REAL    NOT NULL,
            data_admissao   TEXT    NOT NULL,
            empresa_id      INTEGER,
            nome_mae        TEXT,
            estado_civil    TEXT,
            jornada         TEXT    DEFAULT '44h semanais',
            dependentes     INTEGER DEFAULT 0,
            vale_transporte REAL    DEFAULT 0,
            ativo           INTEGER DEFAULT 1,
            created_at      TEXT    DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS rescisoes (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id       INTEGER,
            tipo_rescisao        TEXT    NOT NULL,
            data_aviso           TEXT,
            ultimo_dia           TEXT    NOT NULL,
            aviso_previo_dias    INTEGER DEFAULT 0,
            aviso_previo_tipo    TEXT,
            saldo_salario        REAL    DEFAULT 0,
            ferias_vencidas      REAL    DEFAULT 0,
            ferias_proporcionais REAL    DEFAULT 0,
            decimo_terceiro      REAL    DEFAULT 0,
            aviso_indenizado     REAL    DEFAULT 0,
            fgts_rescisao        REAL    DEFAULT 0,
            multa_fgts           REAL    DEFAULT 0,
            inss                 REAL    DEFAULT 0,
            irrf                 REAL    DEFAULT 0,
            valor_bruto          REAL    DEFAULT 0,
            valor_liquido        REAL    DEFAULT 0,
            saldo_fgts_total     REAL    DEFAULT 0,
            observacoes          TEXT,
            created_at           TEXT    DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS folhas (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id    INTEGER,
            mes               INTEGER NOT NULL,
            ano               INTEGER NOT NULL,
            salario_bruto     REAL    DEFAULT 0,
            horas_extras      REAL    DEFAULT 0,
            adicional_noturno REAL    DEFAULT 0,
            comissoes         REAL    DEFAULT 0,
            dsr               REAL    DEFAULT 0,
            fgts              REAL    DEFAULT 0,
            inss              REAL    DEFAULT 0,
            irrf              REAL    DEFAULT 0,
            vale_transporte   REAL    DEFAULT 0,
            descontos         REAL    DEFAULT 0,
            salario_liquido   REAL    DEFAULT 0,
            created_at        TEXT    DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
        )
    """)

    conn.commit()
