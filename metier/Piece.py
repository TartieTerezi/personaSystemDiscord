from Item import *

class Piece(object):
	"""docstring pour un Piece
	Un piece est lie a un channel et permet de creer d'autre piece et le channel avec
	"""
	def __init__(self, channel,description : str, isMonster : bool = False):
		self.channel = channel #channel discord
		self.description = description # description du lieu 
		self.descriptionsNextRooms = []
		self.nextRooms = [] #reference des pieces lié.
		self.isMonster = isMonster # si le lieu a des monstres ou pas
		self.objects = []
		self.alreadyVisited = [] #liste les joueurs qui sont déjà passé par cette pièce

	#gere ici si un joueur peut aller a une piece ou pas, gere le channel 
	async def autorize(self,user):
		await self.channel.set_permissions(user,read_messages=True,read_message_history = True,send_messages=True)

		if(self.isAlreadyVisited(user) == False):
			self.alreadyVisited.append(user.id)

		for nextRoom in self.nextRooms:
			await nextRoom.channel.set_permissions(user,read_messages=False, read_message_history = False,send_messages=False)

	#gere ici si un joeur ne peut pas aller a une piece ou pas, gere le channel
	async def inautorize(self,user):
		await self.channel.set_permissions(user,overwrite=None)

	def link(self,piece,description = ""):
		self.nextRooms.append(piece)
		self.descriptionsNextRooms.append(description)

	def links(self,listPieces,descriptions = None):
		if(descriptions == None):
			for piece in listPieces:
				self.link(piece)
		else:
			for i in range(len(listPieces)):
				self.link(listPieces[i],descriptions[i])

	def isAlreadyVisited(self,user):
		for i in range(len(self.alreadyVisited)):
			if(user.id == self.alreadyVisited[i]):
				return True

		return False

	#envoie un message via le channel
	async def sendMessage(self,message : str):
		await self.channel.send(message)
