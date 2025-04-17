UNWIND $rows AS row

MATCH (t:Play {id: row.id})
SET
  t.averageRating = row.averageRating,
  t.numVotes = row.numVotes,
  t.weightedRating = row.weightedRating