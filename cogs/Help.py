import discord
from discord.ext import commands


# Creates an embed base for the help commands. This way if I every want to change the look of all my help commands
# I can just change the look of all the help commands from this one function.
def create_embed(name, info, pars, des, examples):
    embed = discord.Embed(
        colour=discord.colour.Color.dark_teal()
    )

    embed.add_field(name='Command Name:', value='```md\n' + name + '```', inline=False)
    embed.add_field(name='Description:', value='```fix\n' + info + '```',
                    inline=False)
    format_string = ""
    description_string = ""
    for par, de in zip(pars, des):
        format_string += " <" + par + ">"
        description_string += "<" + par + "> " + de + "\n\n"

    embed.add_field(name='Format:', value='```md\n>>' + name + format_string + '```', inline=False)
    embed.add_field(name='Parameters:', value='```md\n' + description_string + '```', inline=False)

    examples_string = ""
    index = 0
    for example in examples:
        index += 1
        examples_string += "{}. >>{}\n".format(index, example)
    embed.add_field(name='Examples:', value='```md\n' + examples_string + '```', inline=False)

    embed.set_footer(text="Bot created by FeistyJalapeno#9045. If you have questions, suggestions, "
                          "found a bug, etc. feel free to DM me.")

    return embed


class HelpCog(commands.Cog, name="Help Commands"):
    """Cog that creates help commands for the bot."""

    def __init__(self, bot):
        self.bot = bot

    # Custom help commands
    @commands.group(pass_context=True)
    async def help(self, ctx):

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description="Check your dms for a full list of commands. For more help on a specific command "
                            "call `>>help <command>`",
                colour=discord.colour.Color.dark_teal()
            )
            await ctx.send(embed=embed)

            author = ctx.message.author
            embed = discord.Embed(
                colour=discord.colour.Color.dark_teal()
            )

            my_message = "Note to get the best experience when using PaladinsAssistant it is recommended that you use "\
                         "discord on desktop since over half of the commands use colors and colors do not show up on " \
                         "Mobile. Below are listed all the different types of commands this bot offers." \
                         "\n\nFor example, if someone " \
                         "wants to know how to use the `stats` command, they would type `>>help stats`" \
                         "\n\nAlso if you want more information on how to use the bot to its full extent, feel free to"\
                         " join the support server here: https://discord.gg/njT6zDE"

            embed.set_author(name='PaladinsAssistant Commands: ')
            embed.set_thumbnail(url="http://web.eecs.utk.edu/~ehicks8/Androxus.png")  # Upload to website
            embed.set_footer(icon_url="https://cdn.discordapp.com/embed/avatars/0.png",
                             text="Bot created by FeistyJalapeno#9045.")
            # If you have questions, suggestions, found a bug, etc. feel free to DM me.")
            embed.add_field(name='help', value='Returns this message.', inline=False)
            embed.add_field(name='console_name', value='Returns info for how console players should type their '
                                                       'name for the bot to recognize.', inline=False)
            embed.add_field(name='store', value='Stores a players IGN in Paladins for the bot to use.', inline=False)
            embed.add_field(name='last', value='Returns stats for a player\'s match.', inline=False)
            embed.add_field(name='match', value='Returns detailed stats for a player\'s match.', inline=False)
            embed.add_field(name='stats', value='Returns simple overall stats for a player.', inline=False)
            embed.add_field(name='random', value='Allows user to generate a random siege map, champion, or team.',
                            inline=False)
            embed.add_field(name='current', value='Returns stats for a player\'s current match.', inline=False)
            embed.add_field(name='history', value='Returns simple stats for a player\'s last amount of matches.',
                            inline=False)
            embed.add_field(name='deck', value='Prints out all the decks a player has for a champion. If an a number is'
                                               'given after the character name then an image will be created of that '
                                               'deck.', inline=False)
            embed.add_field(name='top', value='Prints a sorted list of stats of a player\'s champions.',
                            inline=False)
            embed.add_field(name='console', value='Command console players can use to look up their player_id.',
                            inline=False)
            embed.add_field(name='usage', value='Returns how many times you have used commands for this bot.',
                            inline=False)
            # embed.add_field(name='track', value='Starts recording matches played by a player.',
            #                inline=False)
            embed.add_field(name='prefix', value='Lets the server owner change the prefix of the bot.',
                            inline=False)
            embed.add_field(name='language', value='Lets the server owner change the language the bot uses.',
                            inline=False)

            # Try to first dm the user the help commands, then try to post it the channel where it was called
            try:
                await author.send(my_message, embed=embed)
            except discord.Forbidden:
                print("Could not dm the help command to the person who called the command.")
                try:
                    await ctx.send(my_message, embed=embed)
                except discord.Forbidden:
                    print("We have failed to message the help commands to the person.")

    @help.command()
    async def store(self, ctx):
        command_name = "store"
        command_description = "Stores a players IGN in Paladins for the bot to use. Once this command is done a " \
                              "player can type the word [me] instead of their name."
        parameters = ["player_name"]
        descriptions = ["Player's Paladins IGN"]
        examples = ["{} {}".format(command_name, "Your Paladins IGN (user name)")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def last(self, ctx):
        command_name = "last"
        command_description = "Returns stats for a player\'s last match."
        parameters = ["player_name", "match_id"]
        descriptions = ["Player's Paladins IGN", "The match id of the game. This can be found in game in Paladin's "
                                                 "History tab or in this bots >>history command.\n[Optional parameter]:"
                                                 " if not provide, defaults to most recent match"]
        examples = ["{} {}".format(command_name, "z1unknown"), "{} {}".format(command_name, "z1unknown 012345678")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def match(self, ctx):
        command_name = "match"
        command_description = "Returns detailed stats for a player\'s match."
        parameters = ["player_name", "match_id", "colored"]
        descriptions = ["Player's Paladins IGN", "The match id of the game. This can be found in game in Paladin's "
                                                 "History tab or in this bots >>history command.\n[Optional parameter]:"
                                                 " if not provide, defaults to most recent match",
                        "If someone wants the text to be colored in the image created by the command then they need to "
                        "type [-c].\n[Optional parameter]: if not provide, defaults to black text"]
        examples = ["{} {}".format(command_name, "z1unknown"), "{} {}".format(command_name, "z1unknown 012345678"),
                    "{} {}".format(command_name, "z1unknown -c"),
                    "{} {}".format(command_name, "z1unknown 012345678 -c")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def history(self, ctx):
        command_name = "history"
        command_description = "Returns simple stats for a player\'s last amount of matches."
        parameters = ["player_name", "amount", "champ_name"]
        descriptions = ["Player's Paladins IGN", "Amount of matches you want to see (10-50 matches)\n"
                                                 "[Optional parameter]: if not provide, defaults to 10",
                        "Champion's name that you want to look for in History\n"
                        "[Optional parameter]: if not provide, defaults to all champions"]
        examples = ["{} {}".format(command_name, "z1unknown"), "{} {}".format(command_name, "z1unknown 20"),
                    "{} {}".format(command_name, "z1unknown 50"), "{} {}".format(command_name, "z1unknown 50 Androxus"),
                    "{} {}".format(command_name, "z1unknown Evie")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def current(self, ctx):
        command_name = "current"
        command_description = "Get stats for a player's current match."
        parameters = ["player_name", "option"]
        descriptions = ["Player's Paladins IGN", "Type -a if you want an advanced look for all the players. "
                                                 "If -a is provided then the stats of the champion that each person "
                                                 "plays will be returned as well.\n[Optional parameter]: if not "
                                                 "provide, defaults to just returning every player's overall stats"]
        # examples = ["{} {}".format(command_name, "z1unknown")]
        examples = ["{} {}".format(command_name, "z1unknown"), "{} {}".format(command_name, "z1unknown -a")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def top(self, ctx):
        command_name = "top/bottom"
        command_description = "Returns a list of a player\'s champions stats sorted." \
                              "\n>>top - highest to lowest\n>>bottom - lowest to highest"
        parameters = ["player_name", "option", "class?"]
        option_description = "can be one of the following: \n\n" \
                             "1. <Level>: Level of a champion.\n" \
                             "2. <KDA>: KDA of a champion.\n" \
                             "3. <WL>: Win Rate of with champion.\n" \
                             "4. <Matches>: total matches played with a champion.\n" \
                             "5. <Time>: play time of a champion.\n"
        all_option = "If the word \"class\" is provide then the command sorts the stats for all a player's " \
                     "champions by class type\n" \
                     "[Optional parameter]: if not provide, the command defaults to returning the all stats of a " \
                     "players sorted ignoring class type."
        descriptions = ["Player's Paladins IGN", option_description, all_option]
        examples = ["{} {}".format("top", "Level"), "{} {}".format("top", "KDA class"),
                    "{} {}".format("bottom", "Time")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def console(self, ctx):
        command_name = "console"
        command_description = "Command console players can use to look up their player_id."
        parameters = ["player_name", "console_type"]
        option_description = "can be one of the following: \n\n" \
                             "1. <Xbox>\n" \
                             "2. <PS4>\n" \
                             "3. <Switch>\n"
        descriptions = ["Player's Paladins IGN", option_description]
        examples = ["{} {}".format(command_name, "iAssassin03 PS4"),
                    "{} {}".format(command_name, "\"Space in User Name\" Switch")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def stats(self, ctx):
        command_name = "stats"
        command_description = "Returns simple overall stats for a player."
        parameters = ["player_name", "champ_name"]
        long_string = "<champion_name>: will return the player's stats on the name of the champion typed.\n" \
                      "[Optional parameter]: if not provide, the command defaults to returning the player's overall " \
                      "stats"
        descriptions = ["Player's Paladins IGN", long_string]
        examples = ["{} {}".format(command_name, "z1unknown"), "{} {}".format(command_name, "z1unknown Viktor")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def random(self, ctx):
        command_name = "random"
        command_description = "Allows user to generate a random siege map, champion, or team."
        parameters = ["option"]
        long_string = "can be one of the following: \n\n" \
                      "1. <champ>: will return any champion in the game.\n" \
                      "2. <damage>: will return a damage champion.\n" \
                      "3. <healer>: will return a support champion.\n" \
                      "4. <flank>: will return a flank champion.\n" \
                      "5. <tank>: will return a tank champion.\n" \
                      "6. <map>: will return a siege map.\n" \
                      "7. <team>: will return a team of champions.\n"
        descriptions = [long_string]
        examples = ["{} {}".format(command_name, "champ"), "{} {}".format(command_name, "flank"),
                    "{} {}".format(command_name, "team")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def deck(self, ctx):
        command_name = "deck"
        command_description = "Prints out all the decks a player has for a champion. If an a number is given after the"\
                              " character name then an image will be created of that deck."
        parameters = ["player_name", "champ_name", "deck_number"]
        descriptions = ["Player's Paladins IGN ", "Paladin's Champions Name", "Number of the deck you want to create "
                                                                              "an image out of.\n[Optional parameter]: "
                                                                              "if not provide, prints a list all the "
                                                                              "decks that the player has for that "
                                                                              "champion"
                        ]
        examples = ["{} {}".format(command_name, "z1unknown Androxus"),
                    "{} {}".format(command_name, "z1unknown Androxus 1")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def console_name(self, ctx):
        command_name = "console_name"
        command_description = "Returns info for how console players should type their name for the bot to recognize."
        parameters = ["None"]
        descriptions = ["Parameterless command"]
        examples = ["{} {}".format(command_name, "")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def usage(self, ctx):
        command_name = "usage"
        command_description = "Returns how many times you have used commands for this bot."
        parameters = ["None"]
        descriptions = ["Parameterless command"]
        examples = ["{} {}".format(command_name, "")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    """
    @help.command()
    async def track(self, ctx):
        command_name = "track"
        command_description = "Starts recording matches played by a player."
        parameters = ["me"]
        descriptions = ["Players must have stored their name in the bot using the store command first before "
                        "using this command."]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))
    """

    @help.command()
    async def prefix(self, ctx):
        command_name = "prefix"
        command_description = "Lets the server owner change the prefix of the bot."
        parameters = ["prefix"]
        descriptions = ["The prefix can be set to whatever you want."]
        examples = ["{} {}".format(command_name, "**")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))

    @help.command()
    async def language(self, ctx):
        command_name = "language"
        command_description = "Lets the server owner change the language the bot uses."
        parameters = ["language"]
        descriptions = ["This command is still being worked on... If you want to bot to use a certain language dm me "
                        "about it. I rely on people translating text not online translators."]
        examples = ["{} {}".format(command_name, "pl"), "{} {}".format(command_name, "pt"),
                    "{} {}".format(command_name, "reset")]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions, examples))


# Add this class to the cog list
def setup(bot):
    bot.add_cog(HelpCog(bot))
