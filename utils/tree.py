"""
Copyright (C) 2020 Apple Inc. All rights reserved.
"""

import copy
from itertools import chain
from typing import Any, Dict, Hashable, Iterable, List, Union, TypeVar

NodeName = Union[int, str, float, bool]
SelfType = TypeVar("SelfType", bound="TreeNode")


class TreeNode:
    """A tree node with a name and optionally associated data
    Attributes:
        name: name of node
        children: a dict where keys are child names and values are
                  child nodes of type `TreeNode`
        data: a user-supplied data object. Defaults to an empty dict
    """

    name: NodeName
    # children: Dict[NodeName, SelfType]
    data: Dict[Hashable, Any]

    def __init__(
        self: SelfType, name: NodeName, child_list_or_map: Union[List, Dict] = None, data=None
    ):
        """Constructor
        Args:
            name: name of node
            child_list_or_map: children of this node. Can be given as a list
                               of `TreeNode`s, or a dictionary where the values
                               are `TreeNode`s, and the keys are the associated
                               node names. Optional
            data: optional dict of additional data (if representing a protobuf
                  node, the keys should correspond to attributes). Will be
                  initialised as an empty dictionary if not given
        """
        self.name = name
        self.children = self._children_to_map(child_list_or_map)
        self.data = {} if data is None else data

    def _children_to_map(self, children: Union[List, None, Dict]) -> Dict:
        """If the children are given in a list this method
        converts them into a dict"""

        if isinstance(children, list):
            return dict((child.name, child) for child in children)
        elif children is None:
            return {}
        else:
            return children

    def to_dict(self) -> Dict:
        """Converts a TreeNode into a dict
        Return:
            A nested dictionary structure representing the tree. For example :
            {'name' : 'Root',
             'children' : [ {
                                'name' : 'calendar'
                                'children' : [ ... ]
                            },
                            {
                                'name' : 'dialog'
                                'children' : [ .... ]
                            }]
            }
        """

        def go(node):
            children = [go(child) for child_name, child in node.children.items()]
            return {"name": node.name, "children": children}

        return go(self)

    @classmethod
    def from_dict(cls, tree_dict: Dict) -> "TreeNode":
        """Build a tree from a nested dictionary structure
        Args:
            tree_dict: nested dictionary, for example
            those produced by the to_dict method
        Return:
            a root TreeNode
        """

        def go(d):
            children = [go(child) for child in d["children"]]
            data = dict(d["data"]) if "data" in d else None
            return cls(d["name"], children, data=data)

        return go(tree_dict)

    def descendants(self: SelfType, include_self=False) -> Iterable[SelfType]:
        """Yield the descendants of this node
        Args:
            include_self: include current node as a descendant.
                          Defaults to `False`.
        Return:
            a generator for the descendant nodes
        """
        if include_self:
            yield (self)
        yield from chain.from_iterable(
            child.descendants(include_self=True) for child_name, child in self.children.items()
        )

    def dfs(self, prefix: List = None, include_self: bool = False) -> Iterable[List]:
        """Yield paths for descendants of this node
         as discovered in depth-first search (DFS).
        Path for a node is a list of TreeNode instances leading up to the node.
        The first element of the list is the TreeNode that `dfs` was invoked on
        and the last element is the node itself.
        For efficiency reasons the same list object is reused for the
        path in all yielded pairs. To preserve it a copy will need to be made.
        Args:
            include_self: include current node as a descendant.
                          Defaults to `False`.
            prefix: the nodes that have occurred before the current node
        Return:
            a generator for the descendent paths
        """

        p = prefix if prefix else []
        if include_self:
            yield p + [self]
        yield from chain.from_iterable(
            child.dfs(prefix=p + [self], include_self=True) for child in self.children.values()
        )

    def leaves(self: SelfType) -> List[SelfType]:
        """Yield all the leaves in the tree."""
        return [node for node in self.descendants(include_self=True) if len(node.children) == 0]

    def __copy__(self: SelfType) -> SelfType:
        """Copy subtree rooted at this node
        A shallow copy is made of the name and data of the node.
        shallow copy is recursively invoked on child nodes.
        Return:
            the shallow copy
        """
        clone = object.__new__(self.__class__)
        for member in dir(self):
            attribute = getattr(self, member)
            if callable(attribute) or member[:2] == "__":
                continue

            if member == "children":
                copied_value = {k: copy.copy(child) for k, child in attribute.items()}
                setattr(clone, member, copied_value)
            else:
                setattr(clone, member, attribute)
        return clone

    def __repr__(self):
        return "<TreeNode name={} with {} children>".format(self.name, len(self.children))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TreeNode):
            raise NotImplementedError(f"Comparing TreeNode to {type(other)}")
        return (
            self.name == other.name and self.children == other.children and self.data == other.data
        )

    def __hash__(self):
        raise TypeError("unhashable type: TreeNode")

    def canonicalise_order(self) -> None:
        """Recursively sort the child nodes in a consistent order.
        The structure is modified in place.
        """
        for child in self.children.values():
            child.canonicalise_order()

        self.children = {
            name: self.children[name]
            for name in sorted(self.children.keys(), key=lambda name: str(name))
        }
