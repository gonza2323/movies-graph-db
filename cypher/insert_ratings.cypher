UNWIND $rows AS row

MATCH (o:Obra {id: row.id})
SET
  o.averageRating = row.averageRating,
  o.numVotes = row.numVotes
WITH o, row
WHERE row.weightedRating IS NOT NULL
SET o.weightedRating = row.weightedRating