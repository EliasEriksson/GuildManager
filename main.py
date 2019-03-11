from guildmanager.client import Client
import json
import os

"""
Notes:
    # use this link to add the bot to a server
    https://discordapp.com/oauth2/authorize?client_id=523300141835354161&permissions=268445696&scope=bot
    # To check if a player was kicked from the guild, take the players in the discord server and
    see who is in the guild roseter, if in the discord list and not in guild -> left/kicked
"""


def load_token(filename="secret.json"):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename) as f:
        file = json.load(f)
    return file["client_token"]


if __name__ == '__main__':
    token = load_token()
    client = Client()
    client.run(token)
