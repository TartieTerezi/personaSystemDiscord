import discord

class ProgressBar(object):
	"""class progress bar Discord"""
	def __init__(self,ctx,number : int = 10, first_emote = "🟩", second_emote = "⬜"):
		self.number = number
		self.step = 0
		self.message = None
		self.first_emote = first_emote
		self.second_emote = second_emote
		self.ctx = ctx
	   
	async def start(self):
		self.message = await self.ctx.send((self.second_emote*(self.number)))

	async def add(self):
		if(self.message == None):
			await self.start()

		self.step += 1
		await self.message.edit(content = str((self.first_emote*self.step)+(self.second_emote*int((self.number-self.step)))))

		if(self.step >= self.number):
			return True

		return False
	
	def __del__(self):
		 del self
