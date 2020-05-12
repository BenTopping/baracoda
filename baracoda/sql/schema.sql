DROP SEQUENCE IF EXISTS heron;
CREATE SEQUENCE heron
START 200000;

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
