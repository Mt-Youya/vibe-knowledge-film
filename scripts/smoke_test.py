#!/usr/bin/env python3
"""Render a temporary 1.2s film, synthesize audio and inspect the encoded result.

Requires the full render environment (including ffprobe, supplied with ffmpeg).
Does not modify example films or keep generated media in the skill directory.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = """(function () {
  const K = VKit;
  VK.film({dur: 1.2, theme: 'night', meta: {title: 'Smoke test', drone: 0},
    draw(fr, t) {
      fr.circle(500 + 700 * VK.ss(t, 0, 1), 440, 75, {fill: '#64E3F6'});
      K.subs(fr, t, [{a: 0, b: 1.2, zh: '同一个球，从左边移到右边。'}], 'night');
      fr.sfx(0.2, 'tick', {pitch: 2});
    }
  });
})();
"""


def main():
    with tempfile.TemporaryDirectory(prefix="vibe film smoke ") as directory:
        project = Path(directory) / "film's project"
        def run(*args):
            subprocess.run([sys.executable, *map(str, args)], cwd=directory, check=True)
        run(ROOT / "scripts/new_film.py", project, "--world", "C")
        (project / "film.js").write_text(FILM, encoding="utf-8")
        renderer = ROOT / "engine/render.py"
        run(renderer, project, "--det")
        run(renderer, project, "--jobs", "2")
        run(renderer, project, "--events")
        run(ROOT / "engine/audio.py", project)
        video = project / "renders/final.mp4"
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                                "-of", "json", str(video)], capture_output=True, text=True, check=True)
        spec = json.loads(probe.stdout)
        v = next(stream for stream in spec["streams"] if stream["codec_type"] == "video")
        a = next(stream for stream in spec["streams"] if stream["codec_type"] == "audio")
        assert (v["width"], v["height"], v["r_frame_rate"]) == (1920, 1080, "30/1"), v
        assert v["codec_name"] == "h264" and a["codec_name"] == "aac", spec
        assert abs(float(spec["format"]["duration"]) - 1.2) < .15, spec
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
        print("PASS: deterministic 1080p/30fps H.264 + AAC; parallel render, events, audio, decode.")


if __name__ == "__main__":
    main()
