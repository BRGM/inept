import inept


def test_simple():

    class Config(inept.Config):
        with _.options:
            with _.group as a:
                x: int
                y: int
            with _.group as b:
                x: int
                y: int

    node_a = Config.root.nodes[0]
    assert node_a.name == 'a'

    conf = Config()
    subc = conf.extract_node(node_a)

    assert conf.to_dict() == {}
    assert subc.to_dict() == {}

    conf['a.x'] = 42
    assert conf.to_dict() == {'a': True, 'a.x': 42}
    assert subc.to_dict() == {'x': 42}

    subc['y'] = 6
    assert conf.to_dict() == {'a': True, 'a.x': 42, 'a.y': 6}
    assert subc.to_dict() == {'x': 42, 'y': 6}

    conf['b.y'] = 12
    assert conf.to_dict() == {'a': True, 'a.x': 42, 'a.y': 6, 'b':True, 'b.y': 12}
    assert subc.to_dict() == {'x': 42, 'y': 6}

