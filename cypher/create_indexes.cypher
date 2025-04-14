CREATE INDEX index_person_name IF NOT EXISTS
FOR (n:Persona) ON (n.primaryName);

CREATE INDEX index_title_title IF NOT EXISTS
FOR (n:Obra) ON (n.primaryTitle);
CREATE INDEX index_title_year IF NOT EXISTS
FOR (n:Obra) ON (n.startYear);

CREATE INDEX index_title_title IF NOT EXISTS
FOR (n:movie) ON (n.primaryTitle);
CREATE INDEX index_title_year IF NOT EXISTS
FOR (n:movie) ON (n.startYear);