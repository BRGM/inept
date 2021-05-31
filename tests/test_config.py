from inept import Config


def test_build():

    class MenuPasCher(Config):
        " Le menu le moins cher "
        with _.group:
            plat: str = "steak frite"
            with _.switch:
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


def test_carte():

    class Carte(Config):
        with _.options:
            cafe: bool = False
            boisson: str
            with _.switch:
                with _.group as menu_base:
                    plat: str = "steak frite"
                    with _.switch:
                        entree: str
                        dessert: str = "tarte"
                with _.group as menu_complet:
                    plat: str = "lasagnes"
                    entree: str = "salade"
                    dessert: str = "compote"

    c = Carte()

    assert list(c) == [
        'cafe',
        'boisson',
        'menu_base',
        'menu_base.plat',
        'menu_base.entree',
        'menu_base.dessert',
        'menu_complet',
        'menu_complet.plat',
        'menu_complet.entree',
        'menu_complet.dessert',
    ]

    assert c.to_dict() == {'cafe': False}

    c['boisson'] = "limonade"
    assert c.to_dict() == {'cafe': False, 'boisson': 'limonade'}

    c['menu_base'] = True
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base': True,
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'tarte',
    }

    c['menu_base.dessert'] = 'mousse au chocolat'
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base': True,
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'mousse au chocolat',
    }

    c['menu_base.entree'] = 'soupe'
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base': True,
        'menu_base.plat': 'steak frite',
        'menu_base.entree': 'soupe',
    }

    c['menu_complet'] = True
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_complet': True,
        'menu_complet.entree': 'salade',
        'menu_complet.plat': 'lasagnes',
        'menu_complet.dessert': 'compote',
    }

    c['menu_complet'] = False
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
    }

    c['menu_base'] = True
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base': True,
        'menu_base.plat': 'steak frite',
        'menu_base.entree': 'soupe',
    }

