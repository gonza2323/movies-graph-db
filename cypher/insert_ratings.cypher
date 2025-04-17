UNWIND $rows AS row

MATCH (t:Title {id: row.id})
SET
  t.averageRating = row.averageRating,
  t.numVotes = row.numVotes,
  t.weightedRating = row.weightedRating