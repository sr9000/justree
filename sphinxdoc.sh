#!/usr/bin env
sphinx-apidoc -f --full --separate -H justree -V 1.0 -R 1.0.0 -o ./doc ./justree
pushd doc
make html
popd
