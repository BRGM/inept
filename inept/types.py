
class Identity:

    __click_type__ = str

    def __new__(cls, obj):
        return obj


# class Choice:
#     def __init__(self, values):
#         assert all(isinstance(x, Node) for x in values)
#         self.values = list(values)
# 
#     def __call__(self, value):
#         ...

