from test_config import test_conf_script, test_make_empty_conf


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


