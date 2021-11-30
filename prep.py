#!/usr/bin/env python3
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent

def _build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd", help="sub-command help")
    subparsers.required = True

    save_parser = subparsers.add_parser("save")
    save_parser.add_argument("--output-path", default=None)

    return parser


def save(output_path: str = None):
    svc = get_service()
    if output_path:
        bundle_path = Path(args.output_path)
        if not bundle_path.exists():
            bundle_path.mkdir()
        svc.save_to_dir(bundle_path)
    else:
        bundle_path = Path(svc.save())

    bundle_path = bundle_path / "NewsService"
    here = Path(__file__).resolve().parent


def get_service():
    from main import NewsService
    svc = NewsService()
    return svc


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    if args.subcmd == "save":
        save(args.output_path)
