"""Small offline CLI; evidence links are data and are never executed."""
import argparse
import json
import sys
from .store import InvalidStore, KINDS, digest, load, review_queue, review_report, schema, summarize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'summarize', 'review-queue', 'review-report', 'digest'):
        p = sub.add_parser(name)
        p.add_argument('store')
        if name == 'digest':
            p.add_argument('record')
        if name == 'review-queue':
            p.add_argument('--sample-percent', type=int, default=10)
        if name == 'review-report':
            p.add_argument('--limit', type=int, default=20)
    p = sub.add_parser('schema')
    p.add_argument('kind', choices=KINDS)
    args = parser.parse_args()
    try:
        if args.command == 'schema':
            result = schema(args.kind)
        else:
            db = load(args.store)
            if args.command == 'validate':
                result = {'valid': True, 'records': len(db)}
            elif args.command == 'digest':
                if args.record not in db:
                    raise InvalidStore(f'unknown record: {args.record}')
                result = {'record': args.record, 'sha256': digest(db[args.record])}
            elif args.command == 'summarize':
                result = [summarize(db, r) for r in db.values() if r['record_type'] == 'assessment']
            elif args.command == 'review-report':
                print(review_report(db, args.limit))
                return 0
            else:
                result = review_queue(db, args.sample_percent)
        print(json.dumps(result, indent=2))
    except (InvalidStore, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
