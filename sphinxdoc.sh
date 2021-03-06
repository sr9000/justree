#!/usr/bin/env bash
set -e

if [[ -d ./doc ]]; then
  rm -r ./doc
fi
pip3 uninstall --yes justree
pip3 install .
SPHINX_APIDOC_OPTIONS=members,special-members \
    sphinx-apidoc -f --full --separate --private -H justree -V 1.0 -R 1.0.0 -o doc ./justree \
    justree/bfs.py \
    justree/dfs.py \
    justree/tools.py \
    justree/tree_node.py
pushd doc
echo "" >> conf.py
echo "html_theme='bizstyle'" >> conf.py
make html
popd
