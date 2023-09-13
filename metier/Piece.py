from Item import *

class Piece(object):
	"""docstring pour un Piece
	Un piece est lie a un channel et permet de creer d'autre piece et le channel avec
	"""
	def __init__(self, channel,description : str, isMonster : bool = False):
		self.channel = channel #channel discord
		self.description = description # description du lieu 
		self.nextRooms = [] #reference des pieces lié.
		self.isMonster = isMonster # si le lieu a des monstres ou pas
		self.objects = []

	#gere ici si un joueur peut aller a une piece ou pas, gere le channel 
	async def autorize(self,user):
		await self.channel.set_permissions(user,read_messages=True,read_message_history = True,send_messages=True)

		for nextRoom in self.nextRooms:
			await nextRoom.channel.set_permissions(user,read_messages=True, read_message_history = False,send_messages=False)

	#gere ici si un joeur ne peut pas aller a une piece ou pas, gere le channel
	async def inautorize(self,user):
		await self.channel.set_permissions(user,overwrite=None)

	def link(self,piece):
		self.nextRooms.append(piece)

	def links(self,listPieces):
		for piece in listPieces:
			self.link(piece)

	#envoie un message via le channel
	async def sendMessage(self,message : str):
		await self.channel.send(message)
