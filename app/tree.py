from sqlalchemy import inspect
from app.db import Base


def get_classes():
    classes = {}
    for cls in Base._decl_class_registry.values():
        if hasattr(cls, '__tablename__'):
            classes[cls.__tablename__] = cls
    return classes


classes = get_classes()


class Node(object):
    def __init__(self, cls):
        self.cls = cls
        rels = list(inspect(cls).relationships)
        self.relationships = {classes[r.table.name] : r for r in rels}

    def __str__(self):
        return "{} {}".format(self.cls, self.relationships)

    def __repr__(self):
        return "<Node: {}>".format(self.cls)


nodes = []
for cls in classes:
    nodes.append(Node(classes[cls]))


for node in nodes:
    print(node)


def walk(start, target):
    queue = [Node(start)]
    checked = set()
    while queue:
        node = queue.pop(0)
        if node.cls in checked:
            continue
        else:
            checked.add(node.cls)
            if node.cls is target:
                return node
            else:
                for rel in node.relationships:
                    if rel not in checked:
                        queue.append(Node(rel))

walk(classes['pipes'], classes['projects'])
