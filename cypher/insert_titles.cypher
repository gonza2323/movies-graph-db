UNWIND $rows AS row
CREATE (t:Obra:TitleType {
    id: row.id,
    primaryTitle: row.primaryTitle,
    originalTitle: row.originalTitle,
    isAdult: row.isAdult,
    startYear: row.startYear,
    endYear: row.endYear,
    runtimeMinutes: row.runtimeMinutes
})
WITH t, row.genres AS genres
UNWIND genres AS genre
MERGE (g:Genero {tipo: genre})
CREATE (t)-[:TIENE_GENERO]->(g)