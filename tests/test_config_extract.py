import inept


def test_simple_options():

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

    assert list(conf) == ['a', 'a.x', 'a.y', 'b', 'b.x', 'b.y']
    assert list(subc) == ['x', 'y']

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


def test_simple_group():

    class Config(inept.Config):
        with _.group:
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

    assert list(conf) == ['a.x', 'a.y', 'b.x', 'b.y']
    assert list(subc) == ['x', 'y']

    assert conf.to_dict() == {}
    assert subc.to_dict() == {}

    conf['a.x'] = 42
    assert conf.to_dict() == {'a.x': 42}
    assert subc.to_dict() == {'x': 42}

    subc['y'] = 6
    assert conf.to_dict() == {'a.x': 42, 'a.y': 6}
    assert subc.to_dict() == {'x': 42, 'y': 6}

    conf['b.y'] = 12
    assert conf.to_dict() == {'a.x': 42, 'a.y': 6, 'b.y': 12}
    assert subc.to_dict() == {'x': 42, 'y': 6}


def test_simple_switch():

    class Config(inept.Config):
        with _.switch:
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

    assert list(conf) == ['a', 'a.x', 'a.y', 'b', 'b.x', 'b.y']
    assert list(subc) == ['x', 'y']

    assert conf.to_dict() == {}
    assert subc.to_dict() == {}

    conf['a.x'] = 42
    assert conf.to_dict() == {'a': True, 'a.x': 42}
    assert subc.to_dict() == {'x': 42}

    subc['y'] = 6
    assert conf.to_dict() == {'a': True, 'a.x': 42, 'a.y': 6}
    assert subc.to_dict() == {'x': 42, 'y': 6}

    conf['b.y'] = 12
    assert conf.to_dict() == {'b':True, 'b.y': 12}
    assert subc.to_dict() == {}

    subc['x'] = 5
    assert conf.to_dict() == {'a': True, 'a.x': 5, 'a.y': 6}
    assert subc.to_dict() == {'x': 5, 'y': 6}


def test_deep_options():

    class Config(inept.Config):
        with _.group:
            with _.options as a:
                with _.group as ap:
                    x: int
                    y: int
                with _.group as aq:
                    x: int
                    y: int
            with _.options as b:
                with _.group as bp:
                    x: int
                    y: int
                with _.group as bq:
                    x: int
                    y: int

    node_a = Config.root.nodes[0]
    node_ap = Config.root.nodes[0].nodes[0]
    assert node_ap.name == 'ap'

    conf = Config()
    c_a = conf.extract_node(node_a)
    c_ap = conf.extract_node(node_ap)

    assert list(conf) == [
        'a.ap', 'a.ap.x', 'a.ap.y',
        'a.aq', 'a.aq.x', 'a.aq.y',
        'b.bp', 'b.bp.x', 'b.bp.y',
        'b.bq', 'b.bq.x', 'b.bq.y',
    ]
    assert list(c_a) == [
        'ap', 'ap.x', 'ap.y',
        'aq', 'aq.x', 'aq.y',
    ]
    assert list(c_ap) == ['x', 'y']

    assert conf.to_dict() == {}
    assert c_a.to_dict() == {}
    assert c_ap.to_dict() == {}

    conf['a.ap.x'] = 42
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 42}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 42}
    assert c_ap.to_dict() == {'x': 42}

    c_a['ap.x'] = 21
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 21}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21}
    assert c_ap.to_dict() == {'x': 21}

    c_ap['y'] = 6
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 21, 'a.ap.y': 6}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}

    conf['b.bq.y'] = 12
    assert conf.to_dict() == {
        'a.ap': True, 'a.ap.x': 21, 'a.ap.y': 6, 'b.bq': True, 'b.bq.y': 12,
    }
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}


