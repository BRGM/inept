from inept import Config, Group, Exclusive, Option


def test_default_under_flag_group():
    root = Group(None, [
        Group('a', is_flag=True, nodes=[
            Option('x', int, 42),
            Option('y', bool, False)
        ]),
    ])

    conf = Config(root)

    assert conf.to_dict() == {}
    assert conf.to_nested_dict() == {}

    conf['a'] = True

    assert conf.to_dict() == {
        'a': True,
        'a.x': 42,
        'a.y': False,
    }
    assert conf.to_nested_dict() == {
        'a': {
            'x': 42,
            'y': False,
        },
    }

    conf['a'] = False

    assert conf.to_dict() == {}
    assert conf.to_nested_dict() == {}

    conf['a.x'] = 2

    assert conf.to_dict() == {
        'a': True,
        'a.x': 2,
        'a.y': False,
    }
    assert conf.to_nested_dict() == {
        'a': {
            'x': 2,
            'y': False,
        },
    }

