import collections


def flatten_path(nested, parent_key=()):
    items = []
    for k, v in nested.items():
        new_key = parent_key + (k,)
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_path(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten(nested, sep='.'):
    return {sep.join(k): v for k, v in flatten_path(nested).items()}
