"""Build the deployable PyGBag site with the tracked responsive template."""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "web" / "responsive.tmpl"


def main():
    command = [
        sys.executable,
        "-m",
        "pygbag",
        "--build",
        "--width",
        "1200",
        "--height",
        "700",
        "--template",
        str(TEMPLATE),
        str(PROJECT_ROOT),
    ]
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


if __name__ == "__main__":
    main()
