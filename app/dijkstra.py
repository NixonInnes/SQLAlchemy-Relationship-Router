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
sql_tables = get_sql_tables()

class Q(object):
    def __init__(self, dist, node, path):
        self.dist = dist
        self.node = node
        if not isinstance(path, list):
            self.path = [path]
        else:
            self.path = path

    def __lt__(self, other):
        return self.dist < other.dist
        

relationships = []

for table in sql_tables:
    for rel in inspect(sql_tables[table]).relationships:
        relationships.append((sql_tables[table], sql_tables[rel.table.name], 1))
        

def walk(rels, start, target):
    graph = defaultdict(list)

    for frm, to, dist in rels:
        graph[frm].append( (dist, to) )

    queue = [Q(0, start, [])]
    checked = set()

    while queue:
        #print(queue)
        q = heappop(queue)
        if q.node not in checked:
            checked.add(q.node)
            path = q.path + [q.node]
            if q.node is target:
                return q.dist, path
            for dist_n, node_n in graph.get(q.node, ()):
                if node_n not in checked:
                    heappush(queue, Q(q.dist+dist_n, node_n, path))
    return float('inf')

#print("TEST: walk(relationships, sql_tables['mid-mids'], sql_tables['top-rights'])")
#print(walk(relationships, sql_tables['mid-mids'], sql_tables['top-rights']))
