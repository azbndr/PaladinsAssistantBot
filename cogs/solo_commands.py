from discord.ext import commands
import json
import my_utils as helper
from colorama import Fore
from psutil import Process
from os import getpid


def server_owner_only():
    async def predicate(ctx):
        # If in dm's
        if ctx.guild is None:
            return True
        if not ctx.guild.owner == ctx.author:
            raise NotServerOwner("Sorry you are not authorized to use this command. Only the server owner: " +
                                 str(ctx.guild.owner) + " can use this command")
        return True
    return commands.check(predicate)


class NotServerOwner(commands.CheckFailure):
    pass


def enabled_function(enabled=True, message="Command disabled."):
    async def predicate(ctx):
        # If in dm's
        if ctx.guild is None:
            return True
        #if not ctx.guild.owner == ctx.author:
        #    raise NotServerOwner("Sorry you are not authorized to use this command. Only the server owner: " +
        #                        str(ctx.guild.owner) + " can use this command")
        if not enabled:
            await ctx.send(message)
            raise NoNo
        return True
    return commands.check(predicate)


class NoNo(BaseException):
    pass


# Class of commands that are solo (a.k.a) are not used/related to other functions
class SoloCommandCog(commands.Cog, name="Solo Commands"):
    """SoloCommandsCog"""
    # Different supported languages
    languages = ["Polish", "Português"]
    abbreviations = ["pl", "pt"]
    file_name = 'languages/server_configs'
    lan = []
    dashes = "----------------------------------------"

    def __init__(self, bot):
        self.bot = bot
        self.load_lang()

    def load_lang(self):
        with open(self.file_name) as json_f:
            print(Fore.CYAN + "Loaded server languages...")
            self.lan = json.load(json_f)

    @enabled_function(False)
    @commands.command(name='decorators')
    async def decorators(self, ctx):
        await ctx.send("Sup my dude.")

    @commands.command(name='prefix')
    @commands.guild_only()
    @server_owner_only()
    async def set_server_prefix(self, ctx, prefix):
        async with ctx.channel.typing():
            with open(self.file_name) as json_f:
                server_ids = json.load(json_f)
                try:
                    server_ids[str(ctx.guild.id)]["prefix"] = prefix
                except KeyError:  # Server has no configs yet
                    server_ids[str(ctx.guild.id)] = {}
                    server_ids[str(ctx.guild.id)]["prefix"] = prefix
                    # server_ids[str(ctx.guild.id)]["lang"] = "en"
                with open(self.file_name, 'w') as json_d:
                    json.dump(server_ids, json_d)
                await ctx.send("This bot is now set to use the prefix: `" + prefix + "` in this server")

    @commands.command(name='language', aliases=["język"])
    @commands.guild_only()
    @server_owner_only()
    async def set_server_language(self, ctx, language: str):
        async with ctx.channel.typing():
            language = language.lower()

            if language in self.abbreviations:
                with open(self.file_name) as json_f:
                    server_ids = json.load(json_f)
                    try:
                        server_ids[str(ctx.guild.id)]["lang"] = language  # store the server id in the dictionary
                    except KeyError:  # Server has no configs yet
                        server_ids[str(ctx.guild.id)] = {}
                        # server_ids[str(ctx.guild.id)]["prefix"] = ">>"
                        server_ids[str(ctx.guild.id)]["lang"] = language
                    # need to update the file now
                    with open(self.file_name, 'w') as json_d:
                        json.dump(server_ids, json_d)
                    self.load_lang()  # Update the global/class list
                    helper.Lang.lan = server_ids  # Update the other class list
                await ctx.send("This bot is now set to use the language: `" + language + "` in this server")
            elif language == "reset":
                with open(self.file_name) as json_f:
                    server_ids = json.load(json_f)
                    server_ids[str(ctx.guild.id)].pop("lang", None)
                # need to update the file now
                with open(self.file_name, 'w') as json_d:
                    json.dump(server_ids, json_d)
                self.load_lang()  # Update the global/class list
                helper.Lang.lan = server_ids  # Update the other class list
                await ctx.send("Server language has been reset to English")
            else:
                lines = ""
                for abbr, lang, in zip(self.abbreviations, self.languages):
                    lines += "`" + abbr + ":` " + lang + "\n"
                await ctx.send("You entered an invalid language. The available languages are: \n" + lines +
                               "`reset:` Resets the bot to use English"
                               "\nNote that by default the language is English so there is no need to set it to that.")
            # print(ctx.channel.id, ctx.guild.id)
            # print("This server's id is:" + str(ctx.guild.id))
            # await ctx.send("This server's id is: " + str(ctx.guild.id))

    @commands.command(name='check')
    async def check_server_language(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.lan and "lang" in self.lan[guild_id]:
            await ctx.send("This server's language is: " + self.lan[guild_id]["lang"])
            return self.lan[guild_id]["lang"]
        else:
            await ctx.send("This server's language is English")
            return "English"

    # Print how many times a person has used each command
    @commands.command(name='usage', aliases=["użycie"])
    async def usage(self, ctx):
        user_commands = await helper.get_store_commands(ctx.author.id)
        len(user_commands)
        message = "Commands used by {}\n{}\n".format(ctx.author, self.dashes)

        # Data to plot
        labels = []
        data = []
        i = 1

        for command, usage in user_commands.items():
            message += "{}. {:9} {}\n".format(str(i), str(command), str(usage))
            labels.append(command)
            data.append(usage)
            i += 1

        await ctx.send('```md\n' + message + '```')

    @commands.is_owner()
    @commands.command(name='check_bot', aliases=["bot_check"])
    async def check_bot(self, ctx):
        with open("log_file.csv", 'r') as r_log_file:
            lines = r_log_file.read().splitlines()
            servers, n1, old_errors, num_cmd, old_api_calls, old_date = lines[-1].split(',')

        bot_memory = f'{round(Process(getpid()).memory_info().rss/1024/1024, 2)} MB'

        ss = "1. [Server count:]({})\n2. [Help Server Members:]({})\n3. [Fatal Errors:]({})\n4. " \
             "[Commands Used:]({})\n5. [API Calls Used:]({})\n6. [Date:]({})\n7. [Memory Usage:]({})" \
            .format(servers, n1.strip(), old_errors.strip(), num_cmd.strip(), old_api_calls.strip(), old_date.strip(),
                    bot_memory.strip())
        ss_f = '```md\n' + self.dashes + '\n' + ss + '```'
        await ctx.send(ss_f)


# Add this class to the cog list
def setup(bot):
    bot.add_cog(SoloCommandCog(bot))
