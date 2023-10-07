import sqlite3
from Dao import Dao

class StatutEffect(object):
    """Docstring for Statut Effect"""

    def __init__(self,index,nom):
        self.id = index
        self.nom = nom
        
    @classmethod
    def byBdd(cls,index : int):
        result = Dao.getOneDataBdd("SELECT * FROM StatutEffect where id = ?",[index])
        
        return StatutEffect(result[0],result[1])
