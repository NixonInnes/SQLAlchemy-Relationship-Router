from sqlalchemy import inspect
from collections import defaultdict
from heapq import heappop, heappush
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
relationships = []
for table in sql_tables:
    for rel in inspect(sql_tables[table]).relationships:
        relationships.append( (sql_tables[table], sql_tables[rel.table.name], 1) ) #Change this 1 to give "weight"/"distance" to the nodes


def walk(rels, start, target):
    graph = defaultdict(list)

    for frm, to, dist in rels:
        graph[frm].append( (dist, to) )

    queue = [ (0, start, ()) ]
    checked = set()

    while queue:
        print(queue)
        (dist, node, path) = heappop(queue)
        if rel not in checked:
            checked.add(rel)
            path = (rel, path)
            if node is target:
                return dist, path
            for dist_n, node_n in graph.get(node, ()):
                if node_n not in checked:
                    heappush(queue, (dist+dist_n, node_n, path))
    return float('inf')