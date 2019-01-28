import aiosqlite
import asyncio
import os


async def make_database(db: str):
    if not os.path.isfile(db):
        users = """
            CREATE TABLE `Users` (
            `discord_id`    INTEGER,
            `gw2_name`      TEXT,
            `api`           TEXT,
            PRIMARY KEY(`discord_id`)
        );"""

        servers = """
        CREATE TABLE `Servers` (
            `server_id`         INTEGER,
            `owner_discord_id`  INTEGER,
            `owner_gw2_name`    TEXT,
            `guild_id`          TEXT,
            `api`               Text,
            PRIMARY KEY(`server_id`)
        );"""

        users_servers = """
        CREATE TABLE `UsersServers` (
            `id`        INTEGER PRIMARY KEY AUTOINCREMENT,
            `discord_id`   INTEGER,
            `server_id` INTEGER
        );"""
        async with aiosqlite.connect(db) as connection:
            cursor = await connection.cursor()
            await cursor.execute(users)
            await cursor.execute(servers)
            await cursor.execute(users_servers)
            await connection.commit()
        print(f"Created new database '{db}'")
    else:
        print(f"Delete the already excisting database file '{db}' before making a new one")


def make_database_with_loop(db):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_database(db))


if __name__ == '__main__':
    make_database_with_loop("db.db")
