import pytest
import click
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


def test_help(capsys):
    conf = test_make_empty_conf(command_name='cli')

    with pytest.raises(click.exceptions.Exit):
        conf.load_cli(["--help"])
    captured = capsys.readouterr()

    assert captured.out == """\
Usage: cli [OPTIONS]

Options:
  --a1ob BOOLEAN                a1ob doc
  --a2e.b1ef BOOLEAN            b1ef doc
  --a2e.b1ef.c1of BOOLEAN
  --a2e.b1ef.c2of BOOLEAN
  --a2e.b1ef.c3gf BOOLEAN
  --a2e.b1ef.c3gf.d1o TEXT      d1o doc
  --a2e.b1ef.c3gf.d2o TEXT
  --a2e.b2gf BOOLEAN
  --a2e.b2gf.d3gf BOOLEAN
  --a2e.b2gf.d3gf.e1oi INTEGER
  --a2e.b2gf.d4of BOOLEAN
  --a2e.b2gf.c4od FLOAT
  --a2e.b2gf.c5oi INTEGER
  --a2e.b2gf.c6o TEXT
  --a3g.b3oi INTEGER
  --a3g.b4od FLOAT
  --help                        Show this message and exit.
"""

