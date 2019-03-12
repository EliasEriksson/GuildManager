from .easy_namespace import EasyNamespace as EN

"""
a file denoted to all the text that will be sent to a user
"""


messages = EN({
    "install": {
        "introduction":
            "Hello! In order for me to be able to manage the roles and ranks for this "
            "discord server I need a bit of extra information. "
            "I can get all the information I need if you give me a Guild Wars 2 API key "
            "with permissions to access at least  'guild' and 'account' information. "
            "Do you know how to get me one of these API keys? :) "
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "provide_api":
            "Please provide your Guild Wars 2 API key with at least 'guild' and 'account' "
            "accessibility.",
        "api_help_1":
            "You are able to create a Guild Wars 2 API key if you visit your Guild Wars 2 "
            "account page over at https://account.arena.net/applications",
        "api_help_2":
            "To create a new API key simply hit 'New Key' https://tinyurl.com/NewGw2Api",
        "api_help_3":
            "Give it a cool name specific to this application and make sure the 'account' "
            "and 'guild' checkboxes are marked then simply hit 'Create API Key' "
            "https://tinyurl.com/MakeGw2Api\n\n",
        "api_help_4":
            "Do you want to continue the install? C:"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "guild_question":
            "You are guild_leader in the following guilds:\n```"
            "[placeholder]"
            "```\nWhich one would you want to associate with this discord server?",
        "success":
            "I am now 101% up and running, from now on I will keep track of the roles of "
            "every single registered user in this discord server o/.",
        "register":
            "Do you want me to register you aswell while we are at it? I got all the "
            "information I need about you to do so right now anyway"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "registered":
            "Now you are registered aswell, just make sure the rest of your guild members "
            "register themselves aswell or else im not really going to do anything.",
        "not_registering":
            "When you want to register just run the `/register` command in the server chat again.",
        "already_excists":
            "This server is already connected to a guild, run `/uninstall` before you try to "
            "install another guild."
    },
    "register": {
        "introduction":
            "Hello there C;\nIn order for me to be able to set your correct role I'm going to "
            "need a Guild Wars 2 API key with at least "
            "'account' and 'guild' access granted. "
            "Do you want to register via: "
            "```"
            "1: API\n"
            "2: I dont know how to provide API key\n"
            "3: Not at all you dumb robot, you have no control over me!"
            "```",
        "provide_api":
            "Please provide your Guild Wars 2 API key with at least 'guild' and 'account' "
            "accessibility.",
        "api_help_1":
            "You are able to create a Guild Wars 2 API key if you visit your Guild Wars 2 "
            "account page over at https://account.arena.net/applications",
        "api_help_2":
            "To create a new API key simply hit 'New Key' https://tinyurl.com/NewGw2Api",
        "api_help_3":
            "Give it a cool name specific to this application and make sure the 'account' "
            "and 'guild' checkboxes are marked then simply hit 'Create API Key' "
            "https://tinyurl.com/MakeGw2Api\n\n",
        "api_help_4":
            "Do you want to continue the registration? C:"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "offended":
            "Well fuck you then, I dont need you either :C",
        "success":
            "You have successfully registred yourself. Your discord role will now automatically "
            "update to your ingame guild rank.",
        "server_not_installed":
            "The server you are trying to link to is not installed. Contact your guild master "
            "for more information. Your information was saved, when the bot is properly installed "
            "on this discord server you can just rerun /register and it will be done immediately.",
        "not_member":
            "You are not a member of this guild. I will not link your discord accout to this "
            "guilds discord server.",
        "registered":
            "You are already registred and linked to this discord server."
    },
    "uninstall": {
        "are_you_sure":
            "Are you sure you want to uninstall me from your discord server?"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "success":
            "I have successfully removed all the information about the server and the members "
            "affiliation with this server. Everyone is still registered to me and will have to "
            "individually use the ´/unregister´ command if they want me to forget their "
            "information, only then will they be fully unregistered. If you choose not to "
            "unregister, you will not have to provide an API key again when linking me to any "
            "other server also using me.",
        "regret":
            "I knew you would change your mind C:",
        "not_installed":
            "I am not installed on this server :C"
    },
    "unregister": {
        "are_you_sure":
            "Are you sure you want to unregister and unlink yourself from all servers?"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "success":
            "You have been successfully removed from my memory. Who am I talking to?",
        "regret":
            "I knew you would change your mind C:",
        "not_registered":
            "You are not registered here, who are you?"
    },
    "unlink": {
        "are_you_sure":
            "Are you sure you want to unlink youself from this server?"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "success":
            "You have been successfully unlinked from this server.",
        "regret":
            "I knew you would change your mind C:",
        "not_linked":
            "You were not linked to this server to begin with."
    },
    "timeout":
        "The session timed out, rerun the command to try again",
    "reply_error": {
        "1":
            "Yes I know its silly but I will not automate this process so you know "
            "what will happen when at every step, if you want to continue just reply 1",
        "2":
            "You need to reply with number 1 or 2 to proceed.",
        "3":
            "You need to reply with number 1, 2 or 3 to proceed.",
        "4":
            "You need to reply with number 1, 2, 3 or 4 to proceed.",
        "5":
            "You need to reply with number 1, 2, 3, 4 or 5 to proceed.",
        "api":
            "The API key you gave me does not seem to be Guild Wars 2 API key "
            "if you believe this is wrong send an email to eliaseriksson95@gmail.com "
            "and tell me about this error =)",
    },
    "help": {
        "commands": "availeble commands: `/register`, `/help`, `/install`, `/uninstall`, "
        "`/unlink`, `/unregister`"
    },
    "refresh": {
        "success":
            "Server roles was successfully refreshed",
        "missing_server":
            "This discord server is not connected to a guild wars 2 guild yet. Go yell at your "
            "guild master to either use me or boot me out!"
    }
})


if __name__ == '__main__':
    print(messages.install.api_help)
