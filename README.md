# SQLAlchemy Relationship Router
Takes sqlalchemy database relationships, and uses the dijkstra algorith to find the shortest 'route' between two tables.  
Currently the 'distance' between two tables is 1; this can be modified to create preferential routes.

###Example
You have a database with objects related like so:  

<pre>
O----O----O  
|         |  
O----O----O 
|    |    |  
O----O----O
</pre>

O - representing each Base object  

Import initialied Base class into dijkstra.py from your model definitions:  
`from app.db import Base`  

Initialise a Router:  
`g = Router(Base)`  

All tables are stored in the router:  
`g.tables`  

Get a route:  
`g.get_route(g.tables['top-lefts'], g.tables['bottom-rights'])`  

This will return an (int, list) tuple representing the distance and path, respectively. i.e:  
`(4, [<class 'TopLeft'>, <class 'MidLeft'>, <class 'MidMid'>, <class 'BottomMid'>, <class 'BottomRight'>])`
