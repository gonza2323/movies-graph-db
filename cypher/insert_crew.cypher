UNWIND $rows AS row
MATCH (o:Title {id: row.titleId})
WITH o, 
     [id IN row.directors | {id: id, role: 'director'}] + 
     [id IN row.writers | {id: id, role: 'writer'}] AS people

UNWIND people AS personData
MATCH (p:Person {id: personData.id})
MERGE (p)-[:WORKS_IN {type: personData.role}]->(o)