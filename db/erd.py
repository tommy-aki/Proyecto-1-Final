from collections import defaultdict
import re
from db.querries import query


def gen_erd(conexion):
    table_cols, table_rows = query(conexion, f"SHOW FULL TABLES WHERE Table_type='BASE TABLE';")
    foraneas = defaultdict(list)
    columns = defaultdict(list)
    for row in table_rows:
        table_name = row[table_cols[0]]
        
        ddl_cols, ddl_rows = query(conexion, f"SHOW CREATE TABLE `{table_name}`")
        pattern = re.findall(r'CONSTRAINT\s+`?(\w+)`?\s+FOREIGN KEY\s+\((.*?)\)\s+REFERENCES\s+`?(\w+)`?\s+\((.*?)\)', ddl_rows[0][ddl_cols[1]])
        # print(pattern)
        for constraint, lcol, rtab, rcol in pattern:
            foraneas[constraint].append({
                "table" : table_name.replace('`', '').replace(' ', '_').upper(),
                "lcol": lcol.replace('`', '').replace(' ', '_'),
                "rtab" : rtab.replace('`', '').replace(' ', '_').upper(),
                "rcol":rcol.replace('`', '').replace(' ', '_')
                    })
        
        columns_cols, columns_rows = query(conexion, f"SHOW COLUMNS FROM `{table_name}`")
        for row in columns_rows:
            name = row[columns_cols[0]]
            type__ = row[columns_cols[1]].upper()
            if '(' in type__:
                type__, _ = type__.split('(', 1)
            columns[table_name].append({
                "type" : type__.replace(' ', '_'),
                "name" : name.replace(' ', '_')
            })
    
    return foraneas, columns

