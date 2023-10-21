from Item import Item


# exemple d'un object 
# {object : [price,quantite]}
# {pomme : [1,10]}

# exemple d'un objet qu'on peut vendre
# {object : [price]}

class Shop(object):
    """Un shop pourra vendre des objets"""
    def __init__(self,nom = "",objects = {}, objectsToSell = {}):
        self.nom = nom
        self.objects = objects
        self.objectsToSell = objectsToSell
        self.img = "https://static.wikia.nocookie.net/undertale/images/6/66/Tem_Shop_sprite.png"