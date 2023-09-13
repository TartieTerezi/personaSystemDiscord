from Piece import *
import discord

class Lieu(object):
	"""docstring pour un Lieu
	Un lieu contient les pieces et la category correspondante
	"""
	def __init__(self, category):
		self.category = category
		self.pieces = []

	async def newPiece(self,name,description : str = "",isMonster : bool = False):
		channel = await self.category.create_text_channel(name)

		spectacteur = discord.utils.get(channel.guild.roles, name="Spectateur")

		await channel.set_permissions(channel.guild.roles[0],read_messages=False,send_messages=False)
		await channel.set_permissions(spectacteur,read_messages=True,send_messages=False)

		newPiece = Piece(channel,description, isMonster)

		if(newPiece.description != ""):
			await newPiece.sendMessage(description)

		self.pieces.append(newPiece)