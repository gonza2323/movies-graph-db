UNWIND $rows AS row
MATCH (o:Obra {id: row.titleId})
MATCH (p:Persona {id: row.nameId})
CREATE (p)-[r:TRABAJA_EN {
    tipo: row.category,
    job: row.job,
    characters: row.characters}]->(o)