from importlib import *
import discord
from discord.ext import commands, tasks
import ease_of_use as eou
import os
import requests



class Categories(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	def cog_unload(self):
		eou.log(text="Offline", cog="Categories", color="blue")



	@commands.command(brief="Create a category")
	async def createcategory(self, ctx, categoryName):
		# o.createcategory [categoryName]

		# Initial setup
		await ctx.message.delete()
		server = self.bot.get_guild(729856235813470221)

		# Check if a category with the given name already exists
		if discord.utils.get(server.categories, name=categoryName):
			return await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="A category with that name already exists."))

		# Create a new category
		# Wait permissions make it so everyone can see the category just not the channels in it
		# Maybe dont mess with category stuff you nerd



	# o.renamecategory [categoryName] [newCategoryName]
	# o.deletecategory [categoryName]

	# o.movetocategory [channelName] [categoryName]
	# o.removefromcategory [channelName] [categoryName]@commands.command(brief="Create a DM")



def setup(bot):
	eou.log(text="Online", cog="Categories", color="blue")
	bot.add_cog(Categories(bot))
	reload(eou)
