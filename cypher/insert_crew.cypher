UNWIND $rows AS row
MATCH (o:Obra {id: row.titleId})
WITH o, 
     [id IN row.directors | {id: id, role: 'director'}] + 
     [id IN row.writers | {id: id, role: 'writer'}] AS people

UNWIND people AS personData
MATCH (p:Persona {id: personData.id})
MERGE (p)-[:TRABAJO_EN {tipo: personData.role}]->(o)