from Item import Item


# exemple d'un object 
# {object : [price,quantite]}
# {pomme : [1,10]}

class Shop(object):
    """Un shop pourra vendre des objets"""
    def __init__(self,nom = "",objects = {}):
        self.nom = nom
        self.objects = objects