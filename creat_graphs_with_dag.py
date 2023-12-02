from DAG import DAG
dag = DAG(name="make_robot")
dag.add_node("a",info = {"sub":"L","infom":"222"})
dag.add_node("b")
dag.add_node("c")
dag.add_node("d")
dag.add_edge("a", "b", info = "a和b是第一条边")
dag.add_edge("a", "d")
dag.add_edge("b", "c")
print(dag.name)
graphs = []
graphs.append(dag)