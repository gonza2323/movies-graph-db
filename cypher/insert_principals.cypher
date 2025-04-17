UNWIND $rows AS row

MATCH (t:Play {id: row.titleId})
MATCH (p:Person {id: row.nameId})
CREATE (p)-[r:WORKS_IN {
  type:       row.category,
  job:        row.job,
  character: row.characters}]->(t)