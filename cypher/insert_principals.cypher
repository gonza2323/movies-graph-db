UNWIND $rows AS row
MATCH (o:Obra {id: row.titleId})
MATCH (p:Persona {id: row.nameId})
MERGE (p)-[r:TRABAJO_EN {tipo: row.category}]->(o)
SET r.job = row.job,
    r.characters = row.characters