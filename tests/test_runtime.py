"""Regression checks for safe initialization and trustworthy failure reporting."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


render = load_module("film_render", ROOT / "engine/render.py")
fonts = load_module("film_fonts", ROOT / "engine/get_fonts.py")


class RuntimeTests(unittest.TestCase):
    def initialize(self, project, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/new_film.py"), str(project), *args],
                              capture_output=True, text=True)

    def test_initialize_from_another_directory_and_protect_existing_files(self):
        with tempfile.TemporaryDirectory(prefix="vibe project ") as directory:
            project = Path(directory) / "new film"
            result = self.initialize(project, "--world", "b")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("theme: 'flat'", (project / "film.js").read_text())
            (project / "film.js").unlink()
            (project / "index.html").write_text("user page")
            result = self.initialize(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((project / "index.html").read_text(), "user page")
            self.assertFalse((project / "film.js").exists())
            result = self.initialize(project, "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("theme: 'night'", (project / "film.js").read_text())

    def test_invalid_options_do_not_create_project(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "invalid"
            for options in (("--world",), ("--world", "X"), ("--unknown",)):
                self.assertNotEqual(self.initialize(project, *options).returncode, 0)
                self.assertFalse(project.exists())

    def test_project_cannot_be_created_inside_skill(self):
        self.assertNotEqual(self.initialize(ROOT / "temporary-film").returncode, 0)
        self.assertFalse((ROOT / "temporary-film").exists())

    def test_failed_font_download_returns_failure_without_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(fonts, "FONTS", {"sample.ttf": "sample.ttf"}), \
                 patch.object(fonts.urllib.request, "urlopen", side_effect=OSError("offline")):
                self.assertEqual(fonts.download_fonts(Path(directory)), 1)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_determinism_mismatch_is_a_failure(self):
        page = Mock()
        page.evaluate.return_value = 1
        with patch.object(render, "with_page", side_effect=lambda project, fn: fn(page)), \
             patch.object(render, "shot", side_effect=[b"first", b"different"]):
            with self.assertRaises(SystemExit) as error:
                render.det(Path("unused"), n=1)
            self.assertEqual(error.exception.code, 1)

    def test_encoder_failure_is_propagated(self):
        page = Mock()
        page.evaluate.side_effect = [1, 30]
        encoder = Mock()
        encoder.wait.return_value = 1
        with patch.object(render, "with_page", side_effect=lambda project, fn: fn(page)), \
             patch.object(render.subprocess, "Popen", return_value=encoder), \
             patch.object(render, "shot", return_value=b"frame"):
            with self.assertRaises(subprocess.CalledProcessError):
                render.frames(Path("unused"), Path("out.mp4"))


if __name__ == "__main__":
    unittest.main()
