import inept


def test_simple():
    class Config(inept.Config):
        with _.group:
            a: int = 42

    c1 = Config()
    c2 = Config()
    c1['a'] = 6
    assert (c2|c1).to_dict() == {'a': 6}
    assert (c1|c2).to_dict() == {'a': 6}


def test_merge_setitem_win():

    class MenuPasCher(inept.Config):
        " Le menu le moins cher "
        with _.group:
            plat: str = "steak frite"
            with _.switch:
                entree: str
                dessert: str
            cafe: bool = False

    c1 = MenuPasCher()
    c2 = MenuPasCher()
    c1['dessert'] = "mousse au chocolat"
    c2['plat'] = "ravioli"
    assert c1.to_dict() == {'plat': 'steak frite', 'dessert': "mousse au chocolat", "cafe": False}
    assert c2.to_dict() == {'plat': 'ravioli', "cafe": False}
    assert (c1|c2).to_dict() == {'plat': 'ravioli', 'dessert': "mousse au chocolat", "cafe": False}
    assert (c2|c1).to_dict() == {'plat': 'ravioli', 'dessert': "mousse au chocolat", "cafe": False}
    assert c1.to_dict() == {'plat': 'steak frite', 'dessert': "mousse au chocolat", "cafe": False}
    assert c2.to_dict() == {'plat': 'ravioli', "cafe": False}
    c2['cafe'] = True
    assert c2.to_dict() == {'plat': 'ravioli', "cafe": True}
    assert (c1|c2).to_dict() == {'plat': 'ravioli', 'dessert': "mousse au chocolat", "cafe": True}
    assert (c2|c1).to_dict() == {'plat': 'ravioli', 'dessert': "mousse au chocolat", "cafe": True}
    assert c1.to_dict() == {'plat': 'steak frite', 'dessert': "mousse au chocolat", "cafe": False}
    assert c2.to_dict() == {'plat': 'ravioli', "cafe": True}
    c1['entree'] = 'soupe'
    assert c1.to_dict() == {'plat': 'steak frite', 'entree': "soupe", "cafe": False}
    assert (c1|c2).to_dict() == {'plat': 'ravioli', 'entree': "soupe", "cafe": True}
    assert (c2|c1).to_dict() == {'plat': 'ravioli', 'entree': "soupe", "cafe": True}
    assert c1.to_dict() == {'plat': 'steak frite', 'entree': "soupe", "cafe": False}
    assert c2.to_dict() == {'plat': 'ravioli', "cafe": True}

