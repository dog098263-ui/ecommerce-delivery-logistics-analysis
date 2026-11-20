import json
with open('notebooks/02_carrier_analysis.ipynb','r',encoding='utf-8') as f:
    nb = json.load(f)
cells = nb['cells']
print(f'Total cells: {len(cells)}')
code_cells = [c for c in cells if c['cell_type']=='code']
last_ec = code_cells[-1]['execution_count']
print(f'Last exec count: {last_ec}')
errs = [c for c in code_cells if any(o.get('output_type')=='error' for o in c.get('outputs',[]))]
print(f'Cells with errors: {len(errs)}')
