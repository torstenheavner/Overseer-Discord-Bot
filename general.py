from importlib import *
import discord
from discord.ext import commands, tasks
import ease_of_use as eou
import os
import requests


class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def cog_unload(self):
		eou.log(text="Offline", cog="General", color="magenta")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot:
    #         return
	#
    #     for image in os.listdir("./images"):
    #         if message.content == image.split(".")[0]:
    #             try:
    #                 await message.delete()
    #             except:
    #                 pass
    #             await message.channel.send(message.author.name, file=discord.File("images/%s" % image))

	@commands.command(brief="Create a new DM")
	async def create(self, ctx, channelName, createVoice=False, *, people):
		people = people.split(" ") # creates array of DM member usernames
		for i in range(len(people)):
			username = people[i] # stores usernames for error reporting
			people[i] = discord.utils.get(self.bot.get_guild(729856235813470221).members, name=people[i]) # convert usernames to user IDs
			if not people[i]:
				return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="%s isn't in the server!" % username))
		server = self.bot.get_guild(729856235813470221)
		tc = await server.create_text_channel(channelName) # create the requested channel
		await tc.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
		if createVoice:
			vc = await server.create_voice_channel(channelName) # create voice channel with same name if asked to
			await vc.set_permissions(ctx.guild.default_role, view_channel=False, connect=False)
		for person in people:
			await tc.set_permissions(person, read_messages=True, send_messages=True)
			if createVoice:
				await vc.set_permissions(person, view_channel=True, connect=False)
		# change permissions so @everyone cant access, but the individuals can (for both the VC and TC)
		await ctx.send(embed=eou.makeEmbed(title="Success!", description="Channel%s successfully created." % ("s" if createVoice else ""))) # send message confirmation
		eou.log(text="New DM created", cog="General", color="magenta", ctx=ctx)

	@commands.command(brief="Leave a specific channel") # o.leave
	async def leave(self, ctx, channelName):
		member = ctx.author
		tc = discord.utils.get(self.bot.get_guild(729856235813470221).text_channels, name=channelName)
		vc = discord.utils.get(self.bot.get_guild(729856235813470221).voice_channels, name=channelName)
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))
		await tc.set_permissions(member, overwrite=None) # remove all text channel perms from user
		if vc:
			await vc.set_permissions(member, overwrite=None)
		await ctx.send(embed=eou.makeEmbed(title="Success!", description="%s has left %s." % (member.name, channelName)))
		eou.log(text="Left %s" % (channelName), cog="General", color="magenta", ctx=ctx) # log the change

	# o.delete?
	# o.add?
	# o.kick?

	@commands.command(brief="Rename a DM")
	async def rename(self, ctx, channelName, newChannelName):
		tc = discord.utils.get(self.bot.get_guild(729856235813470221).text_channels, name=channelName)
		vc = discord.utils.get(self.bot.get_guild(729856235813470221).voice_channels, name=channelName)
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))
		await tc.edit(name=newChannelName)
		if vc:
			await vc.edit(name=newChannelName)
		await ctx.send(embed=eou.makeEmbed(title="Success!", description="%s sucessfully renamed to %s" % (channelName, newChannelName)))
		eou.log(text="DM renamed", cog="General", color="magenta", ctx=ctx)

def setup(bot):
	eou.log(text="Online", cog="General", color="magenta")
	bot.add_cog(General(bot))
	reload(eou)
