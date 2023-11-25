

class SocialStats(object):
	"""Docstring for Social Stats"""
	def __init__(self,_connaissance : int = 1,_xpConnaissance : int = 0,_charme : int = 1,_xpCharme : int = 0,
			  _gentilesse : int = 1, _xpGentilesse : int = 0, _competence : int = 1, _xpCompetence : int = 0,
			  _maitrise : int = 1, _xpMaitrise : int = 0) -> None:
		#stats sociale 
		self.connaissance : int = _connaissance
		self.xpConnaissance : int = _xpConnaissance
		self.charme : int = _charme
		self.xpCharme : int = _xpCharme
		self.gentilesse : int = _gentilesse
		self.xpGentilesse : int = _xpGentilesse
		self.competence : int = _competence
		self.xpCompetence : int = _xpCompetence
		self.maitrise : int = _maitrise
		self.xpMaitrise : int = _xpMaitrise