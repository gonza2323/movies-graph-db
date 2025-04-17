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
MATCH (o:Title)
  WHERE o.id = titleId
CREATE (p)-[:KNOWN_FOR]->(o)