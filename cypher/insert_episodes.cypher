UNWIND $rows AS row

MATCH (episode:Play {id: row.episodeId})
MATCH (series:Play {id: row.seriesId})
CREATE (episode)-[:EPISODE_OF {
  seasonNumber:  row.seasonNumber,
  episodeNumber: row.episodeNumber}]->(series)