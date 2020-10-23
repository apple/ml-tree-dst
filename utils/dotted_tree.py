"""
Copyright (C) 2020 Apple Inc. All rights reserved.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Callable, List, Dict
from tree import TreeNode


def escape_node_name(node_name: str) -> str:
    """Escapes any special characters in an ontology node name"""
    return node_name.replace(r"|", r"\|").replace(r".", r"\.")


def unescape_node_name(node_name: str) -> str:
    """Unescapes any special characters in an ontology node name"""
    return node_name.replace(r"\|", r"|").replace(r"\.", r".")


def format_node_helper(
    path: List[TreeNode], indent_level: int, num_unprinted: int, format_node_name_fn: Callable
) -> str:
    """Node formatting helper for `pretty_print_tree`
    Formats a tree path, appropriately indented and already printed prefix omitted.
    Args:
        path: list of `TreeNode`s in path
        indent_level: indentation level. The number of whitespaces
                      is usually a mulple of this
        num_unprinted: number of path elements not already printed as a suffix
        format_node_name_fn: function called to format node name
    """
    msg = " " * (4 * indent_level)
    unprinted = path[-num_unprinted:]
    if len(unprinted) != len(path):
        msg += "."

    msg += ".".join([format_node_name_fn(node) for node in unprinted])
    return msg


def default_format_node(path: List[TreeNode], indent_level: int, num_unprinted: int) -> str:
    """Default node formatter for `pretty_print_tree`
    Delegates to `format_node_helper`, using the node name
    without any further formatting.
    """

    def format_name(node):
        return escape_node_name(str(node.name))

    return format_node_helper(path, indent_level, num_unprinted, format_name)


def pretty_print_tree(
    root_node: TreeNode, format_node_fn: Callable = default_format_node, sort_key: Callable = None
):
    """Transforms a boring data structure into a stunning string*
    *: Depends on your choice of formatting function
    Args:
        root_node: root `TreeNode`
        format_node_fn: node formatter, default is `default_format_node`
        sort_key: key function to customize the sort order, default is None
    Return:
        a pretty string
    """
    lines = []

    def go(node, prefix, prefix_num_unprinted, indent):
        # global msg
        path = prefix + [node]
        num_unprinted = prefix_num_unprinted + 1
        new_indent = indent

        if len(node.children) != 1:
            lines.append(format_node_fn(path, indent, num_unprinted))
            new_indent = indent + 1
            num_unprinted = 0

        for child_name in sorted(node.children.keys(), key=sort_key):
            go(node.children[child_name], path, num_unprinted, new_indent)

    go(root_node, [], 0, 0)
    return "\n".join(lines)


def debug_print(input_f: str, limit: int = 50) -> None:
    with open(input_f, "r") as f:
        for lid, line in enumerate(f.readlines()):
            if lid >= limit:
                break
            data = json.loads(line)
            print(f"********Conversation {lid+1}********")
            for tid, turn in enumerate(data["turns"]):
                print(f"***Turn {tid}***")
                utterance = turn["utterance"]
                print(f"Utterance: {utterance}")
                if tid > 0:
                    input_ds = pretty_print_tree(TreeNode.from_dict(turn["input_dialog_state"]))
                    print(f"Last dialog state:\n{input_ds}\n")
                    input_das = turn["input_system_acts"]
                    das = []
                    for da in input_das:
                        das.append(pretty_print_tree(TreeNode.from_dict(da["paths"])))
                    das = "\n".join(das)
                    print(f"Last system acts:\n{das}\n")
                target_ds = pretty_print_tree(TreeNode.from_dict(turn["target_dialog_state"]))
                print(f"Target dialog state:\n{target_ds}\n")
            print("********End of Conversation********")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    debug_print(args.input_file, args.limit)


if __name__ == "__main__":
    main()
