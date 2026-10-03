import os, json
try:
    pkg = json.load(open('frontend/package.json', 'r'))
    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
    print("Deps:", len(deps))
except Exception as e:
    print(e)
