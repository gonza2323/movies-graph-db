UNWIND $rows AS row
MATCH (t:Title {id: row.titleId})
WITH t, 
     [id IN row.directors | {id: id, role: 'director'}] + 
     [id IN row.writers | {id: id, role: 'writer'}] AS people

UNWIND people AS personData
MATCH (p:Person {id: personData.id})
MERGE (p)-[:WORKS_IN {type: personData.role}]->(t)