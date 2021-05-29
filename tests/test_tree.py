import pytest
from inept import Value, Group, Options, Switch


def test_simple_Switch():
    root = Switch(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Switch None>,)",
        "(<Switch None>, <Group 'a'>)",
        "(<Switch None>, <Group 'a'>, <Value 'x'>)",
        "(<Switch None>, <Group 'a'>, <Value 'y'>)",
        "(<Switch None>, <Group 'b'>)",
        "(<Switch None>, <Group 'b'>, <Value 'x'>)",
        "(<Switch None>, <Group 'b'>, <Value 'y'>)",
    ]


def test_simple_Options():
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
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Options None>,)",
        "(<Options None>, <Group 'a'>)",
        "(<Options None>, <Group 'a'>, <Value 'x'>)",
        "(<Options None>, <Group 'a'>, <Value 'y'>)",
        "(<Options None>, <Group 'b'>)",
        "(<Options None>, <Group 'b'>, <Value 'x'>)",
        "(<Options None>, <Group 'b'>, <Value 'y'>)",
    ]


def test_simple_Group():
    root = Group(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Group None>,)",
        "(<Group None>, <Group 'a'>, <Value 'x'>)",
        "(<Group None>, <Group 'a'>, <Value 'y'>)",
        "(<Group None>, <Group 'b'>, <Value 'x'>)",
        "(<Group None>, <Group 'b'>, <Value 'y'>)",
    ]


def test_deeper_Switch():
    root = Switch(None, [
        Group('a', [
            Options('p', [
                Value('x', int, 42),
                Value('y', str, 'hello'),
            ]),
        ], True),
        Group('b', [
            Options('q', [
                Value('x', int, 6),
                Value('y', str, 'bye'),
            ]),
        ]),
    ])
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Switch None>,)",
        "(<Switch None>, <Group 'a'>)",
        "(<Switch None>, <Group 'a'>, <Options 'p'>, <Value 'x'>)",
        "(<Switch None>, <Group 'a'>, <Options 'p'>, <Value 'y'>)",
        "(<Switch None>, <Group 'b'>)",
        "(<Switch None>, <Group 'b'>, <Options 'q'>, <Value 'x'>)",
        "(<Switch None>, <Group 'b'>, <Options 'q'>, <Value 'y'>)",
    ]


def test_deeper_Options():
    root = Options(None, [
        Group('a', [
            Options('p', [
                Value('x', int, 42),
                Value('y', str, 'hello'),
            ]),
        ], True),
        Group('b', [
            Options('q', [
                Value('x', int, 6),
                Value('y', str, 'bye'),
            ]),
        ]),
    ])
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Options None>,)",
        "(<Options None>, <Group 'a'>)",
        "(<Options None>, <Group 'a'>, <Options 'p'>, <Value 'x'>)",
        "(<Options None>, <Group 'a'>, <Options 'p'>, <Value 'y'>)",
        "(<Options None>, <Group 'b'>)",
        "(<Options None>, <Group 'b'>, <Options 'q'>, <Value 'x'>)",
        "(<Options None>, <Group 'b'>, <Options 'q'>, <Value 'y'>)",
    ]


def test_deeper_Group():
    root = Group(None, [
        Group('a', [
            Options('p', [
                Value('x', int, 42),
                Value('y', str, 'hello'),
            ]),
        ], True),
        Group('b', [
            Options('q', [
                Value('x', int, 6),
                Value('y', str, 'bye'),
            ]),
        ]),
    ])
    root.validate()
    assert list(map(str, root.walk())) == [
        "(<Group None>,)",
        "(<Group None>, <Group 'a'>, <Options 'p'>, <Value 'x'>)",
        "(<Group None>, <Group 'a'>, <Options 'p'>, <Value 'y'>)",
        "(<Group None>, <Group 'b'>, <Options 'q'>, <Value 'x'>)",
        "(<Group None>, <Group 'b'>, <Options 'q'>, <Value 'y'>)",
    ]


def test_make_tree():
    root = Group(None, [
        Value("a1ob", bool, default=False, doc="a1ob doc"),
        Switch("a2e", [
            Switch('b1ef', doc="b1ef doc", nodes=[
                Value("c1of", bool),
                Value("c2of", bool),
                Group("c3gf", nodes=[
                    Value("d1o", doc="d1o doc"),
                    Value("d2o"),
                ]),
            ]),
            Group('b2gf', nodes=[
                Switch(None, [
                    Group("d3gf", nodes=[
                        Value("e1oi", int, default=50),
                    ]),
                    Value("d4of", bool),
                ]),
                Value("c4od", float, default=1e-8),
                Value("c5oi", int, default=100),
                Value("c6o"),
            ]),
        ]),
        Group("a3g", [
            Value("b3oi", int, default=30),
            Value("b4od", float, default=1e-6),
        ])
    ])
    root.validate()
    assert list(map(Value.name_from_path, root.walk())) == [
        '',
        'a1ob',
        'a2e.b1ef',
        'a2e.b1ef.c1of',
        'a2e.b1ef.c2of',
        'a2e.b1ef.c3gf',
        'a2e.b1ef.c3gf.d1o',
        'a2e.b1ef.c3gf.d2o',
        'a2e.b2gf',
        'a2e.b2gf.d3gf',
        'a2e.b2gf.d3gf.e1oi',
        'a2e.b2gf.d4of',
        'a2e.b2gf.c4od',
        'a2e.b2gf.c5oi',
        'a2e.b2gf.c6o',
        'a3g.b3oi',
        'a3g.b4od',
    ]
    return root


def test_invalid_duplicate():
    root = Switch(None, [
        Group('a', [
            Value('x', int, 42),
            Value('x', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])
    with pytest.raises(ValueError):
        root.validate()


def test_invalid_duplicate_2():
    root = Switch(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ], True),
        Group('a', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ]),
    ])
    with pytest.raises(ValueError):
        root.validate()


def test_invalid_Switch_multiple_activated():
    root = Switch(None, [
        Group('a', [
            Value('x', int, 42),
            Value('x', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ], True),
    ])
    with pytest.raises(ValueError):
        root.validate()


def test_invalid_Switch_multiple_activated():
    root = Switch(None, [
        Group('a', [
            Value('x', int, 42),
            Value('y', str, 'hello'),
        ], True),
        Group('b', [
            Value('x', int, 6),
            Value('y', str, 'bye'),
        ], False),
    ])
    root.validate()
