UNWIND $ROWS AS row

MATCH (o:Play {id: row.titleId})
MATCH (p:Person {id: row.nameId})
CREATE (p)-[r:WORKS_IN {
  tipo:       row.category,
  job:        row.job,
  characters: row.characters}]->(o)