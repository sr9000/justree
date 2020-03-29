@echo off
if exist doc\ (
  rmdir /s /q doc\ || goto :error
)
pip3 uninstall --yes justree || goto :error
pip3 install . || goto :error
setlocal
  set SPHINX_APIDOC_OPTIONS=members,special-members
  sphinx-apidoc -f --full --separate --private -H justree -V 1.0 -R 1.0.0 -o doc ./justree ^
    justree/bfs.py ^
    justree/dfs.py ^
    justree/tools.py ^
    justree/tree_node.py
endlocal
pushd doc\ || goto :error
echo.>> conf.py
echo html_theme='bizstyle'>> conf.py
call make html
popd
goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
