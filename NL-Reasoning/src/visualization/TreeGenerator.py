import pydot

from logics.Expression import Expression


class TreeGenerator:

    def __init__(self, premise):
        self.graph = pydot.Dot('applied_rules', graph_type = 'graph')
        self.root_node = pydot.Node(0, id="root_node", label = self.get_rule_string(premise, "Initial root", None), shape = 'polygon', fillcolor='#1f77b4')
        self.graph.add_node(self.root_node)
        self.node_id = 1

    def add_node(self, parent_node, applied_rule):
        new_nodes = []

        if applied_rule.created_expressions is None:
            new_node = pydot.Node(self.node_id, label = f'{self.get_rule_string([applied_rule.c_expression, applied_rule.matched_expression], applied_rule.rule_name, applied_rule.referenced_line)}', shape = 'polygon', fillcolor='#1f77b4')
            self.graph.add_node(new_node)
            my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
            self.graph.add_edge(my_edge)
            self.node_id += 1
            new_nodes.append(new_node)
        else:
            for new_exp in applied_rule.created_expressions.values():
                new_node = pydot.Node(self.node_id, label = f'{self.get_rule_string(new_exp, applied_rule.rule_name, applied_rule.referenced_line)}', shape = 'polygone', fillcolor="#1f77b4")
                self.graph.add_node(new_node)

                my_edge = pydot.Edge(parent_node.get_name(), str(self.node_id))
                self.graph.add_edge(my_edge)
                self.node_id += 1
                new_nodes.append(new_node)
        return new_nodes

    def get_rule_string(self, expression: Expression, rule_name, reference_line):

        sorted_exp = sorted(expression, key = lambda expr: expr.id)

        reference_line_str = f'<td ROWSPAN="{len(expression)}" SIDES="L">{reference_line}</td>' if reference_line is not None or rule_name == 'tautologie' else ""

        tautologie_line = ""
        table_head = f'<tr><td COLSPAN="3" ALIGN="CENTER" SIDES="B">{rule_name}</td></tr>'
        if rule_name == 'tautologie':
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
        return self.graph.to_string()