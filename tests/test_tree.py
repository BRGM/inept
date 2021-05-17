from inept import Group, Exclusive, Option


def test_make_tree():
    root = Group(None, [
        Option("a1ob", bool, default=False),
        Exclusive("a2e", [
            Exclusive('b1ef', is_flag=True, nodes=[
                Option("c1of", is_flag=True),
                Option("c2of", is_flag=True),
                Group("c3gf", is_flag=True, nodes=[
                    Option("d1o"),
                    Option("d2o"),
                ]),
            ]),
            Group('b2gf', is_flag=True, nodes=[
                Exclusive(None, [
                    Group("d3gf", is_flag=True, nodes=[
                        Option("e1oi", int, default=50),
                    ]),
                    Option("d4of", is_flag=True),
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

