import asyncio
from dataclasses import dataclass

import asyncpg


@dataclass
class Shard:
    date_hour: int
    table_url: str
    current_shard: int
    shard_size: int
    compacted: bool


async def get_uncompacted_shards(connection):
    records = await connection.fetch(
        """
        SELECT * 
          FROM index_metadata.shards 
         WHERE NOT compacted"""
    )
    shards = [Shard(**record) for record in records]
    return shards


async def run_example():
    connection = await asyncpg.connect("postgresql://postgres@127.0.0.1/postgres")
    shards = await get_uncompacted_shards(connection)
    print(shards)
    if shards:
        date_hours = [shard.date_hour for shard in shards]
        table_urls = [shard.table_url for shard in shards]
        await connection.execute(
            f"""
                WITH update_payload AS (
                  SELECT UNNEST($1::bigint[]) as date_hour, 
                         UNNEST($2::text[]) as table_url
                )
                UPDATE index_metadata.shards
                   SET compacted = true
                  FROM update_payload
                 WHERE update_payload.date_hour = index_metadata.shards.date_hour
                   AND update_payload.table_url = index_metadata.shards.table_url""",
            date_hours,
            table_urls,
        )
        shards = await get_uncompacted_shards(connection)
        print(shards)
    await connection.close()


if __name__ == "__main__":
    asyncio.run(run_example())
