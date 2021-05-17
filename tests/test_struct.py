

def test_make_tree():
    root = Group(None, [
        Option("verbose", bool, default=False),
        Exclusive("linear_solver", [
            Exclusive('direct', is_flag=True, nodes=[
                Option("lu", is_flag=True),
                Option("cholesky", is_flag=True),
                Group("mumps", is_flag=True, nodes=[
                    Option("opt1"),
                    Option("opt2"),
                ]),
            ]),
            Group('iterative', is_flag=True, nodes=[
                Exclusive(None, [
                    Group("gmres", is_flag=True, nodes=[
                        Option("restart", int, default=50),
                    ]),
                    Option("bicgstab", is_flag=True),
                ]),
                Option("tolerance", float, default=1e-8),
                Option("maxit", int, default=100),
                Option("preconditioner"),
            ]),
        ]),
        Group("newton", [
            Option("maxit", int, default=30),
            Option("tolerance", float, default=1e-6),
        ])
    ])
    return root

