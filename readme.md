# Secformer paper experiments code
### Extends Multi-Protocol SPDZ [![Documentation Status](https://readthedocs.org/projects/mp-spdz/badge/?version=latest)](https://mp-spdz.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://dev.azure.com/data61/MP-SPDZ/_apis/build/status/data61.MP-SPDZ?branchName=master)](https://dev.azure.com/data61/MP-SPDZ/_build/latest?definitionId=7&branchName=master) [![Gitter](https://badges.gitter.im/MP-SPDZ/community.svg)](https://gitter.im/MP-SPDZ/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

# Notes
Please download the [MP-SPDZ Code](https://github.com/data61/MP-SPDZ) and configure the environment, and then put the secformer code into it.

# Step
1. ./compile.py -R 64 three
2. ./replicated-ring-party.x 0 three
3. ./replicated-ring-party.x 1 three
4. ./replicated-ring-party.x 2 three