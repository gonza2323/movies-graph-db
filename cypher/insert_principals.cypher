UNWIND $rows AS row

MATCH (o:Play {id: row.titleId})
MATCH (p:Person {id: row.nameId})
CREATE (p)-[r:WORKS_IN {
  type:       row.category,
  job:        row.job,
  characters: row.characters}]->(o)