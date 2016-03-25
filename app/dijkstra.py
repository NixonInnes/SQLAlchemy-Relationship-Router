from sqlalchemy import inspect
from collections import defaultdict
from heapq import heappop, heappush
from app.db import Base

class Router(object):
    def __init__(self, Base):
        self.tables = {}
        self.make_tables(Base)
        self.relationships = []
        self.make_relationships()
        self.graph = defaultdict(list)
        self.make_graph()
        
    def make_tables(self, Base):
        for cls in Base._decl_class_registry.values():
            if hasattr(cls, '__tablename__'):
                self.tables[cls.__tablename__] = cls

    def make_relationships(self):
        for table in self.tables:
            for rel in inspect(self.tables[table]).relationships:
                self.relationships.append((self.tables[table], self.tables[rel.table.name], 1))

    def make_graph(self):
        for frm, to, dist in self.relationships:
            self.graph[frm].append( (dist, to) ) 

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

    def get_route(self, start, target):
        queue = [self.Q(0, start, [])]
        checked = set()
        while queue:
            q = heappop(queue)
            if q.node not in checked:
                checked.add(q.node)
                path = q.path + [q.node]
                if q.node is target:
                    return q.dist, path
                for dist_n, node_n in self.graph.get(q.node):
                    if node_n not in checked:
                        heappush(queue, self.Q(q.dist+dist_n, node_n, path))
        return float('inf')

    # Makes life a little easier
    def table(self, tablename):
        return self.tables.get(tablename)

#g = Router(Base)
#g.get_route(g.tables['mid-mids'], g.tables['top-rights'])
