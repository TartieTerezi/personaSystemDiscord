from Item import Item


# exemple d'un object 
# {object : [price,quantite]}
# {pomme : [10,10]}

class Shop(object):
    """Un shop pourra vendre des objets"""
    def __init__(self,objects = {}):
        self.objects = objects