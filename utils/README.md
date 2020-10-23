# Tree utils

Python 3.6 and above

## Visualization
We use a dotted-tree format to visualize the tree structures. The tree can be printed with the `dotted_tree.pretty_print_tree` function and we also provide a simple command to visualize the conversations and annotations in a json data file, e.g. `python dotted_tree.py test_dst.json --limit 50`.

## Evaluation
We use turn-level average exact match accuracy as the metric of dialog state prediction. To evaluate whether two trees result in an exact match, the `dotted_tree.pretty_print_tree` function (with default node sorting order) can be used to convert a tree node to a string, and make comparisons at the string level.
