CREATE INDEX index_person_name IF NOT EXISTS
FOR (n:Person) ON (n.primaryName);

CREATE INDEX index_title_title IF NOT EXISTS
FOR (n:Title) ON (n.primaryTitle);

CREATE INDEX index_title_year IF NOT EXISTS
FOR (n:Title) ON (n.startYear);

CREATE INDEX index_title_title IF NOT EXISTS
FOR (n:movie) ON (n.primaryTitle);

CREATE INDEX index_title_year IF NOT EXISTS
FOR (n:movie) ON (n.startYear);