
ALTER TABLE Image ADD COLUMN keywords VARCHAR(510) DEFAULT NULL;
ALTER TABLE Image ADD COLUMN is_in_generator BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE User ADD COLUMN `sys_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP;

