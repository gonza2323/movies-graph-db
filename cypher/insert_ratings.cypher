UNWIND $rows AS row
MATCH (o:Obra {id: row.id})
SET o.averageRating = row.averageRating,
    o.numVotes = row.numVotes