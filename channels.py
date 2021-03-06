from importlib import *
import discord
from discord.ext import commands, tasks
import ease_of_use as eou
import os
import requests



class Channels(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	def cog_unload(self):
		eou.log(text="Offline", cog="Channels", color="magenta")



	@commands.command(brief="Create a DM")
	async def create(self, ctx, channelName, createVoice=False, *, people):
		# o.create [channelName] [createVoice=False] [people]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)
		people = people.split(" ")

		# Change the array of names to an array of discord.Member objects
		for i in range(len(people)):
			username = people[i]
			people[i] = discord.utils.get(server.members, name=people[i])
			if not people[i]:
				return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description=f"I couldn't find anyone with that name."))

		# Check if a channel with the given name alredy exists
		if discord.utils.get(server.text_channels, name=channelName):
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description=f"A DM with the name \"{channelName}\" already exists."))

		# Create a new channel and prevent @everyone from seeing it
		tc = await server.create_text_channel(channelName)
		await tc.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)

		# If necesarry, create matching voice channel and prevent #everyone from seeing it
		if createVoice:
			vc = await server.create_voice_channel(channelName)
			await vc.set_permissions(ctx.guild.default_role, view_channel=False, connect=False)

		# Allow everyone in the [people] array to see the channel(s)
		for person in people:
			await tc.set_permissions(person, read_messages=True, send_messages=True)
			if createVoice:
				await vc.set_permissions(person, view_channel=True, connect=False)

		# Send ouput and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description="Channel%s successfully created." % ("s" if createVoice else "")))
		eou.log(text="New DM created", cog="Channels", color="magenta", ctx=ctx)



	@commands.command(brief="Leave a DM")
	async def leave(self, ctx, channelName):
		# o.leave [channelName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Attempt to get the text and voice channels by the given name
		tc = discord.utils.get(server.text_channels, name=channelName)
		vc = discord.utils.get(server.voice_channels, name=channelName)

		# Throw an error if you cant find the text channel
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))

		# Get rid of the authors permissions in the necesarry channels
		await tc.set_permissions(ctx.author, overwrite=None)
		if vc:
			await vc.set_permissions(ctx.author, overwrite=None)

		# Send output and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description=f"{ctx.author.name} has left {channelName}."))
		eou.log(text=f"Left {channelName}", cog="Channels", color="magenta", ctx=ctx)



	@commands.command(brief="Add someone to a DM")
	async def add(self, ctx, person, channelName):
		# o.add [person] [channelName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Attempt to get the user and channels by the given names
		user = discord.utils.get(server.members, name=person)
		tc = discord.utils.get(server.text_channels, name=channelName)
		vc = discord.utils.get(server.voice_channels, name=channelName)

		# Throw an error if you cant find the user or text channel
		if not user:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find anyone with that name."))
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))

		# Give the user permissions in the necesarry channels
		await tc.set_permissions(user, read_messages=True, send_messages=True)
		if vc:
			await vc.set_permissions(user, read_messages=True, send_messages=True)

		# Send output and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description=f"{user.name} has been added to {channelName}."))
		eou.log(text=f"Added {user.name} to {channelName}", cog="Channels", color="magenta", ctx=ctx)



	@commands.command(brief="Kick someone from a DM")
	async def kick(self, ctx, person, channelName):
		# o.kick [person] [channelName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Attempt to get the user and channels by the given names
		user = discord.utils.get(server.members, name=person)
		tc = discord.utils.get(server.text_channels, name=channelName)
		vc = discord.utils.get(server.voice_channels, name=channelName)

		# Throw an error if you cant find the user or text channel
		if not user:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find anyone with that name."))
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))

		# Get rid of the users permissions in the necesarry channels
		await tc.set_permissions(user, overwrite=None)
		if vc:
			await vc.set_permissions(user, overwrite=None)

		# Send output and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description=f"{user.name} has been kicked from {channelName}."))
		eou.log(text=f"Kicked {user.name} from {channelName}", cog="Channels", color="magenta", ctx=ctx)



	@commands.command(brief="Delete a DM")
	async def delete(self, ctx, channelName):
		# o.delete [channelName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Attempt to get the text and voice channels by the given name
		tc = discord.utils.get(server.text_channels, name=channelName)
		vc = discord.utils.get(server.voice_channels, name=channelName)

		# Throw an error if you cant find the text channel
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))

		# Delete the necesarry channels
		await tc.delete()
		if vc:
			await vc.delete()

		# Send output and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description=f"{channelName} successfully deleted."))
		eou.log(text="DM deleted", cog="Channels", color="magenta", ctx=ctx)



	@commands.command(brief="Rename a DM")
	async def rename(self, ctx, channelName, newChannelName):
		# o.rename [channelName] [newChannelName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Attempt to get the text and voice channels by the given name
		tc = discord.utils.get(server.text_channels, name=channelName)
		vc = discord.utils.get(server.voice_channels, name=channelName)

		# Throw an error if you cant find the text channel
		if not tc:
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="I couldn't find that channel."))

		# Change the names of the necesarry channels
		await tc.edit(name=newChannelName)
		if vc:
			await vc.edit(name=newChannelName)

		# Send output and log to console
		await ctx.send(embed=eou.makeEmbed(title="Success!", description=f"{channelName} sucessfully renamed to {newChannelName}." ))
		eou.log(text="DM renamed", cog="Channels", color="magenta", ctx=ctx)



	# o.open [channelName]
	# o.close [channelName]
	# o.join [channelName]
	# o.listopenchannels



def setup(bot):
	eou.log(text="Online", cog="Channels", color="magenta")
	bot.add_cog(Channels(bot))
	reload(eou)
