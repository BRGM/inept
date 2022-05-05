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

    assert c.all_keys() == [
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
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'tarte',
    }

    c['menu_base.dessert'] = 'mousse au chocolat'
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'mousse au chocolat',
    }

    c['menu_base.entree'] = 'soupe'
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
        'menu_base.plat': 'steak frite',
        'menu_base.entree': 'soupe',
    }

    c['menu_complet'] = True
    assert c.to_dict() == {
        'cafe': False,
        'boisson': 'limonade',
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
        'menu_base.plat': 'steak frite',
        'menu_base.entree': 'soupe',
    }


def test_carte_swith_to_False():
    """
    putting an inactive switched group to False should not change config
    see issue #37
    """

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

    c['menu_base'] = True
    assert c.to_dict() == {
        'cafe': False,
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'tarte'
    }

    c['menu_complet'] = False
    assert c.to_dict() == {
        'cafe': False,
        'menu_base.plat': 'steak frite',
        'menu_base.dessert': 'tarte'
    }


def test_switch_in_switch_set_False():

    class Conf(Config):
        with _.switch:
            with _.switch as a:
                u: str
                v: str
            with _.switch as b:
                x: str
                y: str

    c = Conf()

    assert c.to_dict() == {}

    c['a.u'] = 1
    assert c.to_dict() == {'a.u': '1'}

    c['b.x'] = 2
    assert c.to_dict() == {'b.x': '2'}

