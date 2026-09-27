"""Build the deployable PyGBag site with a branded Sandman startup shell."""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "web" / "responsive.tmpl"


def brand_generated_shell():
    candidates = [
        PROJECT_ROOT / "build" / "web" / "index.html",
        PROJECT_ROOT / "build" / "index.html",
    ]
    index_path = next((path for path in candidates if path.exists()), None)
    if not index_path:
        return

    html = index_path.read_text(encoding="utf-8")

    replacements = {
        'platform.document.body.style.background = "#7f7f7f"':
            'platform.document.body.style.background = "#05070c"',
        'msg  = "Ready to start ! Please click/touch page"':
            'msg  = "ENTER THE MAT · Tap to continue"',
        'background: green;\n            color: blue;':
            'background: rgba(8, 10, 15, .94);\n            color: #f5d76e;',
        '<div id="infobox">Loading, please wait ...</div>':
            '<div id="infobox">SANDMAN COMBAT GAMES · Preparing the mat…</div>',
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    html = html.replace(
        "#infobox {\n            position: fixed;",
        "#infobox {\n            position: fixed;\n            min-width: min(520px, calc(100vw - 48px));\n            text-align: center;\n            letter-spacing: .08em;\n            text-transform: uppercase;\n            border: 1px solid rgba(245, 215, 110, .45);\n            border-radius: 18px;\n            box-shadow: 0 24px 80px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.04);",
    )

    html = html.replace(
        "body {\n            font-family: arial;",
        "body {\n            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;",
    )

    html = html.replace(
        "background-color: #000;\n        }",
        "background:\n                radial-gradient(circle at 50% 18%, rgba(217, 181, 76, .11), transparent 34%),\n                radial-gradient(circle at 50% 78%, rgba(28, 43, 76, .28), transparent 42%),\n                linear-gradient(180deg, #080a10 0%, #030407 100%);\n        }",
        1,
    )

    index_path.write_text(html, encoding="utf-8")


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
    brand_generated_shell()


if __name__ == "__main__":
    main()
