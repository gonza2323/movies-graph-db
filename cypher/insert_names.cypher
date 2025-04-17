UNWIND $rows AS row

CREATE (p:Person {
  id:                row.id,
  primaryName:       row.primaryName,
  birthYear:         row.birthYear,
  deathYear:         row.deathYear,
  primaryProfession: row.primaryProfession
})
WITH p, row.knownForTitles AS titleIds
UNWIND titleIds AS titleId
MATCH (t:Title)
  WHERE t.id = titleId
CREATE (p)-[:KNOWN_FOR]->(t)