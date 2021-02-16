
-- USER GROUP

CREATE TABLE UserGroup (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE UserGroupAssignment (
	group_id INT NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY (group_id, user_id),
	FOREIGN KEY (group_id) REFERENCES UserGroup (id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES User (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE UserGroupRight (
    group_id INT NOT NULL,
	resource VARCHAR(255) NOT NULL,
	parameter VARCHAR(255) DEFAULT NULL,
	PRIMARY KEY (group_id, resource),
	FOREIGN KEY (group_id) REFERENCES UserGroup (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE UserCompanyAssignment (
	user_id INT NOT NULL,
	company_id INT NOT NULL,
	PRIMARY KEY (user_id, company_id),
	FOREIGN KEY (user_id) REFERENCES User (id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (company_id) REFERENCES Company (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE UserRequest (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	user_id INT NOT NULL,
	status ENUM('NEW', 'IN PROCESS', 'PROCESSED') NOT NULL DEFAULT 'NEW',
	request TEXT(8192) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES User (id) ON UPDATE CASCADE ON DELETE CASCADE,
);

-- USER MODIFICATION

ALTER TABLE `User` ADD COLUMN is_admin BOOLEAN DEFAULT FALSE AFTER password;
ALTER TABLE `User` ADD COLUMN telephone VARCHAR(55) DEFAULT NULL AFTER password;
ALTER TABLE `User` ADD COLUMN is_active BOOLEAN DEFAULT FALSE AFTER is_admin;

-- ARTICLE MODIFICATION (FIELDS FOR JOB OFFER)

ALTER TABLE `Article` ADD COLUMN external_reference VARCHAR(50) DEFAULT NULL AFTER image;
ALTER TABLE `Article` ADD COLUMN link VARCHAR(550) DEFAULT NULL AFTER external_reference;
ALTER TABLE `Article` MODIFY COLUMN status ENUM('DRAFT', 'PUBLIC', 'ARCHIVE') DEFAULT 'DRAFT' AFTER `end_date`;
