import pytest

from inept import ConfigSimple, Group, Switch, Value, Options

from test_tree import test_make_tree


def test_make_empty_conf(**kwds):
    root = test_make_tree()
    conf = ConfigSimple(root, **kwds)
    return conf


def test_conf_type():
    conf = test_make_empty_conf()

    with pytest.raises(ValueError):
        conf['a2e.b2gf.d3gf.e1oi'] = 'toto'


def test_conf_script():
    conf = test_make_empty_conf()

    conf['a1ob'] = True
    conf["a2e.b1ef.c1of"] = True
    conf['a2e.b2gf.d4of'] = True
    conf['a2e.b2gf.d3gf.e1oi'] = 10
    conf['a2e.b2gf.d3gf'] = True

    assert conf['a1ob']
    assert conf['a2e.b2gf.d3gf.e1oi'] == 10
    assert conf['a2e.b2gf.d3gf']
    assert conf['a2e.b2gf.c5oi'] == 100
    assert conf['a3g.b3oi'] == 30

    return conf


def test_default_under_exclusif():
    root = Switch(None, [
        Value('x', int, 42),
        Value('y', bool)
    ])

    conf = ConfigSimple(root)

    assert conf['x'] == 42
    with pytest.raises(KeyError):
        conf['y']

    conf['y'] = True

    assert conf['y']
    with pytest.raises(KeyError):
        conf['x']


def test_multiple_default_under_exclusif():
    root = Switch(None, [
        Value('x', int, 42),
        Value('y', bool, True)
    ])

    with pytest.raises(ValueError):
        ConfigSimple(root)


def test_default_group_under_exclusif():
    root = Switch(None, [
        Group('a', default=True, nodes=[
            Value('x', int, 42),
            Value('y', bool, True)
        ]),
        Group('b', nodes=[
            Value('x', int, 42),
            Value('y', bool, True)
        ]),
    ])

    conf = ConfigSimple(root)

    assert conf['a']
    assert conf['a.x'] == 42
    assert conf['a.y']
    assert not conf['b']
    with pytest.raises(KeyError):
        conf['b.x']
    with pytest.raises(KeyError):
        conf['b.y']
    assert conf.to_dict() == {'a.x': 42, 'a.y': True}

    conf['b'] = True

    assert conf['b']
    assert conf['b.x'] == 42
    assert conf['b.y']
    assert not conf['a']
    with pytest.raises(KeyError):
        conf['a.x']
    with pytest.raises(KeyError):
        conf['a.y']
    assert conf.to_dict() == {'b.x': 42, 'b.y': True}

    conf['b'] = False
    assert not conf['a']
    with pytest.raises(KeyError):
        conf['a.x']
    with pytest.raises(KeyError):
        conf['a.y']
    assert not conf['b']
    with pytest.raises(KeyError):
        conf['b.x']
    with pytest.raises(KeyError):
        conf['b.y']
    assert conf.to_dict() == {}


def test_one_option():
    root = Options(None, [
        Group('a', nodes=[
            Value('x', int, 42),
            Value('y', bool, False)
        ]),
    ])

    conf = ConfigSimple(root)

    assert not conf['a']
    with pytest.raises(KeyError):
        conf['a.x']
    with pytest.raises(KeyError):
        conf['a.y']
    assert conf.to_dict() == {}

    conf['a'] = True

    assert conf['a']
    assert conf['a.x'] == 42
    assert conf['a.y'] == False
    assert conf.to_dict() == {'a.x': 42, 'a.y': False}

    conf['a'] = False

    assert not conf['a']
    with pytest.raises(KeyError):
        conf['a.x']
    with pytest.raises(KeyError):
        conf['a.y']
    assert conf.to_dict() == {}

    conf['a.x'] = 15

    assert conf['a']
    assert conf['a.x'] == 15
    assert conf['a.y'] == False
    assert conf.to_dict() == {'a.x': 15, 'a.y': False}


def test_options():
    root = Options(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ]),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])

    conf = ConfigSimple(root)
    assert conf.to_dict() == {}

    conf['a'] = True
    assert conf.to_dict() == {'a.x': 42, 'a.y': 'hello'}

    conf['a'] = False
    assert conf.to_dict() == {}

    conf['b.x'] = 12
    assert conf.to_dict() == {'b.x': 12, 'b.y': 'bye'}

    conf['a'] = True
    assert conf.to_dict() == {'a.x': 42, 'a.y': 'hello', 'b.x': 12, 'b.y': 'bye'}


def test_options_with_default():
    root = Options(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])

    conf = ConfigSimple(root)
    assert conf.to_dict() == {'a.x': 42, 'a.y': 'hello'}

    conf['a'] = True
    assert conf.to_dict() == {'a.x': 42, 'a.y': 'hello'}

    conf['a'] = False
    assert conf.to_dict() == {}

    conf['b.x'] = 12
    assert conf.to_dict() == {'b.x': 12, 'b.y': 'bye'}

    conf['a'] = True
    assert conf.to_dict() == {'a.x': 42, 'a.y': 'hello', 'b.x': 12, 'b.y': 'bye'}


def test_empty_conf_exclusive():
    conf = ConfigSimple(
        Switch(None, [
            Group('a', nodes=[
                Value('x', int, 42),
            ]),
            Group('b', nodes=[
                Value('x', int, 12),
            ]),
        ])
    )
    assert conf.to_dict() == {}


def test_empty_conf_default_under_exclusive():
    conf = ConfigSimple(
        Switch(None, [
            Group('a', default=True, nodes=[
                Value('x', int, 42),
            ]),
            Group('b', nodes=[
                Value('x', int, 12),
            ]),
        ])
    )
    assert conf.to_dict() == {'a.x': 42}

