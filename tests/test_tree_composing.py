import pytest
import inept


class MenuPasCher(inept.Config):
    with _.group:
        plat: str = "steak frite"
        with _.switch:
            entree: str
            dessert: str = "tarte"


class MenuComplet(inept.Config):
    with _.group:
        plat: str = "lasagnes"
        entree: str = "salade"
        dessert: str = "compote"


def test_simple():
    from inept import ConfigSimple, Value, Options, Switch
    carte_tree = Options(None, [
        Value('cafe', bool, False),
        Value('boisson', str),
        Switch(None, [
            MenuPasCher.root.rename("menu_base"),
            MenuComplet.root.rename("menu_complet"),
        ])
    ])
    order = ConfigSimple(carte_tree)
    assert order.all_keys() == [
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


def test_tree_builder():

    class Carte(inept.Config):
        with _.options:
            cafe: bool = False
            boisson: str
            with _.switch:
                menu_base = MenuPasCher.root
                menu_complet = MenuComplet.root

    order = Carte()
    assert order.all_keys() == [
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


def test_with_annotation():

    with pytest.raises(SyntaxError):

        class Carte(inept.Config):
            with _.options:
                cafe: bool = False
                boisson: str
                with _.switch:
                    menu_base: ... = MenuPasCher.root
                    menu_complet = MenuComplet.root

