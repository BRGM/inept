from inept import Group, Exclusive, Option


def test_make_tree():
    root = Group(None, [
        Option("a1ob", bool, default=False, doc="a1ob doc"),
        Exclusive("a2e", [
            Exclusive('b1ef', is_flag=True, doc="b1ef doc", nodes=[
                Option("c1of", bool),
                Option("c2of", bool),
                Group("c3gf", is_flag=True, nodes=[
                    Option("d1o", doc="d1o doc"),
                    Option("d2o"),
                ]),
            ]),
            Group('b2gf', is_flag=True, nodes=[
                Exclusive(None, [
                    Group("d3gf", is_flag=True, nodes=[
                        Option("e1oi", int, default=50),
                    ]),
                    Option("d4of", bool),
                ]),
                Option("c4od", float, default=1e-8),
                Option("c5oi", int, default=100),
                Option("c6o"),
            ]),
        ]),
        Group("a3g", [
            Option("b3oi", int, default=30),
            Option("b4od", float, default=1e-6),
        ])
    ])
    return root

