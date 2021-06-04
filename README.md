# inept

An "**in**teractive **e**ditable o**pt**ions" library for handling complex option hierarchies
from multiple sources (script, CLI, config files, ...).

## Installation 

Install inept with pip

```bash 
  pip install inept
```

## Quick start

An option hierarchy is build by subclassing `inept.Config` and using the `with` statement.
Inside of the class body, the special variable `_` is made avalaible and provides different context managers that can customize the option nesting:
- a `with _.options` block will list **optional** values
- a `with _.group` block will list **mandatory** values
- a `with _.switch` block will list **mutually exclusive** values

```python
import inept

class RestaurantMenu(inept.Config):
    with _.options:
        coffe: bool = False
        drink: str
        with _.switch:
            with _.group as simple_menu:
                dish: str = "steak and fries"
                with _.switch:
                    starter: str
                    dessert: str = "apple pie"
            with _.group as full_menu:
                starter: str = "salad"
                dish: str = "lasagna"
                dessert: str = "compote"
```

An instance of this class will store option values while ensuring consistency with the declared hierachy.
Each option has a unique key, a string made of the nested option names, assembled with `'.'`.

```python
order = RestaurantMenu()
print(list(order))  # list of the option names
# Outputs:
# ['coffe',
#  'drink',
#  'simple_menu',
#  'simple_menu.plat',
#  'simple_menu.starter',
#  'simple_menu.dessert',
#  'full_menu',
#  'full_menu.starter',
#  'full_menu.dish',
#  'full_menu.dessert']
```


A configuration object acts like a dict for the set and get operations.
```python
order['coffe'] = True
order['full_menu.dessert'] = "creme brulee"
print(order['full_menu.starter'])  # default values are automatically set
# Outputs:
# 'salad'
```
The method `to_dict()` provides the full state of the configuration.
```python
print(order.to_dict())
# Outputs:
# {'coffe': True,
#  'full_menu': True,
#  'full_menu.starter': 'salad',
#  'full_menu.dish': 'lasagna',
#  'full_menu.dessert': 'creme brulee'}
```
According to the `options`/`group`/`switch` used during declaration, the options are optional, mandatory or mutually exclusive.
The configuration object ensures the consistency of its own state.
```python
order['simple_menu'] = True  # this erases 'full_menu' because 'simple_menu' and 'full_menu' are in a switch block
print(order.to_dict())
# Outputs:
# {'coffe': True,
#  'simple_menu': True,
#  'simple_menu.dish': 'steak and fries',
#  'simple_menu.dessert': 'apple pie'}
```

A nested dict can also be produced.
```python
print(order.to_nested_dict())
# Outputs:
# {'coffe': True,
#  'simple_menu': {'plat': 'steak and fries', 'dessert': 'apple pie'}}
```

A configuration can be filled from a dict.
```python
new_order = RestaurantMenu()
some_dict = {'full_menu': True, 'drink': 'water'}
some_nested_dict = {'simple_menu': {'starter': 'salad'}}
new_order.update(some_dict)
print(new_order.to_dict())
# Outputs:
# {'coffe': False,
#  'drink': 'water',
#  'full_menu': True,
#  'full_menu.starter': 'salad',
#  'full_menu.dish': 'lasagna',
#  'full_menu.dessert': 'compote'}
new_order.update(inept.flatten(some_nested_dict))
print(new_order.to_dict())
# Outputs:
# {'coffe': False,
#  'drink': 'water',
#  'simple_menu': True,
#  'simple_menu.plat': 'steak and fries',
#  'simple_menu.starter': 'salad'}
```

The command line arguments can be loaded at any time with 
```python
# $ python myscript.py --coffe true --full_menu.dessert jelly
order.load_cli()
```

## Roadmap

Inept is still in its early development.\
Here is a non-exhaustive list of the upcoming features:
- documentation
- handling of complexe types like file/path or enum
- composing tree declaration
- extracting sub configuration
- serialization to/from configuration file formats (yaml, json, INI, ...)
- improving command line interface

## Running Tests

To run tests, run the following command

```bash
  pytest
```

## Used By

This project is used by the following softwares:

- https://github.com/BRGM/ComPASS

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

