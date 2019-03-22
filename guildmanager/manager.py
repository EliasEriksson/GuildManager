from typing import List
from collections import namedtuple
from . import exceptions
from . import PATH
import aiosqlite
import os

# TODO remove unused methods
# TODO change named tuples to EasyNamespace?
# TODO mothods returnign dict return EasyNamespace instead?


class Manager:
    """
    Manages database interactions
    """

    """
    namedtuples for the various tables and their fields
    """
    user_keys = namedtuple(
        "user_keys", ["discord_id", "gw2_name", "api"]
    )("discord_id", "gw2_name", "api")

    server_keys = namedtuple(
        "server_keys",
        ["server_id", "owner_discord_id", "owner_gw2_name", "guild_id", "api"]
    )("server_id", "owner_discord_id", "owner_gw2_name", "guild_id", "api")

    user_server_keys = namedtuple(
        "user_server_keys",
        ["discord_id", "server_id"]
    )("discord_id", "server_id")

    tables = namedtuple(
        "tables", ["users", "servers", "users_servers"]
    )("Users", "Servers", "UsersServers")

    def __init__(self, db: str) -> None:
        """
        initiates the instance with the database name

        :param db: str, the database file name
        """
        self.db = os.path.join(PATH, db)

    async def __aenter__(self) -> "Manager":
        """
        returns self just to be able to be used as a context manager
        TODO if its possible to open the connection here it would be better

        :return: self
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        required to not crash

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        pass

    async def add_user(self, discord_id: int, gw2_name: str, api: str) -> None:
        """
        adds a user to the user table

        strors the discord id, the gw2 account name and an api key

        :param discord_id: the discord users client id
        :param gw2_name:   the guild wars 2 account name (with numbers)
        :param api:        a guild wars 2 api key
        :return:           None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_user_command = f"""
            select 1 from {self.tables.users}
            where {self.user_keys.discord_id} = {discord_id}
            """

            add_user_command = f"""
            insert into {self.tables.users} (
                {", ".join(self.user_keys)}
            ) values (
                "{discord_id}", "{gw2_name}", "{api}"
            );"""

            await cursor.execute(check_user_command)
            user_excists = await cursor.fetchall()
            if not user_excists:
                await cursor.execute(add_user_command)
                await connection.commit()
            else:
                raise exceptions.UserAlreadyExcists(
                    f"User: {discord_id} already excists.")

    async def add_server(self, server_id: int, owner_discord_id: int,
                         owner_gw2_name: str, guild_id: str, api: str) -> None:
        """
        adds a server to the server table

        stores the discord servers id, discord servers name, the discord servers owners client id,
        the discord servers owners guild wars 2 account name (with numbers),
        the guild wars 2 guild id and the owners guild wars 2 api key

        :param server_id:        discord server id
        :param owner_discord_id: owners discord client id
        :param owner_gw2_name:   owners guild wars 2 account name
        :param guild_id:         guild wars 2 guild id
        :param api:              owners guild wars 2 api key
        :return:                 None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_server_command = f"""
            select 1 from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            add_server_command = f"""
            insert into {self.tables.servers} (
                {", ".join(self.server_keys)}
            ) values (
                {server_id}, {owner_discord_id}, 
                "{owner_gw2_name}", "{guild_id}", "{api}"
            );"""

            await cursor.execute(check_server_command)
            server_excists = await cursor.fetchall()
            if not server_excists:
                await cursor.execute(add_server_command)
                await connection.commit()
            else:
                raise exceptions.ServerAlreadyExcists(
                    f"Server: {server_id} already excists."
                )

    async def add_user_server(self, discord_id: int, server_id: int) -> None:
        """
        adds a link between a user and a discord server

        the link is an assosiation/membership between the user and the gw2 guild
        the discord client id and the server id can be used to query information from
        the database about the server / user from the server / user tables
        stores the users/members discord client id and the discord server id

        :param discord_id: users/members discord client id
        :param server_id:  discord servers id
        :return:           None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_users_command = f"""
            select 1 from {self.tables.users} 
            where {self.user_keys.discord_id} = {discord_id}
            """

            check_servers_command = f"""
            select 1 from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            check_entry_command = f"""
            select 1 from {self.tables.users_servers}
            where {self.user_server_keys.discord_id} = {discord_id}
            and {self.user_server_keys.server_id} = {server_id}
            """

            add_users_servers_command = f"""
            insert into {self.tables.users_servers} (
                {", ".join(self.user_server_keys)}
            ) values (
                "{discord_id}", "{server_id}"
            );"""

            await cursor.execute(check_users_command)
            user_excists = await cursor.fetchall()
            await cursor.execute(check_servers_command)
            server_excists = await cursor.fetchall()
            await cursor.execute(check_entry_command)
            entry_excists = await cursor.fetchall()
            if user_excists:
                if server_excists:
                    if not entry_excists:
                        await cursor.execute(add_users_servers_command)
                        await connection.commit()
                    else:
                        raise exceptions.UsersServersLinkAlreadyExcists(
                            f"the link between discord user {discord_id} and server "
                            f"{server_id} already excists"
                        )
                else:
                    raise exceptions.MissingServer(
                        f"Server: {server_id} is not yet registered."
                    )
            else:
                raise exceptions.MissingUser(
                    f"User: {discord_id} is not yet registered."
                )

    async def remove_user(self, discord_id: int) -> None:
        """
        removes a user from the users table and all links between its servers

        removes all information stored about the user including its asosiations with all
        registered stored discord servers

        :param discord_id: users discord client id
        :return:           None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_users_command = f"""
            select 1 from {self.tables.users} 
            where {self.user_keys.discord_id} = {discord_id}
            """

            remove_users_command = f"""
            delete from {self.tables.users}
            where {self.user_keys.discord_id} = {discord_id}
            """

            remove_users_servers_command = f""" 
            delete from {self.tables.users_servers} 
            where {self.user_server_keys.discord_id} = {discord_id}
            """

            await cursor.execute(check_users_command)
            user_excists = await cursor.fetchall()
            if user_excists:
                await cursor.execute(remove_users_command)
                await cursor.execute(remove_users_servers_command)
                await connection.commit()
            else:
                raise exceptions.MissingUser(
                    f"User with id {discord_id} doesn't excist"
                )

    async def remove_server(self, server_id: int):
        """
        removes a server from the server table and all its links between users

        removes all informations stored about the server including its assosiations with all
        registered users

        :param server_id: discord server id
        :return:          None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_server_command = f"""
            select 1 from {self.tables.servers} 
            where {self.server_keys.server_id} = {server_id}
            """

            remove_servers_command = f"""
            delete from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            remove_users_server_command = f"""
            delete from {self.tables.users_servers}
            where {self.user_server_keys.server_id} = {server_id}
            """

            await cursor.execute(check_server_command)
            server_excists = await cursor.fetchall()
            if server_excists:
                await cursor.execute(remove_servers_command)
                await cursor.execute(remove_users_server_command)
                await connection.commit()
            else:
                raise exceptions.MissingServer(f"Server with id {server_id} doesn't excist")

    async def unlink_user(self, discord_id: int, server_id: int):
        """
        unlinks a users assosiation with a server

        removes the link between a user and a server in the UsersServers table

        :param discord_id: users discord client id
        :param server_id:  discord server id
        :return:           None
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            check_users_servers_command = f"""
            select 1 from {self.tables.users_servers}
            where {self.user_server_keys.discord_id} = {discord_id} 
            and {self.user_server_keys.server_id} = {server_id}
            """

            unlink_command = f"""
            delete from {self.tables.users_servers}
            where {self.user_server_keys.discord_id} = {discord_id} 
            and {self.user_server_keys.server_id} = {server_id}
            """

            await cursor.execute(check_users_servers_command)
            users_server_excists = await cursor.fetchall()
            if users_server_excists:
                await cursor.execute(unlink_command)
                await connection.commit()
            else:
                raise exceptions.MissingUsersServer(
                    f"User id {discord_id} is not linked to server id {server_id}"
                )

    async def get_users(self) -> List[dict]:
        """
        queries the users table for all users

        queries and returns the users table and reformats the response from a tuple to a
        dictionary with the tables field names as the dictionarys keys

        :return: list of users as dictionary with database field names as keys
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select * from {self.tables.users}
            """

            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.user_keys, result)) for result in query]
        return query

    async def get_user(self, discord_id: int) -> dict:
        """
        queries the users table for a single user

        queries and returns a single user and reformats the response from a tuple to a
        dictionary with the tables field names as the dictionarys keys

        :param discord_id: users discord client id
        :return:           user as dictionary with database field names as keys
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select * from {self.tables.users}
            where {self.user_keys.discord_id} = {discord_id}
            """

            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.user_keys, result)) for result in query]
        if len(query) == 1:
            return query[0]
        return {}

    async def get_servers(self) -> List[dict]:
        """
        queries the servers table for all servers

        queries and returns the servers table and reformats the response from a tuple to a
        dictionary with the tables field names as the dictionaries keys

        :return: List[dict], list of users as dictionary with database field names as keys
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select * from {self.tables.servers}
            """

            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.server_keys, result)) for result in query]
        return query

    async def get_server(self, server_id: int) -> dict:
        """
        queries the servers table to a single server

        querieis and returns a single server and reformats the response from a tuple to a
        dictionary with the tables field names as the dictionarys keys

        :param server_id: servers discord id
        :return:          server as dictionary with database field names as keys
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select * from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.server_keys, result)) for result in query]
        if len(query) == 1:
            return query[0]
        else:
            return {}

    async def get_users_servers(self, discord_id: int, server_id: int) -> List[dict]:
        """
        queries all links between servers and users from the UsersServers table

        queries and returns the links between users and servers and reformats the response from a
        tuple to a dictionary with the talbes field names as the dictionaries keys

        :return: list of links as dictionary with database field names as keys
        """

        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select {self.user_server_keys.discord_id}, {self.user_server_keys.server_id} 
            from {self.tables.users_servers}
            where {self.user_server_keys.discord_id} = {discord_id}
            and {self.user_server_keys.server_id} = {server_id}
            """

            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.user_server_keys, result)) for result in query]
        return query

    async def get_servers_user(self, discord_id: int, server_id: int) -> dict:
        """
        queries a single link between a user and a server from the UserServers table

        queries and returns a link between a user and server and reformats the response from a
        tuple to a dictionary with tables field names as the dictionarys keys

        :param discord_id: clients discord id
        :param server_id:  discord server id
        :return:           a link as dictionary with database field names as keys
        """
        async with aiosqlite.connect(self.db) as connecton:
            cursor = await connecton.cursor()
            command = f"""
            select *
            from {self.tables.users}
            where {self.user_server_keys.discord_id} = (
                select {self.user_server_keys.discord_id}
                from {self.tables.users_servers}         
                where {self.user_server_keys.discord_id} = {discord_id}
                and {self.user_server_keys.server_id} = {server_id}
            )
            """
            await cursor.execute(command)
            query = await cursor.fetchall()
        query = [dict(zip(self.user_keys, result)) for result in query]
        if len(query) == 1:
            return query[0]
        else:
            return {}

    async def get_server_api(self, server_id: int) -> str:
        """
        queries a single servers api key

        queries and returns a guild wars 2 api key from a server

        :param server_id: discord server id
        :return:          guild wars 2 api key
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select {self.server_keys.api} from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """
            await cursor.execute(command)
            query = await cursor.fetchall()
            query = tuple(value for value in query)
            if len(query) == 1:
                # is str() needed here really?
                return query[0][0]
            return ""

    async def get_server_guild_id(self, server_id) -> str:
        """
        queries a single servers guild id

        queries and returns a connected discord servers afiliated guild wars 2 guild id

        :param server_id: discord server id
        :return:          guild wars 2 guild id
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select {self.server_keys.guild_id} from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            await cursor.execute(command)
            query = tuple(await cursor.fetchall())
        if len(query) == 1:
            return str(query[0][0])
        return ""

    async def server_excists(self, server_id: int):
        """
        checks if a server ixcists in the database

        checks if a discord server excists in the database evaluates to True or Fase
        :param server_id: discord server id
        :return:          True or False if it excists or not
        """
        async with aiosqlite.connect(self.db) as connection:
            cursor = await connection.cursor()

            command = f"""
            select 1 from {self.tables.servers}
            where {self.server_keys.server_id} = {server_id}
            """

            await cursor.execute(command)
            query = tuple(await cursor.fetchall())
        if query:
            return True
        return False


async def main():
    pass


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
