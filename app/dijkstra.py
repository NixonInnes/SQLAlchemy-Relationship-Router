from sqlalchemy import inspect
from collections import defaultdict
from heapq import heappop, heappush
from app.db import Base

class Graph(object):
    def __init__(self, Base):
        self.tables = self.get_tables(Base)
        self.relationships = []
        self.get_relationships()
        
    def get_tables(self, Base):
        tables = {}
        for cls in Base._decl_class_registry.values():
            if hasattr(cls, '__tablename__'):
                tables[cls.__tablename__] = cls
        return tables

    def get_relationships(self):
        for table in self.tables:
            for rel in inspect(self.tables[table]).relationships:
                self.relationships.append((self.tables[table], self.tables[rel.table.name], 1))

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

    def walk(self, start, target):
        graph = defaultdict(list)

        for frm, to, dist in self.relationships:
            graph[frm].append( (dist, to) )

        queue = [self.Q(0, start, [])]
        checked = set()

        while queue:
            q = heappop(queue)
            if q.node not in checked:
                checked.add(q.node)
                path = q.path + [q.node]
                if q.node is target:
                    return q.dist, path
                for dist_n, node_n in graph.get(q.node):
                    if node_n not in checked:
                        heappush(queue, self.Q(q.dist+dist_n, node_n, path))
        return float('inf')

#g = Graph(Base)
#g.walk(g.tables['mid-mids'], g.tables['top-rights'])
