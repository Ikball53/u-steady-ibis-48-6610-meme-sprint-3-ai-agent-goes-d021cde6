"""Meme Sprint 3 entry runner.

The meme artwork ships with this entry as a bundled PNG file.
This script simply places an exact copy of that artwork into the
output location the grader expects. No image processing happens
here, so nothing beyond the Python standard library is needed.
"""

from pathlib import Path


def locate_bundled_artwork() -> Path:
    # The artwork lives beside this script, wherever it is unpacked.
    script_folder = Path(__file__).resolve().parent
    return script_folder / "meme.png"


def publish_artwork() -> None:
    source_path = locate_bundled_artwork()
    artwork_bytes = source_path.read_bytes()

    # Guard against a truncated bundle: an empty file would grade
    # as a broken image, so fail loudly instead of copying nothing.
    if not artwork_bytes:
        raise ValueError(f"bundled artwork is empty: {source_path}")

    destination_path = Path("/output/entry.png")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_bytes(artwork_bytes)


if __name__ == "__main__":
    publish_artwork()
