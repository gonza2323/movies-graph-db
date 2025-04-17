UNWIND $rows AS row

MATCH (episode:Title {id: row.episodeId})
MATCH (series:Title {id: row.seriesId})
CREATE (episode)-[:EPISODE_OF {
  seasonNumber:  row.seasonNumber,
  episodeNumber: row.episodeNumber}]->(series)