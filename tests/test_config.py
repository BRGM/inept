import pytest

from inept import Config, Group, Exclusive, Option

from test_tree import test_make_tree


def test_make_empty_conf():
    root = test_make_tree()
    conf = Config(root)
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

    assert conf['a1ob'] == True
    assert conf['a2e.b2gf.d3gf.e1oi'] == 10
    assert conf['a2e.b2gf.d3gf'] == True
    assert conf['a2e.b2gf.c5oi'] == 100
    assert conf['a3g.b3oi'] == 30

    return conf


def test_conf_cli():
    conf = test_conf_script()
    conf.load_cli([
        "--a2e.b2gf.c4od", "1e-4",
        "--a1ob", "False",
        "--a2e.b2gf.d3gf.e1oi", "20"
    ])

    assert conf['a1ob'] == False
    assert conf['a2e.b2gf.d3gf.e1oi'] == 20
    assert conf['a2e.b2gf.d3gf'] == True
    assert conf['a2e.b2gf.c5oi'] == 100
    assert conf['a2e.b2gf.c4od'] == 1e-4
    assert conf['a3g.b3oi'] == 30


def test_conf_cli_alone():
    conf = test_make_empty_conf()

    conf.load_cli([
        '--a1ob', 'True',
        "--a2e.b1ef.c1of", 'True',
        '--a2e.b2gf.d4of', 'True',
        '--a2e.b2gf.d3gf.e1oi', '10',
        '--a2e.b2gf.d3gf', 'True',
    ])

    assert conf['a1ob'] == True
    assert conf['a2e.b2gf.d3gf.e1oi'] == 10
    assert conf['a2e.b2gf.d3gf'] == True
    assert conf['a2e.b2gf.c5oi'] == 100
    assert conf['a3g.b3oi'] == 30


def test_default_under_exclusif():
    root = Exclusive(None, [
        Option('x', int, 42),
        Option('y', bool)
    ])

    conf = Config(root)

    assert conf['x'] == 42
    with pytest.raises(KeyError):
        conf['y']

    conf['y'] = True

    assert conf['y'] == True
    with pytest.raises(KeyError):
        conf['x']


def test_multiple_default_under_exclusif():
    root = Exclusive(None, [
        Option('x', int, 42),
        Option('y', bool, True)
    ])

    with pytest.raises(ValueError):
        Config(root)


def test_default_group_under_exclusif():
    root = Exclusive(None, [
        Group('a', is_flag=True, default=True, nodes=[
            Option('x', int, 42),
            Option('y', bool, True)
        ]),
        Group('b', is_flag=True, nodes=[
            Option('x', int, 42),
            Option('y', bool, True)
        ]),
    ])

    conf = Config(root)

    assert conf['a'] == True
    assert conf['a.x'] == 42
    assert conf['a.y'] == True
    with pytest.raises(KeyError):
        conf['b']

    conf['b'] = True

    assert conf['b'] == True
    assert conf['b.x'] == 42
    assert conf['b.y'] == True
    with pytest.raises(KeyError):
        conf['a']

    conf['b'] = False

    # WARNING : old default come back !
    assert conf['a'] == True
    assert conf['a.x'] == 42
    assert conf['a.y'] == True
    with pytest.raises(KeyError):
        conf['b']


def test_default_under_flag_group():
    root = Group(None, [
        Group('a', is_flag=True, nodes=[
            Option('x', int, 42),
            Option('y', bool, False)
        ]),
    ])

    conf = Config(root)

    with pytest.raises(KeyError):
        conf['a']

    conf['a'] = True

    assert conf['a'] == True
    assert conf['a.x'] == 42
    assert conf['a.y'] == False

    conf['a'] = False

    with pytest.raises(KeyError):
        conf['a']

