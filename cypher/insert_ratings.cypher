UNWIND $rows AS row

MATCH (o:Play {id: row.id})
SET
  o.averageRating = row.averageRating,
  o.numVotes = row.numVotes
WITH o, row
SET o.weightedRating = row.weightedRating