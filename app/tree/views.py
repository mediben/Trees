from .models import Node
from ..base import Session, engine, Base
from sqlalchemy.sql import exists
import json

def create_node(param, parentX=None):
    Base.metadata.create_all(engine)
    session = Session()
    #Check if root exist
    if parentX is None:
        root_exist = get_root()
        if not root_exist:
            node = Node(param)
        else:
            return ({'msg' : 'Tree has a root and there can only be one Root, Daa !', 'code':'301'})
    else:
            parent_node = session.query(Node).filter(Node.id==parentX).first()
            node = Node(param, parent=parent_node)    
    session.add(node)
    session.commit()
    session.flush()
    session.close()
    return ({'msg':'Node created', 'code':'200'})

def fetch_tree():
    session = Session()
    nodes = Node.mp.query(session).all()
    session.close()
    res = []
    for node in nodes:
        dic={}
        dic['id'] = node.id
        dic['name'] = node.name
        dic['parent'] = get_parent(node.parent_id)
        dic['heigh'] = node.mp_depth
        res.append(dic)
    return json.dumps({'code':'200', 'msg':res})

def get_root():
    session = Session()
    is_root = session.query(exists().where(Node.mp_depth == '0')).scalar()
    session.flush()
    session.close()
    return is_root

def get_descendants(param):
    """
    param: is Node id
    """
    session = Session()
    node = session.query(Node).filter(Node.id==param).first()
    res = []
    for descendants in node.mp.query_descendants(and_self=False):
        dic = {}
        dic['id'] = descendants.id
        dic['name'] = descendants.name
        dic['depth'] = descendants.mp_depth
        dic['path'] = descendants.mp_path
        res.append(dic)
    session.flush()
    session.close()
    return json.dumps({'code':'200', 'msg':res})

def get_children(param):
    """
    param: is Node id
    """
    session = Session()
    parent = session.query(Node).filter(Node.id==param).first()
    res = []
    for child in parent.mp.query_children().all():
        dic = {}
        dic['id'] = child.id
        dic['name'] = child.name
        dic['depth'] = child.mp_depth
        dic['path'] = child.mp_path
        res.append(dic)
    session.flush()
    session.close()
    return json.dumps({'code':'200', 'msg':res})

def move_node_children(param, new_parent):
    """
    param: is Node id
    new_parent: new parent node id
    """
    session = Session()
    Node.mp.move_subtree_to_bottom(session,param,new_parent)
    session.commit()
    session.close()
    return ({'msg':'Node created', 'code':'200'})

def get_parent(p_id):
    if p_id :
        session = Session()
        node = session.query(Node).filter(Node.id==p_id).first()
        session.flush()
        session.close()
        return node.name
    else:
        return 'No parent'
    