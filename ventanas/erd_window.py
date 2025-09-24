from db.erd import gen_erd
from graphviz import Digraph

def gen_erd_window(conexion, filename="er_diagram.png"):
    dot = Digraph(comment = f"ERD para {conexion}", format = "png")
    dot.attr('node', shape='box')
    fks = gen_erd(conexion)
    for _, refs in fks.items():
        for ref in refs:
            table = ref["table"]
            rtab = ref["rtab"]
            label = f'{ref["lcol"]} → {ref["rcol"]}'
            dot.node(table)
            dot.node(rtab)
            dot.edge(table, rtab, label=label)

    dot.render(filename, cleanup=True)
    return filename