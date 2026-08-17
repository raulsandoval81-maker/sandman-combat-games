import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "web" / "responsive.tmpl"
BUILD_SCRIPT = PROJECT_ROOT / "web" / "build.py"


class WebPresentationTests(unittest.TestCase):
    def test_template_uses_contain_fit_and_safe_viewport(self):
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("viewport-fit=cover", template)
        self.assertIn("window.visualViewport", template)
        self.assertIn("Math.min(availableWidth / logicalWidth", template)
        self.assertIn('"--game-canvas-width"', template)
        self.assertIn('"--game-canvas-height"', template)
        self.assertIn("var(--game-canvas-width", template)
        self.assertIn("var(--game-canvas-height", template)
        self.assertIn("var(--game-canvas-left", template)
        self.assertIn("var(--game-canvas-top", template)
        self.assertIn("transform: translate(-50%, -50%) !important", template)
        canvas_css = re.search(
            r"canvas\.emscripten\s*\{(?P<rules>.*?)\}", template, re.DOTALL
        ).group("rules")
        self.assertNotRegex(canvas_css, r"(?m)^\s*width:\s*100%;")
        self.assertNotRegex(canvas_css, r"(?m)^\s*height:\s*100%;")

    def test_build_uses_tracked_template_and_logical_resolution(self):
        build_script = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('PROJECT_ROOT / "web" / "responsive.tmpl"', build_script)
        self.assertRegex(build_script, r'"--width",\s*"1200"')
        self.assertRegex(build_script, r'"--height",\s*"700"')


if __name__ == "__main__":
    unittest.main()
