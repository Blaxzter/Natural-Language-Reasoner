import pydot

from logics.senteces.Expression import Expression


class TreeGenerator:
    """
    Interface to the pydot libary
    """

    def __init__(self, root_expressions):
        """
        Creates the graph and root node
        :param root_expressions:
        """
        self.graph = pydot.Dot(' ', graph_type = 'graph')
        self.root_node = pydot.Node(0, id="root_node", label = self.get_rule_string(root_expressions, "Initial root", None), shape = 'polygon', tooltip=" ")
        self.graph.add_node(self.root_node)
        self.node_id = 1

    def add_node(self, parent_node, applied_rule, rule_id):
        """
        Add a node to the tree below the given parent node

        :param parent_node:   The node the new node should be below
        :param applied_rule:  The rule of through whcih the node is created
        :param rule_id:       The id of the node
        :return: The created node
        """
        # If we have a split rule then create more then just on rule
        new_nodes = []

        # If we have no created expression it is a tautology
        if applied_rule.created_expressions is None:
            new_node = pydot.Node(self.node_id, id=f"node_{rule_id}", label = f'{self.get_rule_string([applied_rule.c_expression, applied_rule.matched_expression], applied_rule.rule_desc_obj["name"], applied_rule.referenced_line)}', shape = 'polygon', tooltip=" ")
            self.graph.add_node(new_node)
            my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
            self.graph.add_edge(my_edge)
            self.node_id += 1
            new_nodes.append(new_node)
        else:
            # Go over each branch in the created expression
            for new_exp in applied_rule.created_expressions.values():
                new_node = pydot.Node(self.node_id, id=f"node_{rule_id}", label = f'{self.get_rule_string(new_exp, applied_rule.rule_desc_obj["name"], applied_rule.referenced_line)}', shape = 'polygon', tooltip=" ")
                self.graph.add_node(new_node)

                my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
                self.graph.add_edge(my_edge)
                self.node_id += 1
                new_nodes.append(new_node)
        return new_nodes

    @staticmethod
    def get_rule_string(expression: Expression, rule_name, reference_line):
        """
        Create the string for the pydot node

        :param expression:      The new expressions
        :param rule_name:       The name of the used rule
        :param reference_line:  The line that was used (or id)
        :return: Created string
        """
        sorted_exp = sorted(expression, key = lambda expr: expr.id)

        reference_line_str = f'<td ROWSPAN="{len(expression)}" SIDES="L">{reference_line}</td>' if reference_line is not None or rule_name == 'Tautologie' else ""

        tautologie_line = ""
        table_head = f'<tr><td COLSPAN="3" ALIGN="CENTER" SIDES="B">{rule_name}</td></tr>'
        if rule_name == 'Tautologie':
            tautologie_line = f'<tr><td COLSPAN="3" ALIGN="CENTER" SIDES="T">X</td></tr>'
            table_head = ''

        return f'''<
        <table border="0" CELLBORDER="1">
        {table_head}
        {''.join([f'<tr><td BORDER="0" CELLSPACING="10">{orig.id}:</td><td BORDER="0" ALIGN="LEFT">{orig.get_string_rep()}</td>{reference_line_str if i == 0 else ""}</tr>' for i, orig in enumerate(sorted_exp)])}
        {tautologie_line}
        </table>
        >'''
        # return '\n'.join([' '.join(item.tokens) for item in expression])

    def create_file(self):
        """
        The create file method returns just the pydot string of the graph
        :return:
        """
        return self.graph.to_string()
