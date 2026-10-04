import glob, json, math, os, re, zipfile
import numpy as np

ARCHIVE = '/home/aadityansha/Downloads/TrenTorch_250_Problemset_TestReady_v2.zip'
ROOT = 'TrenTorch_Web/data/app_data'
zip_file = zipfile.ZipFile(ARCHIVE)
configs = {}
for file_name in sorted(glob.glob('repair_config_*.json')):
    configs.update({int(k): v for k, v in json.load(open(file_name)).items()})

def normalize(value):
    if isinstance(value, np.ndarray): return normalize(value.tolist())
    if isinstance(value, np.generic): return normalize(value.item())
    if isinstance(value, (tuple, list)): return [normalize(v) for v in value]
    if isinstance(value, dict): return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return 'NaN' if math.isnan(value) else ('Infinity' if value > 0 else '-Infinity')
    return value

def render(value):
    if isinstance(value, list): return '[' + ', '.join(render(v) for v in value) + ']'
    if isinstance(value, dict): return '{' + ', '.join(repr(k) + ': ' + render(v) for k,v in value.items()) + '}'
    return repr(value)

def display(expr):
    expr = re.sub(r"\{'\$rng':\s*(\d+)\}", r'np.random.default_rng(\1)', expr)
    expr = re.sub(r"\{'\$quadratic':\s*True\}", 'lambda z: float(np.sum(np.asarray(z,dtype=float)**2))', expr)
    return expr

def runtime(value):
    if isinstance(value, dict) and set(value) == {'$rng'}: return np.random.default_rng(value['$rng'])
    if isinstance(value, dict) and set(value) == {'$quadratic'}: return lambda x: float(np.sum(np.asarray(x,dtype=float)**2))
    if isinstance(value, list): return [runtime(v) for v in value]
    if isinstance(value, dict): return {k:runtime(v) for k,v in value.items()}
    return value

def invoke_args(q, args):
    args = [runtime(v) for v in args]
    if q == 194: args = [np.asarray(args[0]), np.asarray(args[1])]
    elif q == 195: args = [np.asarray(v) for v in args]
    elif q == 230: args = [np.asarray(args[0]), np.asarray(args[1]), args[2]]
    elif q == 250: args = [args[0], np.asarray(args[1]), np.asarray(args[2]), args[3]]
    return args

def oracle(code):
    namespace = {'np':np, 'math':math}
    exec(compile(code, '<source-oracle>', 'exec'), namespace)
    return namespace['solve']

def make_tests(relative_path, q, calls, outputs):
    test_cases = '\n'.join(f'    ("example_{i+1}", {render(args)}, {render(output)}),' for i,(args,output) in enumerate(zip(calls,outputs)))
    return '''"""Question-specific tests with fixed expected values."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
_module = load_solution(''' + repr(relative_path) + ''')
solve = _module.solve
CASES = [
''' + test_cases + '''
]
def _build(value):
    if isinstance(value, dict) and set(value) == {"$rng"}: return np.random.default_rng(value["$rng"])
    if isinstance(value, dict) and set(value) == {"$quadratic"}: return lambda x: float(np.sum(np.asarray(x,dtype=float)**2))
    if isinstance(value, list): return [_build(v) for v in value]
    if isinstance(value, dict): return {k:_build(v) for k,v in value.items()}
    return value
def _assert_value(actual, expected):
    if isinstance(actual,(tuple,list)) and isinstance(expected,list):
        assert len(actual) == len(expected)
        for got,want in zip(actual,expected): _assert_value(got,want)
    elif isinstance(actual,dict): assert actual == expected
    elif isinstance(expected,list): np.testing.assert_allclose(np.asarray(actual),np.asarray(expected),rtol=1e-7,atol=1e-9)
    elif isinstance(expected,float): assert actual == pytest.approx(expected,rel=1e-7,abs=1e-9)
    else: assert actual == expected
@pytest.mark.parametrize("case,args,expected", CASES, ids=[row[0] for row in CASES])
def test_contract(case,args,expected):
    q = ''' + str(q) + '''
    args = _build(args)
    if q == 194: args=[np.asarray(args[0]),np.asarray(args[1])]
    elif q == 195: args=[np.asarray(x) for x in args]
    elif q == 230: args=[np.asarray(args[0]),np.asarray(args[1]),args[2]]
    elif q == 250: args=[args[0],np.asarray(args[1]),np.asarray(args[2]),args[3]]
    _assert_value(solve(*args),expected)
'''

source_dirs = {}
for name in zip_file.namelist():
    match = re.search(r'/([0-9]{3})-[^/]+/README\.md$', name)
    if match and int(match.group(1)) in configs: source_dirs[int(match.group(1))] = name.rsplit('/',1)[0]
folders = {}
for directory, children, _ in os.walk(ROOT):
    if os.path.basename(directory) == '98-authored-problemset':
        for child in children:
            match = re.match(r'(\d+)-', child)
            if match and int(match.group(1)) in configs: folders[int(match.group(1))] = os.path.join(directory, child)

for q, item in configs.items():
    path, src = folders[q], source_dirs[q]
    statement, theory, expressions = item['statement'], item['theory'], item['calls']
    solution = zip_file.read(src + '/solution.py').decode()
    starter = zip_file.read(src + '/starter.py').decode()
    starter = re.sub(r'("""|\'\'\').*?(\1)', '"""Implement the contract described in README.md."""', starter, count=1, flags=re.S)
    if 'pass' not in starter: starter = starter.rstrip() + '\n    # TODO: implement the contract described in README.md\n    pass\n'
    open(path + '/solution.py','w').write(solution.rstrip()+'\n')
    open(path + '/starter.py','w').write(starter.rstrip()+'\n')
    solve = oracle(solution)
    calls = [eval('[' + expression + ']', {'np':np}) for expression in expressions]
    outputs = [normalize(solve(*invoke_args(q,args))) for args in calls]
    old = open(path + '/README.md').read()
    frontmatter = re.match(r'\A---\n.*?\n---\n', old, re.S).group(0).rstrip()
    signature = re.search(r'^def solve\(.*$', starter, re.M).group(0).rstrip(':')
    examples = ''
    for i,(expr,output) in enumerate(zip(expressions,outputs),1):
        examples += f'\n### Example {i}\n\n```python\nsolve({display(expr)})\n```\n\nReturns:\n\n```python\n{render(output)}\n```\n'
    readme = frontmatter + '\n\n## Statement\n\n' + statement + '\n\nSignature: `' + signature + '`. Arguments are passed directly; return the stated value without printing.\n' + examples + '\n## Theory\n\n' + theory + '\n\n## Explanation\n\n' + statement + ' The examples show concrete inputs and expected returned values.\n'
    open(path + '/README.md','w').write(readme)
    relative = os.path.relpath(path, ROOT)
    open(path + '/tests.py','w').write(make_tests(relative,q,calls,outputs))
print(f'Repaired {len(configs)} folders / {4*len(configs)} authored files.')
