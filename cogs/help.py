import discord
from discord.ext import commands


# Creates an embed base for the help commands. This way if I every want to change the look of all my help commands
# I can just change the look of all the help commands from this one function.
def create_embed(name, info, pars, des):
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
    embed.set_footer(text="Bot created by FeistyJalapeno#9045. If you have questions, suggestions, "
                          "found a bug, etc. feel free to DM me.")

    return embed


class HelpCog(commands.Cog, name="Help Commands"):
    """SimpleCog"""

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
            # embed.add_field(name='about', value='Returns more information about the bot.', inline=False)
            embed.add_field(name='last', value='Returns stats for a player\'s last match.', inline=False)
            embed.add_field(name='stats', value='Returns simple overall stats for a player.', inline=False)
            embed.add_field(name='random', value='Randomly chooses a map, champion, or team to help with '
                                                 'custom matches.', inline=False)
            embed.add_field(name='current', value='Returns stats for a player\'s current match.', inline=False)
            embed.add_field(name='history', value='Returns simple stats for a player\'s last amount of matches.',
                            inline=False)
            embed.add_field(name='deck', value='Prints out all the decks a player has for a champion. If an a number is'
                                               'given after the character name then an image will be created of that '
                                               'deck.', inline=False)
            embed.add_field(name='usage', value='Returns how many times you have used commands for this bot in the form'
                                                'of a pie-chart.', inline=False)
            embed.add_field(name='prefix', value='Lets the server owner change the prefix of the bot.',
                            inline=False)
            embed.add_field(name='language', value='Lets the server owner change the language the bot uses.',
                            inline=False)

            # Try to first dm the user the help commands, then try to post it the channel where it was called
            try:
                await author.send(my_message, embed=embed)
            except None:
                print("Could not dm the help command to the person who called the command.")
                try:
                    await ctx.send(my_message, embed=embed)
                except None:
                    print("We have failed to message the help commands to the person.")

    @help.command()
    async def last(self, ctx):
        command_name = "last"
        command_description = "Returns stats for a player\'s last match."
        parameters = ["player_name"]
        descriptions = ["Player's Paladins IGN"]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def history(self, ctx):
        command_name = "history"
        command_description = "Returns simple stats for a player\'s last amount of matches."
        parameters = ["player_name", "amount", "champ_name"]
        descriptions = ["Player's Paladins IGN", "Amount of matches you want to see (2-50 matches)\n"
                                                 "[Optional parameter]: if not provide, defaults to 10",
                        "Champion's name that you want to look for in History\n"
                        "[Optional parameter]: if not provide, defaults to 10"]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def current(self, ctx):
        command_name = "current"
        command_description = "Get stats for a player's current match."
        parameters = ["player_name"]
        descriptions = ["Player's Paladins IGN"]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def stats(self, ctx):
        command_name = "stats"
        command_description = "Returns simple overall stats for a player."
        parameters = ["player_name", "option"]
        long_string = "can be one of the following: \n\n" \
                      "1. <me>: will return the player's overall stats. \n" \
                      "2. <champion_name>: will return the player's stats on the name of the champion entered."
        # "3. <elo>: will return the player's Guru elo.\n" \
        descriptions = ["Player's Paladins IGN", long_string]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

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
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def usage(self, ctx):
        command_name = "usage"
        command_description = "Returns how many times you have used commands for this bot in the form of a pie-chart."
        parameters = ["None"]
        descriptions = ["Parameterless command"]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def prefix(self, ctx):
        command_name = "prefix"
        command_description = "Lets the server owner change the prefix of the bot."
        parameters = ["prefix"]
        descriptions = ["The prefix can be set to whatever you want."]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))

    @help.command()
    async def language(self, ctx):
        command_name = "language"
        command_description = "Lets the server owner change the language the bot uses."
        parameters = ["language"]
        descriptions = ["This command is still being worked on..."]
        await ctx.send(embed=create_embed(command_name, command_description, parameters, descriptions))


# Add this class to the cog list
def setup(bot):
    bot.add_cog(HelpCog(bot))
