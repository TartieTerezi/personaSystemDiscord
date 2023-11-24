from Item import Item

class Shop(object):
    """Un shop pourra vendre des objets"""
    def __init__(self,_nom : str = "",_objectsToBuy : dict[Item] = {}, _objectsToSell : dict[Item] = {}, _img : str = "https://static.wikia.nocookie.net/undertale/images/6/66/Tem_Shop_sprite.png"):
        self.nom : str = _nom
        """Nom du Shop."""
        self.objects : dict[Item] = _objectsToBuy
        """
            Liste des Items a vendre.
            # exemple d'un Item dans la liste 
            # {object : [price,quantite]}
            # {pomme : [1,10]}
        """
        self.objectsToSell : dict[Item] = _objectsToSell
        """
            Liste des Items que le shop peut acheter, pas de limite de ce que le shop peut acheter.
            # exemple d'un objet qu'on peut vendre
            # {object : [price]}
        """
        self.img : str = _img
        """Lien de l'image du shop."""