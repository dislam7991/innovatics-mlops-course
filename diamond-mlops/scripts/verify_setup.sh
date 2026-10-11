#!/usr/bin/env bash
# Three real checks. A failed prerequisite never becomes a passing setup.
set -uo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root" || exit 1
python="$project_root/.venv/bin/python"
failures=0

if [[ ! -x "$python" ]]; then
    echo 'FAIL: create the Python 3.12 .venv and install requirements.txt first.' >&2
    exit 1
fi

echo '[1/3] AWS IAM user identity'
if command -v aws >/dev/null 2>&1 && \
    AWS_PAGER='' AWS_CLI_AUTO_PROMPT=off aws sts get-caller-identity \
        --output json --no-cli-pager --cli-connect-timeout 10 --cli-read-timeout 20 | \
        "$python" scripts/check_identity.py; then
    :
else
    echo 'FAIL AWS: install AWS CLI v2 and configure your student IAM user credentials.' >&2
    failures=$((failures + 1))
fi

echo '[2/3] Docker hello-world'
if command -v docker >/dev/null 2>&1 && \
    docker run --rm hello-world@sha256:ec153840d1e635ac434fab5e377081f17e0e15afab27beb3f726c3265039cfff; then
    echo 'PASS Docker: hello-world completed.'
else
    echo 'FAIL Docker: start Docker Desktop and enable integration with your WSL2 distro.' >&2
    failures=$((failures + 1))
fi

echo '[3/3] Diamond notebook (full dataset; allow several minutes)'
if "$python" scripts/run_notebook.py; then
    :
else
    echo 'FAIL notebook: read the traceback and confirm the locked environment is installed.' >&2
    failures=$((failures + 1))
fi

if (( failures > 0 )); then
    echo "Setup incomplete: $failures of 3 checks failed." >&2
    exit 1
fi
echo 'Setup ready: all 3 checks passed.'
