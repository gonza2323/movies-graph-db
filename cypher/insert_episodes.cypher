UNWIND $rows AS row
MATCH (episode:Obra {id: row.episodeId})
MATCH (series:Obra {id: row.seriesId})
CREATE (episode)-[:EPISODIO_DE {
    seasonNumber: row.seasonNumber,
    episodeNumber: row.episodeNumber}]->(series)