UNWIND $rows AS row

CREATE (t:Play:TitleType {
  id:             row.id,
  primaryTitle:   row.primaryTitle,
  isAdult:        row.isAdult,
  startYear:      row.startYear,
  endYear:        row.endYear,
  runtimeMinutes: row.runtimeMinutes
})
WITH t, row.genres AS genres
UNWIND genres AS genre
MERGE (g:Genre {tipo: genre})
CREATE (t)-[:HAS_GENRE]->(g)