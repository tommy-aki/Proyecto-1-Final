
import webview
from db.erd import gen_erd 
from mermaid import Mermaid 
from mermaid.graph import Graph 

def gen_erd_window(conexion, filename="er_diagram"): 
    fks, cols = gen_erd(conexion)
    mermaid_code = "erDiagram\n"
    for table_n, refs in cols.items():
        mermaid_code += f"    {table_n.upper()} " + "{\n"
        for ref in refs:
            type_ = ref['type']
            name = ref['name']
            mermaid_code += f"       {type_} {name}\n"
        mermaid_code += "    }\n"
    for _, refs in fks.items():
        for ref in refs:
            table = ref["table"]
            rtab = ref["rtab"]
            lcol = ref["lcol"]
            rcol = ref["rcol"]

            mermaid_code += f"    {table} ||--o" + "{ " + f"{rtab} : \"{lcol} → {rcol}\"\n"




    print(mermaid_code)

    html_content = f"""
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body>
        <div class="mermaid">
            {mermaid_code}
        </div>
    </body>
    </html>
    """


    webview.create_window("Diagrama ER", html=html_content)
    webview.start()