def test_deep_group():

    class Config(inept.Config):
        with _.group:
            with _.group as a:
                with _.group as ap:
                    x: int
                    y: int
                with _.group as aq:
                    x: int
                    y: int
            with _.group as b:
                with _.group as bp:
                    x: int
                    y: int
                with _.group as bq:
                    x: int
                    y: int

    node_a = Config.root.nodes[0]
    node_ap = Config.root.nodes[0].nodes[0]
    assert node_ap.name == 'ap'

    conf = Config()
    c_a = conf.extract_node(node_a)
    c_ap = conf.extract_node(node_ap)

    assert list(conf) == [
        'a.ap.x', 'a.ap.y',
        'a.aq.x', 'a.aq.y',
        'b.bp.x', 'b.bp.y',
        'b.bq.x', 'b.bq.y',
    ]
    assert list(c_a) == [
        'ap.x', 'ap.y',
        'aq.x', 'aq.y',
    ]
    assert list(c_ap) == ['x', 'y']

    assert conf.to_dict() == {}
    assert c_a.to_dict() == {}
    assert c_ap.to_dict() == {}

    conf['a.ap.x'] = 42
    assert conf.to_dict() == {'a.ap.x': 42}
    assert c_a.to_dict() == {'ap.x': 42}
    assert c_ap.to_dict() == {'x': 42}

    c_a['ap.x'] = 21
    assert conf.to_dict() == {'a.ap.x': 21}
    assert c_a.to_dict() == {'ap.x': 21}
    assert c_ap.to_dict() == {'x': 21}

    c_ap['y'] = 6
    assert conf.to_dict() == {'a.ap.x': 21, 'a.ap.y': 6}
    assert c_a.to_dict() == {'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}

    conf['b.bq.y'] = 12
    assert conf.to_dict() == {
        'a.ap.x': 21, 'a.ap.y': 6, 'b.bq.y': 12,
    }
    assert c_a.to_dict() == {'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}


def test_deep_switch():

    class Config(inept.Config):
        with _.group:
            with _.switch as a:
                with _.group as ap:
                    x: int
                    y: int
                with _.group as aq:
                    x: int
                    y: int
            with _.switch as b:
                with _.group as bp:
                    x: int
                    y: int
                with _.group as bq:
                    x: int
                    y: int

    node_a = Config.root.nodes[0]
    node_ap = Config.root.nodes[0].nodes[0]
    assert node_ap.name == 'ap'

    conf = Config()
    c_a = conf.extract_node(node_a)
    c_ap = conf.extract_node(node_ap)

    assert list(conf) == [
        'a.ap', 'a.ap.x', 'a.ap.y',
        'a.aq', 'a.aq.x', 'a.aq.y',
        'b.bp', 'b.bp.x', 'b.bp.y',
        'b.bq', 'b.bq.x', 'b.bq.y',
    ]
    assert list(c_a) == [
        'ap', 'ap.x', 'ap.y',
        'aq', 'aq.x', 'aq.y',
    ]
    assert list(c_ap) == ['x', 'y']

    assert conf.to_dict() == {}
    assert c_a.to_dict() == {}
    assert c_ap.to_dict() == {}

    conf['a.ap.x'] = 42
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 42}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 42}
    assert c_ap.to_dict() == {'x': 42}

    c_a['ap.x'] = 21
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 21}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21}
    assert c_ap.to_dict() == {'x': 21}

    c_ap['y'] = 6
    assert conf.to_dict() == {'a.ap': True, 'a.ap.x': 21, 'a.ap.y': 6}
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}

    conf['b.bq.y'] = 12
    assert conf.to_dict() == {
        'a.ap': True, 'a.ap.x': 21, 'a.ap.y': 6, 'b.bq': True, 'b.bq.y': 12,
    }
    assert c_a.to_dict() == {'ap': True, 'ap.x': 21, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 21, 'y': 6}

    c_a['aq.y'] = 7
    assert conf.to_dict() == {
        'a.aq': True, 'a.aq.y': 7, 'b.bq': True, 'b.bq.y': 12,
    }
    assert c_a.to_dict() == {'aq': True, 'aq.y': 7}
    assert c_ap.to_dict() == {}

    c_ap['x'] = 5
    assert conf.to_dict() == {
        'a.ap': True, 'a.ap.x': 5, 'a.ap.y': 6, 'b.bq': True, 'b.bq.y': 12,
    }
    assert c_a.to_dict() == {'ap': True, 'ap.x': 5, 'ap.y': 6}
    assert c_ap.to_dict() == {'x': 5, 'y': 6}

