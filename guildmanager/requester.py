from typing import List
# from .easy_namespace import EasyNamespace as EN
from . import exceptions
import aiohttp

# TODO use EasyNamespace instead of dict


class Requester:
    """
    manages requests to the guild wars 2 api
    """

    def __init__(self, api) -> None:
        """
        initiates the instance with the api key

        :param api: str, the guild wars 2 api key
        """
        self.api = api

    async def __aenter__(self) -> "Requester":
        """
        initiates the client session

        initiates the clients session and applies the api key to the header for
        authorization when requesting the gw2 api

        :return: self
        """

        header = {"Authorization": f"Bearer {self.api}"}
        self.session = aiohttp.ClientSession(headers=header)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        closes the client session

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """

        await self.session.close()

    async def get_guilds(self) -> List[dict]:
        """
        retrives guild information from the guild wars 2 api

        retrives the guild name, guild tag and the guilds ranks from each guild the
        owner of the api is guild leader of and returns each guild as a dictionary
        in a list

        :return: a list of guilds as dictionaries
        """

        guild_ids = None
        account_url = f"https://api.guildwars2.com/v2/account"
        async with self.session.get(account_url) as response:
            if not response.status == 200:
                raise exceptions.RequestNotSuccessfull(
                    f"Unsuccessful request for url {account_url}\n"
                    f"status {response.status}")
            account = await response.json()
            guild_ids = account["guild_leader"]
        guilds = []
        for guild_id in guild_ids:
            guild_name_url = f"https://api.guildwars2.com/v2/guild/{guild_id}"
            async with self.session.get(guild_name_url) as response:
                if not response.status == 200:
                    raise exceptions.RequestNotSuccessfull(
                        f"Unsuccessful request for url {guild_name_url}\n"
                        f"status {response.status}")
                guild = await response.json()

            ranks_url = f"https://api.guildwars2.com/v2/guild/{guild_id}/ranks"
            async with self.session.get(ranks_url) as response:
                if not response.status == 200:
                    raise exceptions.RequestNotSuccessfull(
                        f"Unsuccessful request for url {ranks_url}\n"
                        f"status {response.status}")
                ranks = await response.json()
                ranks = [rank["id"] for rank in ranks]
            guilds.append({
                "guild_id": guild_id,
                "name": guild["name"],
                "tag": guild["tag"],
                "ranks": ranks})

        return guilds

    async def get_roster(self, guild_id: str) -> List[dict]:
        """
        retrives the guilds roster from the guild wars 2 api

        retrives the name and the rank for each player in the guild and returns each player as
        a dictionary in a list

        :param guild_id: guild wars 2 guild id
        :return: a list of players as dictionaries
        """

        roster_url = f"https://api.guildwars2.com/v2/guild/{guild_id}/members"
        async with self.session.get(roster_url) as response:
            if not response.status == 200:
                raise exceptions.RequestNotSuccessfull(
                    f"Unsuccessful request for url {roster_url}\n"
                    f"status {response.status}")
            members = await response.json()
            roster = []
            for member in members:
                roster.append({"name": member["name"], "rank": member["rank"]})
            return roster

    async def get_ranks(self, guild_id: str) -> List[str]:
        """
        retrives the ranks for a guild

        :param guild_id: guild wars 2 guild id
        :return: list of the ranks as strings
        """
        ranks_url = f"https://api.guildwars2.com/v2/guild/{guild_id}/ranks"
        async with self.session.get(ranks_url) as response:
            if not response.status == 200:
                raise exceptions.RequestNotSuccessfull(
                    f"Unsuccessful request for url {ranks_url}\n"
                    f"status {response.status}")
            ranks = [rank["id"] for rank in await response.json()]
            return ranks

    async def get_gw2_username(self) -> str:
        """
        retrives the gw2 username of the api owner

        :return: gw2 username
        """
        url = "https://api.guildwars2.com/v2/account"
        async with self.session.get(url) as response:
            if response.status == 403:
                raise exceptions.RequestAuthenticationError(
                    f"Invalid api key: '{self.api}'"
                )
            if not response.status == 200:
                raise exceptions.RequestNotSuccessfull(
                    f"Unsuccessful request for url {url}\n"
                    f"status {response.status}")

            account = await response.json()
            return account["name"]

    async def valid_api(self):
        url = "https://api.guildwars2.com/v2/tokeninfo"
        async with self.session.get(url) as response:
            if not response.status == 200:
                raise exceptions.RequestNotSuccessfull(
                    f"Unsuccessful request for url {url}\n"
                    f"status {response.status}")
            token_info = await response.json()
            if "account" in token_info["permissions"]:
                if "guilds" in token_info["permissions"]:
                    return True
            return False


async def main():
    pass


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
