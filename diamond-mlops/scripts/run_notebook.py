"""Execute the complete notebook in the project's environment and verify metrics."""

import json
import math
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "mae": 279.29262903257705,
    "rmse": 524.9243546483148,
    "r2": 0.982563973914643,
}


def main():
    if sys.version_info[:2] != (3, 12) or Path(sys.prefix).resolve() != ROOT / ".venv":
        raise RuntimeError("Run with this project's .venv/bin/python using Python 3.12.")
    import nbformat
    from nbclient import NotebookClient

    # The default Python kernel must resolve inside this project's environment.
    os.environ["PATH"] = str(ROOT / ".venv/bin") + os.pathsep + os.environ["PATH"]
    for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[variable] = "1"
    os.environ["LOKY_MAX_CPU_COUNT"] = "2"
    os.environ["MPLBACKEND"] = "Agg"
    notebook_path = ROOT / "notebooks/01_diamond_exploration.ipynb"
    output_dir = ROOT / "notebooks/executed"
    output_dir.mkdir(exist_ok=True)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(notebook_path.parent)}},
    )
    # Explicit argv avoids picking a user-installed kernel from another environment.
    client.create_kernel_manager()
    client.km.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    client.execute()
    nbformat.write(notebook, output_dir / notebook_path.name)
    metrics = json.loads((ROOT / "models/metrics.json").read_text())
    if (metrics["model"], metrics["seed"], metrics["n_test"]) != (
        "HistGradientBoosting", 42, 10755
    ):
        raise RuntimeError("Notebook model, seed, or holdout row count changed.")
    for key, expected in EXPECTED.items():
        if not math.isclose(metrics[key], expected, rel_tol=0, abs_tol=1e-9):
            raise RuntimeError(f"Notebook {key} changed: {metrics[key]!r}")
        print(f"{key.upper()}: {metrics[key]!r}")
    print("PASS notebook: every cell executed; diamond metrics match (absolute tolerance 1e-9).")


if __name__ == "__main__":
    main()
