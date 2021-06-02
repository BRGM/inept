from inept.utils import flatten, flatten_path


def test_flatten_tuple():
    nested = {
        'a': 1,
        'c': {
            'a': 2,
            'b': {
                'x': 5,
                'y' : 10
            }
        },
        'd': [1, 2, 3]
    }

    assert flatten_path(nested) == {
        ('a',): 1,
        ('c', 'a'): 2,
        ('c', 'b', 'x'): 5,
        ('c', 'b', 'y'): 10,
        ('d',): [1, 2, 3],
    }


def test_a():
    nested = {
        'a': 1,
        'c': {
            'a': 2,
            'b': {
                'x': 5,
                'y' : 10
            }
        },
        'd': [1, 2, 3]
    }

    assert flatten(nested) == {
        'a': 1,
        'c.a': 2,
        'c.b.x': 5,
        'c.b.y': 10,
        'd': [1, 2, 3],
    }
