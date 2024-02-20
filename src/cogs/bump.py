import discord
from discord.ext import commands
import asyncio
import time
from functions import fetchData


class bump(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    bump = discord.SlashCommandGroup("bump-config")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.id == 302050872383242240:
            return None
        GuildID = message.guild.id
        channel = message.channel
        rawData = fetchData(path=f"/{GuildID}/bumpConfig", cache="bumpCache")
        try:
            isEnabled = rawData["isEnabled"]
        except:
            return None

        if not isEnabled:
            return None

        for embed in message.embeds:
            if not "Bump done!" in embed.description:
                return None
            isEmbed = rawData["isEmbed"]
            thankTitle = rawData["thankTitle"]
            thankDesc = str(rawData["thankDesc"])
            remindDesc = rawData["remindDesc"]
            remindTitle = rawData["remindTitle"]
            pingRole = rawData["pingRole"]
            roleID = rawData["roleID"]
            embed = ""
            content = ""

            if "{role}" in thankDesc:
                thankDesc = thankDesc.replace("{role}", f"<@&{roleID}>")
            if "{next-bump-count}" in thankDesc:
                current_epoch_time = int(str(int(time.time()))[:10])
                epoch_time_plus_two_hours = current_epoch_time + 2 * 3600
                thankDesc = thankDesc.replace(
                    "{next-bump-count}", f"<t:{str(epoch_time_plus_two_hours)}:R>"
                )
            if isEmbed:
                embed = discord.Embed(title=thankTitle, description=thankDesc)
            else:
                if thankTitle:
                    content = thankTitle + "\n" + thankDesc
                else:
                    content = thankDesc
            await channel.send(content=content, embed=embed)
            content = ""
            await asyncio.sleep(7200)  # waits 2 hours
            if pingRole:
                content = f"<@&{roleID}>"
            if isEmbed:
                embed = discord.Embed(title=remindTitle, description=remindDesc)
            else:
                if remindTitle:
                    content = content + "\n" + remindTitle + "\n" + remindDesc
                else:
                    content = content + "\n" + remindDesc
            await channel.send(content=content, embed=embed)


#    @bump.command(name="remind-title")
#    async def remindTitle(self, ctx, title: discord.Option(str)):
#        await ctx.defer()
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("SELECT * from configs WHERE guild_id = ?", (ctx.guild.id,))
#        rows = cur.fetchall()
#        column_names = [description[0] for description in cur.description]
#        for row in rows:
#            raw_data = dict(zip(column_names, row))
#        staff_id = raw_data[staff_role_id]
#    for role in ctx.author.roles:
#        print(role)
#        if role.id == staff_id:
#            with sqlite3.connect(database) as conn:
#                cur = conn.cursor()
#                cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remindTitle) VALUES (?, ?)", (ctx.guild.id, title,))
#            await ctx.respond(f'Set remind title to "{title}"')
#        else:
#            pass
# @bump.command(name="remind-description")
# async def remindDesc(self, ctx, description: discord.Option(str)):
#    await ctx.defer()
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remindDesc) VALUES (?, ?)", (ctx.guild.id, description,))
#    await ctx.respond(f'Set remind description to "{description}"')
#
# @bump.command(name="thank-title")
# async def thankTitle(self, ctx, title: discord.Option(str)):
#    await ctx.defer()
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, thankTitle) VALUES (?, ?)", (ctx.guild.id, title,))
#    await ctx.respond(f'Set thank title to "{title}"')
#
# @bump.command(name="thank-description")
# async def thankDesc(self, ctx, description: discord.Option(str)):
#    await ctx.defer()
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, thankDesc) VALUES (?, ?)", (ctx.guild.id, description,))
#    await ctx.respond(f'Set remind description to "{description}"')
#
# @bump.command(name="embed")
# async def embed(self, ctx, embeds: discord.Option(str, choices=["enabled", "disabled"])):
#    await ctx.defer()
#    if embeds == "enabled":
#        isEmbed=1
#    else:
#        isEmbed=0
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, isEmbed) VALUES (?, ?)", (ctx.guild.id, isEmbed,))
#    await ctx.respond(f'Embeds are now {embeds}')
#
#
# @bump.command(name="role")
# async def role(self, ctx, description: discord.Option(str)):
#    await ctx.defer()
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remindDesc) VALUES (?, ?)", (ctx.guild.id, description,))
#    await ctx.respond(f'Set remind description to "{description}"')
# Disabled, i'll get it working tmr -Nugget


# todo - might not do this due to db cost
# @commands.Cog.listener()
# async def on_ready(self): # on start
# check last bump time, if under 2 hrs start timer with remaining time til 2 hrs from bump time
# otherwise just send the reminder
# todo
def setup(bot):
    bot.add_cog(bump(bot))
