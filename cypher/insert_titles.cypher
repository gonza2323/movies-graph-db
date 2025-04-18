UNWIND $rows AS row

CREATE (t:Title:TitleType {
  id:             row.id,
  primaryTitle:   row.primaryTitle,
  originalTitle:  row.originalTitle,
  startYear:      row.startYear,
  endYear:        row.endYear,
  runtimeMinutes: row.runtimeMinutes
})
WITH t, row.genres AS genres
UNWIND genres AS genre
MERGE (g:Genre {type: genre})
CREATE (t)-[:HAS_GENRE]->(g)