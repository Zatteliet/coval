import argparse

from coval import scorer

parser = argparse.ArgumentParser()

parser.add_argument("--key_file")
parser.add_argument("--sys_file")
parser.add_argument("--np_only", default=False)
parser.add_argument("--remove_nested", default=False)
parser.add_argument("--keep_singletons", default=True)
parser.add_argument("--min_span", default=False)

args = parser.parse_args()

scorer.score(
    args.key_file,
    args.sys_file,
    np_only=args.np_only,
    remove_nested=args.remove_nested,
    keep_singletons=args.keep_singletons,
    min_span=args.min_span,
)
