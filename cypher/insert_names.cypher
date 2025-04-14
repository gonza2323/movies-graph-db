UNWIND $rows AS row
CREATE (p:Persona {
    id: row.id,
    primaryName: row.primaryName,
    birthYear: row.birthYear,
    deathYear: row.deathYear,
    primaryProfession: row.primaryProfession
})
WITH p, row.knownForTitles AS titleIds
UNWIND titleIds AS titleId
MATCH (o:Obra) WHERE o.id = titleId
CREATE (p)-[:CONOCIDA_POR]->(o)