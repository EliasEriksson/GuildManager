from guildmanager.client import Client

"""
Notes:
    # use this link to add the bot to a server
    https://discordapp.com/oauth2/authorize?client_id=523300141835354161&permissions=268445696&scope=bot
    # To check if a player was kicked from the guild, take the players in the discord server and
    see who is in the guild roseter, if in the discord list and not in guild -> left/kicked
"""

if __name__ == '__main__':
    client = Client()
    client.boot()
