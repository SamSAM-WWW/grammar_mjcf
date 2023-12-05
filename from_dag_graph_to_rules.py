from create_graphs_with_dag import create_graphs

graph_choose = 1


class Rule():
    def __init__(self):
        self.name_ = None
        self.lhs = None
        self.rhs = None
        self.common = None


def create_rule_from_graph(graph):
    '''
    Rule 类型是一个包含三个子图LHS、RHS、Common的class

    struct Rule {
    `name`
    
    Left-Hand Side (LHS) subgraph
    `Graph lhs_;`

    Right-Hand Side (RHS) subgraph
    `Graph rhs_;`

    Common subgraph
    `Graph common_;`
    };
    '''
    rule = Rule()
    rule.name = graph.name
    print("rule_name is",rule.name)

    # Graph must have subgraphs named "L" and "R"
    if 'L' not in graph.lr_subgraph or 'R' not in graph.lr_subgraph:
            raise RuntimeError("Graph must contain subgraphs named \"L\" and \"R\"")






    # Continue with the rest of the function...

    return rule




graphs = create_graphs(graph_choose)

graph_0 = graphs[0]
create_rule_from_graph(graph_0)