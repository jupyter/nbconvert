# Verify that the "all" reqs are in sync.
import sys

from tomli import load

with open("pyproject.toml", "rb") as fid:
    data = load(fid)

all_reqs = data["project"]["optional-dependencies"]["all"]
remaining_all = all_reqs.copy()
errors = []

for (key, reqs) in data["project"]["optional-dependencies"].items():
    if key == "all":
        continue
    for req in reqs:
        if req not in all_reqs:
            errors.append(req)
        elif req in remaining_all:
            remaining_all.remove(req)

if errors:
    print('Missing deps in "all" reqs:')
    print([e for e in errors])

if remaining_all:
    print('Reqs in "all" but nowhere else:')
    print([r for r in remaining_all])

if errors or remaining_all:
    sys.exit(1)
