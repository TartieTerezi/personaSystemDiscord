from StatutEffect import StatutEffect
from metier.Item import Weapon

class Fighter(object):
    def __init__(self,_level : int,_pv : int, _maxPv : int,_pc : int,_maxPc):
        self.level : int = _level
        
        self.pv : int = _pv
        self.maxPv : int = _maxPv
        self.pc : int = _pc
        self.maxPc : int = _maxPc
        
        self.arme : Weapon = None
        
        self.isProtect : bool = False
        self.statutEffect : StatutEffect = None