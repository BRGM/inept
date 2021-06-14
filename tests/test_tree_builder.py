from inept.tree import Node
from inept.tree_builder import TreeBuilder


def test_build():

    class MyConfig(TreeBuilder):
        "MyConfig documentation, not for options"
        with _.group:
            _ = """
            general doc of option tree
            """
            a1ob: int = False
            _ = "a1ob doc"
            with _.switch as a2e:
                _ = "doc for a2e switch group"
                with _.switch as b1ef:
                    c1of: bool
                    c2of: bool
                    with _.group as c3gf:
                        d1o: str
                        d2o: str
                with _.group as b2gf:
                    with _.switch:
                        with _.group as d3gf:
                            e1oi: int = 50
                        d4of: bool
                    c4od: float = 1e-8
                    c5oi: int = 100
                    c6o: str
            with _.group as a3g:
                b3oi: int = 30
                b4od: float = 1e-6

    assert {Node.name_from_path(p) for p in MyConfig.__root__.walk()} == {
        '',
        'a1ob',
        'a2e.b1ef',
        'a2e.b1ef.c1of',
        'a2e.b1ef.c2of',
        'a2e.b1ef.c3gf',
        'a2e.b1ef.c3gf.d1o',
        'a2e.b1ef.c3gf.d2o',
        'a2e.b2gf',
        'a2e.b2gf.d3gf',
        'a2e.b2gf.d3gf.e1oi',
        'a2e.b2gf.d4of',
        'a2e.b2gf.c4od',
        'a2e.b2gf.c5oi',
        'a2e.b2gf.c6o',
        'a3g.b3oi',
        'a3g.b4od',
    }

