CREATE CONSTRAINT title_id_unique IF NOT EXISTS
FOR (t:Play)
REQUIRE t.id IS UNIQUE;