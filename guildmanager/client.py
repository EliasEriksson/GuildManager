from typing import List
import asyncio
import re
from datetime import datetime
from .requester import Requester
from . import messages as mes
from .manager import Manager
from . import exceptions
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# TODO tell ppl not to start command in the private mssage unless told to do so
# TODO tell ppl what to name the api key to use if you dont know what to name it
# TODO if already registered change message of successful /register


class Client(discord.Client):
    def __init__(self) -> None:
        super(Client, self).__init__()
        self.commands = {
            re.compile(r"^/install$"):    self.install,
            re.compile(r"^/register"):    self.register,
            re.compile(r"^/uninstall"):   self.uninstall,
            re.compile(r"^/unregister$"): self.unregister,
            re.compile(r"^/refresh$"):    self.refresh,
            re.compile(r"^/unlink$"):     self.unlink,
            re.compile(r"^/help$"):       self.help}

        self.check_reply = {
            "api": re.compile(
                r"^[A-Z0-9]{8}-(?:[A-Z0-9]{4}-){3}[A-Z0-9]{20}-(?:[A-Z0-9]{4}-){3}[A-Z0-9]{12}$"),
            "1": re.compile(r"^1$"),
            "2": re.compile(r"^[1-2]$"),
            "3": re.compile(r"^[1-3]$"),
            "4": re.compile(r"^[1-4]$"),
            "5": re.compile(r"^[1-5]$"),
            "number": re.compile(r"^\d+$")}

        self.db = "db.db"

    async def check_commands(self, message: discord.Message) -> None:
        """
        checks a message for commands, if found call its method

        :param message: message from person who invoked the command
        :return: None
        """
        for command, func in self.commands.items():
            if command.fullmatch(message.content):
                await message.delete()
                await func(message)

    async def _ask_for(self, key: str, message: discord.Message, question: str) -> discord.Message:
        """
        ask the user for something

        question can be set to "" to wait for the last question to be answered
        aks the user a question and waits for a reply that matches a regex format

        :param key: key to regexmatch (key in self.check_reply)
        :param message: message that initially invoked teh command
        :param question: the text the user wil be sent in private message
        :return: a valid reply
        """
        if question:
            await message.author.dm_channel.send(question)

        try:
            reply: discord.Message = await self.wait_for(
                event="message",
                check=lambda m: m.author == message.author,
                timeout=300)
            if reply.channel == message.author.dm_channel:
                if self.check_reply[key].fullmatch(reply.content):
                    return reply
                else:
                    return await self._ask_for(key, message, mes.reply_error[key])
            else:
                for command in self.commands:
                    if command.fullmatch(reply.content):
                        raise exceptions.DoubleCommand(
                            f"executed new command {reply.content} before "
                            f"finishing the ongoing one")
            return await self._ask_for(key, message, "")

        except asyncio.TimeoutError:
            raise exceptions.Timeout

    async def install(self, message: discord.Message) -> None:
        """
        initiates the instalation of the bot to a server

        installs the bot to the server and asks the owner to register after success
        installing results in storage of information stored in the server table in database

        :param message: discord.Message
        :return: None
        """
        if "guild" in dir(message.channel):
            server = message.channel.guild
            if server:
                server_id = server.id
                owner_discord_id = server.owner_id
                await self._ensure_dm_excists(message)
                async with Manager(self.db) as manager:
                    if await manager.server_excists(server_id):
                        await message.author.dm_channel.send(mes.install.already_excists)
                        return
                    if not message.author.dm_channel:
                        await message.author.create_dm()

                    reply: discord.Message = await self._ask_for(
                        "2", message, mes.instatruell.introduction)

                    if reply.content == "1":
                        reply: discord.Message = await self._ask_for(
                            "api", message, mes.install.provide_api)
                        api = reply.content
                        async with Requester(api) as session:
                            guilds = await session.get_guilds()
                            question = (mes.install.guild_question.replace(
                                "[placeholder]", "\n".join(
                                    [f"{index+1}: {guild['name']} [{guild['tag']}]"
                                     for index, guild in enumerate(guilds)])))

                            reply: discord.Message = await self._ask_for(
                                str(len(guilds)), message, question)
                            guild = guilds[int(reply.content) - 1]

                            owner_gw2_name = await session.get_gw2_username()

                        try:
                            await manager.add_server(
                                server_id=server_id,
                                owner_discord_id=owner_discord_id,
                                owner_gw2_name=owner_gw2_name,
                                guild_id=guild["guild_id"],
                                api=api)

                            await message.author.dm_channel.send(mes.install.success)
                            reply = await self._ask_for("2", message, mes.install.register)
                            if reply.content == "1":
                                try:
                                    try:
                                        await manager.add_user(owner_discord_id, owner_gw2_name, api)
                                    except exceptions.UserAlreadyExcists:
                                        pass
                                    await manager.add_user_server(owner_discord_id, server_id)
                                    await message.author.dm_channel.send(mes.install.registered)
                                except exceptions.UsersServersLinkAlreadyExcists:
                                    message.author.dm_channel.send(mes.install.already_excists)
                            else:
                                await message.author.dm_channel.send(mes.install.not_registering)
                        except exceptions.ServerAlreadyExcists:
                            await message.author.dm_channel.send(mes.install.already_excists)
                    else:
                        await message.author.dm_channel.send(mes.install.api_help_1)
                        await asyncio.sleep(1)
                        await message.author.dm_channel.send(mes.install.api_help_2)
                        await asyncio.sleep(1)
                        await message.author.dm_channel.send(mes.install.api_help_3)
                        await asyncio.sleep(1)
                        reply = await self._ask_for("2", message, mes.install.api_help_4)
                        if reply.content == "1":
                            await self.install(message)

    @staticmethod
    async def _ensure_dm_excists(message: discord.Message) -> None:
        """
        ensures that a prvate chat with a user already excists

        call thisbefore trying to send a private message to a user

        :param message: message from the discord user who invoked a command
        :return: None
        """
        if not message.author.dm_channel:
            await message.author.create_dm()

    async def _ensure_roles_excists(self, server_id: int, ranks: List[str]) -> None:
        """
        creates a new roles on the server if they dont excist

        :param server_id: discord server id
        :param ranks: gw guild ranks for a guild
        :return: None
        """
        channel = self.get_channel(server_id)
        roles = [role.name for role in channel.guild.roles]
        if channel.guild:
            for rank in ranks:
                if rank not in roles:
                    await channel.guild.create_role(
                        name=rank,
                        reason="Excisting rank in guild does nto excist as role"
                               "in this discord"
                    )

    @staticmethod
    async def _register_with_excisting_user(
            message: discord.Message, manager: Manager, user: dict) -> None:
        """
        tries to link an excisting user to a server

        a helper method for Client.register() that tries to link an excisting
        user to a server

        :param message: original message that started the registering process
        :param manager: manager object used by self.register
        :param user: user information from databse in Users table
        :return: None
        """
        guild_master_api = await manager.get_server_api(message.author.guild.id)
        guild_id = await manager.get_server_guild_id(message.author.guild.id)

        if guild_master_api and guild_id:
            async with Requester(guild_master_api) as session:
                roster: List[dict] = await session.get_roster(guild_id)
            member_names = [member["name"] for member in roster]
            if user["gw2_name"] in member_names:
                try:
                    await manager.add_user_server(message.author.id, message.author.guild.id)
                    await message.author.dm_channel.send(mes.register.success)
                except exceptions.UsersServersLinkAlreadyExcists:
                    await message.author.dm_channel.send(mes.register.registered)
            else:
                await message.author.dm_channel.send(mes.register.not_member)
        else:
            await message.author.dm_channel.send(mes.register.server_not_installed)

    @staticmethod
    async def _remove_roles(member: discord.Member, *roles: discord.Role) -> None:
        """
        checks if a user have a role, if the user have it it gets removed

        :param member: discord server member to check
        :param roles: roles to try to remove
        :return: None
        """
        await member.remove_roles(*[role for role in roles if role in member.roles])

    @staticmethod
    async def _add_roles(member: discord.Member, *roles: discord.Member) -> None:
        """
        checs if a user have a role, if not add it

        :param member: discord server member to check
        :param roles: roles to try to add
        :return: None
        """
        await member.add_roles(*[role for role in roles if role not in member.roles])

    async def register(self, message: discord.Message) -> None:
        """
        registers a user to the bot

        registers a user to the bot and also tries to link it to a server

        :param message: original message that invoket the registration command
        :return: None
        """
        if "guild" in dir(message.channel):
            if message.channel.guild:
                await self._ensure_dm_excists(message)
                async with Manager(self.db) as manager:
                    user = await manager.get_user(message.author.id)
                    if user:
                        await self._register_with_excisting_user(message, manager, user)
                    else:
                        reply: discord.Message = await self._ask_for(
                            "3", message, mes.register.introduction)

                        if reply.content == "1":
                            reply: discord.Message = await self._ask_for(
                                "api", message, mes.register.provide_api)
                            async with Requester(reply.content) as session:
                                gw2_name = await session.get_gw2_username()
                            await manager.add_user(message.author.id, gw2_name, reply.content)
                            user = await manager.get_user(message.author.id)
                            await self._register_with_excisting_user(message, manager, user)

                        elif reply.content == "2":
                            await message.author.dm_channel.send(mes.register.api_help_1)
                            await asyncio.sleep(1)
                            await message.author.dm_channel.send(mes.register.api_help_2)
                            await asyncio.sleep(2)
                            await message.author.dm_channel.send(mes.register.api_help_3)
                            reply: discord.Message = await self._ask_for(
                                "2", message, mes.register.api_help_4)

                            if reply.content == "1":
                                await self.register(message)

                        else:
                            await message.author.dm_channel.send(mes.register.offended)

    async def unregister(self, message: discord.Message) -> None:
        """
        unregisters a user from the bot

        removes the user entry and its links to servers from the database

        :param message: original message that invoked the remove command
        :return: None
        """
        if "guild" in dir(message.channel):
            if message.channel.guild:
                await self._ensure_dm_excists(message)
                async with Manager(self.db) as manager:
                    user = await manager.get_user(message.author.id)
                    if user:
                        reply: discord.Message = await self._ask_for(
                            "2", message, mes.unregister.are_you_sure)
                        if reply.content == "1":
                            try:
                                await manager.remove_user(message.author.id)
                                await message.author.dm_channel.send(mes.unregister.success)
                            except exceptions.MissingUser:
                                await message.author.dm_channel.send(mes.unregister.not_registered)
                        else:
                            await message.author.dm_channel.send(mes.unregister.regret)
                    else:
                        await message.author.dm_channel.send(mes.unregister.not_registered)

    async def uninstall(self, message: discord.Message) -> None:
        """
        uninstalls the bot from the discord server/gw2 guild

        removes the server entry and all users_serversentries in the database

        :param message: original message that invoked the uninstall command
        :return: None
        """
        if "guild" in dir(message.channel):
            if message.channel.guild:
                await self._ensure_dm_excists(message)
                async with Manager(self.db) as manager:
                    server = await manager.get_server(message.channel.guild.id)
                    # TODO change to server excists
                    if server:
                        reply: discord.Message = await self._ask_for(
                            "2", message, mes.uninstall.are_you_sure)
                        if reply.content == "1":
                            try:
                                await manager.remove_server(message.channel.guild.id)
                                await message.author.dm_channel.send(mes.uninstall.success)
                            except exceptions.MissingServer:
                                await message.author.dm_channel.send(mes.uninstall.not_installed)
                        else:
                            await message.author.dm_channel.send(mes.uninstall.regret)
                    else:
                        await message.author.dm_channel.send(mes.uninstall.not_installed)

    async def unlink(self, message: discord.Message) -> None:
        """
        unlinks a user from a server

        unlinks a user but doesnt unregister the user from the bot.
        can re-register by running the `/register` command without passing any information

        :param message: original message that invoked the /unlink command
        :return: None
        """
        if message.channel.guild:
            await self._ensure_dm_excists(message)
            async with Manager(self.db) as manager:
                link = await manager.get_users_servers(message.author.id, message.channel.guild.id)
                # TODO implement Manager.link_excists()
                servers = [server["server_id"] for server in link]
                if message.channel.guild.id in servers:
                    reply: discord.Message = await self._ask_for(
                        "2", message, mes.unlink.are_you_sure)
                    if reply.content == "1":
                        try:
                            await manager.unlink_user(message.author.id, message.guild.id)
                            await message.author.dm_channel.send(mes.unlink.success)
                        except exceptions.MissingUsersServer:
                            await message.author.dm_channel.send(mes.unlink.not_linked)
                    else:
                        await message.author.dm_channel.send(mes.unlink.regret)
                else:
                    await message.author.dm_channel.send(mes.unlink.not_linked)

    async def help(self, message: discord.Message) -> None:
        """
        sends a help message to the user who invoked the command

        :param message: original message that invoked the command
        :return: None
        """
        await self._ensure_dm_excists(message)
        await message.author.dm_channel.send(mes.help.commands)

    async def refresh(self, message: discord.Message) -> None:
        """
        user prompted refresh command, refreshes a single server

        refreshes the server where the command was invoked

        :param message: the original message that invoked the command
        :return: None
        """
        if "guild" in dir(message.channel):
            async with Manager(self.db) as manager:
                server_data = await manager.get_server(message.guild.id)
                server = self.get_guild(server_data["server_id"])
            if server:
                await self._refresh_server(server, server_data, manager)
            else:
                # TODO error message here
                pass

    async def _refresh_all(self) -> None:
        """
        refreshes the ranks/roles on all linked users

        :return: None
        """
        async with Manager(self.db) as manager:
            servers = await manager.get_servers()
            for server_data in servers:
                server = self.get_guild(server_data["server_id"])
                if not server:
                    continue  # TODO clean this server from database first
                else:
                    await self._refresh_server(server, server_data, manager)

    async def _refresh_server(self, server, server_data, manager) -> None:
        """
        refreshes a single server

        helper function for self.refresh and self._refresh_all

        :param server:
        :param server_data:
        :param manager:
        :return:
        """
        async with Requester(server_data["api"]) as requester:
            roster = await requester.get_roster(server_data["guild_id"])
            ranks = await requester.get_ranks(server_data["guild_id"])

        await self._ensure_roles_excists(server_data["server_id"], ranks)
        roles = [role for role in server.roles if role.name in ranks]

        for server_member in server.members:
            app_user_data = await manager.get_servers_user(
                server_member.id, server_data["server_id"])
            if not app_user_data:
                await self._remove_roles(server_member, *roles)
                continue
            for member in [m for m in roster if app_user_data["gw2_name"] == m["name"]]:
                for role in roles:
                    if role.name == member["rank"]:
                        await self._add_roles(server_member, role)
                    else:
                        await self._remove_roles(server_member, role)

    async def rename(self, message: discord.message) -> None:
        """
        merges roles that have been renamed from ingame

        if a guild rank is renamed the bot have no way of knowing if its a new role or an old one
        being rename. This command is ment to merge and old ingame rank dsicrod role into
        the new discord role

        :param message: original message that invoked the command
        :return: None
        """
        # TODO implement
        pass

    async def on_ready(self) -> None:
        """
        refreshes the ranks/servers on boot and every 10 minute

        :return: None
        """
        print(f"Bot went online @ {datetime.now()}")

        await self._refresh_all()
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self._refresh_all, "interval", minutes=10)
        scheduler.start()

    async def on_message(self, message: discord.Message) -> None:
        """
        command handle

        :param message: any message the bot is going to see
        :return: None
        """
        if message.author != self.user:
            try:
                await self.check_commands(message)
            except exceptions.DoubleCommand:
                pass
            except exceptions.Timeout:
                await message.author.dm_channel.send(mes.timeout)


if __name__ == '__main__':
    pass
