import argparse


parser = argparse.ArgumentParser(
    prog="tlp",
    description="CLI entrypoint for techroot lesson parsing and manifest generation.",
)

# Subcommands are intentionally kept minimal for now; extend here as new workflows
# (e.g. `build`, `validate`, `manifest`) are added.
parser.add_subparsers(dest="command")
