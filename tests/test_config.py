import pytest

from inept import Config

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

