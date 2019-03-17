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
            "Give it a cool name specific to this application (if you dont know what just name it "
            "`guild manager`) and make sure the 'account' and 'guild' checkboxes are marked then "
            "simply hit 'Create API Key' https://tinyurl.com/MakeGw2Api\n\n",
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
            "install another guild.",
        "try_again":
            "Do you want to rerun the installation?",
        "linked":
            "Im not sure how but you just installed this server and you are already linked. "
            "This should not be possible, how did you do this?"
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
            "Give it a cool name specific to this application (if you dont know what just name it "
            "`guild manager`)and make sure the 'account' and 'guild' checkboxes are marked then "
            "simply hit 'Create API Key' https://tinyurl.com/MakeGw2Api\n\n",
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
            "You are already registred and linked to this discord server. If your role is "
            "incorrect please use the command `/gm register`",
        "authentication_error":
            "The api key you gav me resulted in an authentication error, make sure the api key "
            "is correctly typed to me and that it does have the 'account' and 'guild' "
            "permissions.",
        "unexpected_api_error":
            "There seems to be an issue with connecting correctly to guild wars 2 api, "
            "try again now or later and if th issue prsists please contact my developer: "
            "`mail@eliaseriksson.eu`",
        "goodbye":
            "Alrite good bye then C:"
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
        "number":
            "You need to reply with a number ammong the options to proceed."
    },
    "errors": {
        "refresh_error_owner":
            "A user on your server tried to refresh the ranks and I was forbiden to change the "
            "roles on the people in the server. This is probably beccause I am to low on the "
            "role list in the server settings. To fix this simply move me higher up on the list. "
            "If you run `/gm refresh` and this error doesnt show up I am in a good spot.",
        "refresh_user_error":
            "When I tried to update the roles on evryonee including you an error occured. "
            "Your discord server owner have been notefied about the issue and a solution.",
        "invalid_api":
            "The api you gave me is lacking permissions. Make sure you tick both the `guild` "
            "and `account` checkboxes when you create a new api. I will automaticly rerun your "
            "last command and if you need help with generating your api key select that option.",
        "unsuccessfull_request":
            "Something went wrong when I tried to connect to arenanets `api.guildwars2.com` "
            "my developer havnt told me what to do really when this happends. All I can recomend "
            "is try again, either now or later =3",
        "permission_error":
            "You are not an administrator of this discord server. To be able to successfully "
            "install this bot to a server you need to have administrator previleges.",
        "wrong_chat_error":
            "This command requires to be executed in the related server, otherwise I dont know "
            "where I need to do my work =<"
    },
    "help": {
        "commands": "availeble commands: `/gm register`, `/gm help`, `/gm install`, "
                    "`/gm uninstall`, `/gm unlink`, `/gm unregister`, `/gm merge`"
    },
    "refresh": {
        "success":
            "Server roles was successfully refreshed",
        "missing_server":
            "This discord server is not connected to a guild wars 2 guild yet. Go yell at your "
            "guild master to either use me or boot me out!",
        "ensuring_roles":
            "Making sure that the guild ranks exists as discord roles..."
    },
    "merge": {
        "instructions":
            "This command is used to merge ranks who have been renamed but are still "
            "represented as a discord role. It will as a minimum remove an old role from "
            "affected members and make sure the members gets the new role. Durring this procedure "
            "you will have options to copy the permissions and/or delete the old role.\n"
            "Is this what you wish to do?"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "goodbye":
            "Alrite good bye C:",
        "uninstalled_server":
            "This server seems to be uninstalled =|",
        "rank_question":
            "Which one of these ranks is it that have been renamed or in some way needs to be "
            "merged?\n```"
            "[placeholder]"
            "```",
        "role_question":
            "Which one of these roles do you wish to merge the old rank into?"
            "```"
            "[placeholder]"
            "```",
        "delete_old":
            "Do you want me to delete the old role?"
            "```"
            "1: Yes\n"
            "2: No"
            "```",
        "not_a_role":
            "This rank is not a role on this server.",
        "move_perms":
            "Do you want me to move the permissions from the old role to the new role?\n"
            "OBS! This will overwrite all permissions in the new role."
            "```"
            "1: Yes\n"
            "2: No"
            "```"
    }
})


if __name__ == '__main__':
    print(messages.install.api_help)
