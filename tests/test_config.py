from inept import Config


def test_build():

    class MenuPasCher(Config):
        " Le menu le moins cher "
        with group:
            plat: str = "steak frite"
            with switch:
                entree: str
                dessert: str
            cafe: bool = False

    return MenuPasCher


def test_setitem():
    conf = test_build()()
    assert conf.to_dict() == {'plat': 'steak frite', 'cafe': False}
    conf['dessert'] = "mousse au chocolat"
    assert conf.to_dict() == {'plat': 'steak frite', 'cafe': False, 'dessert': 'mousse au chocolat'}
    conf['entree'] = "soupe"
    assert conf.to_dict() == {'plat': 'steak frite', 'cafe': False, 'entree': 'soupe'}

