CREATE INDEX index_person_name FOR (n:Persona) ON (n.primaryName);

CREATE INDEX index_title_title FOR (n:Obra) ON (n.primaryTitle);
CREATE INDEX index_title_year FOR (n:Obra) ON (n.startYear);

CREATE INDEX index_title_title FOR (n:movie) ON (n.primaryTitle);
CREATE INDEX index_title_year FOR (n:movie) ON (n.startYear);