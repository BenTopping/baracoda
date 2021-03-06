DROP SEQUENCE IF EXISTS heron;
CREATE SEQUENCE heron
START 200000;

DROP SEQUENCE IF EXISTS ht;
CREATE SEQUENCE ht
START 111111;

DROP TABLE IF EXISTS barcodes;

CREATE TABLE barcodes
(
    id SERIAL,
    barcode VARCHAR(255) NOT NULL,
    prefix VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    barcodes_group_id integer,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS barcodes_groups;
CREATE TABLE barcodes_groups
(
    id SERIAL,
    created_at timestamp,
    PRIMARY KEY (id)
);


DROP TABLE IF EXISTS alembic_version;
CREATE TABLE alembic_version
(
    version_num character varying(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version
    (version_num)
VALUES
    ('a32c725ae353');