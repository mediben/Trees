from ..base import *

class Node(Base):
    __tablename__ = 'node'
    __mp_manager__ = 'mp'
    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('node.id'))
    parent = relation("Node", remote_side=[id])
    name = Column(String())

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
    
    def __repr__(self):
        return '<Node %r has heigh %r>' % self.name % self.mp_depth
