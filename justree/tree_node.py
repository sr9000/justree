from typing import List


class TreeNode:
    _children: List['TreeNode']

    def __init__(self) -> None:
        self._children = []
