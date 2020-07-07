import json
import os
from datetime import *
from termcolor import colored
import discord


def clear(): return os.system("cls")


def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())


def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=1))


def makeEmbed(title="TITLE", description="DESCRIPTION", color=0x833103):
	return discord.Embed(title=title, description=description, color=color)


def getTime():
	return datetime.now()


def log(text="PLACEHOLDER", cog="Main", color="green", ctx=None, event=False):
	if ctx:
		if event:
			print("[%s] [%s] [%s] %s [%s] %s %s" % (getTime(), colored("Overseer", "red"), colored(cog, color), ("." * (20 - len(cog))), ("Direct Message" if not ctx.guild else ctx.guild.name), ("." * (20 - len("Direct Message" if not ctx.guild else ctx.guild.name))), text))
		else:
			print("[%s] [%s] [%s] %s [%s] %s [%s] %s %s" % (getTime(), colored("Overseer", "red"), colored(cog, color), ("." * (20 - len(cog))), ("Direct Message" if not ctx.guild else ctx.guild.name), ("." * (20 - len("Direct Message" if not ctx.guild else ctx.guild.name))), ctx.author.name, ("." * (20 - len(ctx.author.name))), text))
	else:
		print("[%s] [%s] [%s] %s %s" % (getTime(), colored("Overseer", "red"), colored(cog, color), ("." * (20 - len(cog))), text))