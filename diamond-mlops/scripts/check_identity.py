"""Accept only a non-root IAM user, as required by the Week 0 practical."""

import json
import re
import sys


def main():
    try:
        identity = json.load(sys.stdin)
        arn = identity["Arn"]
        if not isinstance(arn, str) or not re.fullmatch(
            r"arn:aws:iam::[0-9]{12}:user/[^\s]+", arn
        ):
            raise ValueError("Week 0 requires an IAM user; root and role identities fail.")
    except (ValueError, KeyError, TypeError) as exc:
        print(f"FAIL AWS identity: {exc}", file=sys.stderr)
        return 1
    print("PASS AWS identity: authenticated as an IAM user.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
