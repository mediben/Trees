from flask import Blueprint, request
from .views import create_node, get_children, fetch_tree, move_node_children

tree = Blueprint('tree', __name__)

@tree.route('/tree', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        """
        # Create node
        @params:
        name => name or data of the new node
        parent => the wished parent id 
        """
        data = request.get_json(force=True) 
        name = data['name']
        parent = None
        if (len(data))>1:
            parent = data['parent']
        res = create_node(name, parent)
        return 'asked for post'
    else:
        #get all tree
        res = fetch_tree()
        return str(res)

@tree.route('/edit', methods=['POST'])
def update():
    if request.method == 'POST':
        """
        # Move subtree selected to its new position
        @params:
        node => node id
        destination => id of new parent node
        """
        data = request.get_json(force=True) 
        res = move_node_children(data['node'], data['destination'])
        return res

@tree.route('/view', methods=['POST'])
def manage():
    if request.method == 'POST':
        """
        # Get children of given node
         @params: node => Current parent node id. 
        """
        data = request.get_json(force=True) 
        res = get_children(data['node'])
        return res