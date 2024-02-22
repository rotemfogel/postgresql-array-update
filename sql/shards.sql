CREATE SCHEMA IF NOT EXISTS index_metadata;
CREATE TABLE IF NOT EXISTS index_metadata.shards
(
    date_hour            bigint not null,
    table_url            text   not null,
    current_shard        smallint,
    shard_size           bigint,
    compacted            boolean,
    PRIMARY KEY (date_hour, table_url)
);
CREATE INDEX ON index_metadata.shards(compacted);
-- data
INSERT INTO index_metadata.shards
  (date_hour, table_url, current_shard, shard_size, compacted)
VALUES
  (2024022200, 's3://my_bucket/team_id=55555', 0, 0, true),
  (2024022201, 's3://my_bucket/team_id=55555', 0, 0, false),
  (2024022202, 's3://my_bucket/team_id=55555', 0, 0, false),
  (2024022203, 's3://my_bucket/team_id=55555', 0, 0, false),
  (2024022204, 's3://my_bucket/team_id=55555', 0, 0, false),
  (2024022205, 's3://my_bucket/team_id=55555', 0, 0, false);