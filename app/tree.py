from sqlalchemy import inspect
from app.db import Base

def get_sql_tables():
    classes = {}
    for cls in Base._decl_class_registry.values():
        if hasattr(cls, '__tablename__'):
            classes[cls.__tablename__] = cls
    return classes


# { tablename : table_object }
# i.e. { 'pipes': <class '__main__.Pipe'> }
sql_tables = get_sql_tables()

# { table_object : node_object }
# i.e. { <class '__main__.User'> : <Node: <class '__main__.User'>> }
class_nodes = {}

class Node(object):
    def __init__(self, cls):
        self.cls = cls
        self.rels = list(inspect(cls).relationships)
        class_nodes[self.cls] = self
        self.create_related_nodes()

    def create_related_nodes(self):
        for r in self.rels:
            if sql_tables[r.table.name] not in class_nodes:
                class_nodes[sql_tables[r.table.name]] = Node(sql_tables[r.table.name])

    def __str__(self):
        return "{} {}".format(self.cls, self.rels)

    def __repr__(self):
        return "<Node: {}>".format(self.cls)


# give me table strings
def walk(start, target):
    Node(sql_tables[start])
    path = [start]
    queue = [class_nodes[sql_tables[start]]]
    checked = set()
    while queue:
        #print("Q",queue)
        #print("C",checked)
        node = queue.pop(0)
        if node in checked:
            continue
        else:
            checked.add(node)
            if node.cls is sql_tables[target]:
                print('.'.join(path))
                return node
            else:
                for rel in node.rels:
                    if class_nodes[sql_tables[rel.table.name]] not in checked:
                        path.append(str(rel.class_attribute).split('.')[1])
                        queue.append(class_nodes[sql_tables[rel.table.name]])

def test_walk():
    print("TEST: walk('pipes', 'projects')")
    return walk('pipes', 'projects')

test_walk()