"""Break Production, Own It.

One job: print the confession, exactly as an AI agent would blurt it
out the second production goes down. The program keeps the line in a
single constant, checks it against the 200-character gate, and drops
it into entry.txt as raw UTF-8 bytes, no trailing newline, so the file
holds the line and nothing else.
"""

from os import environ
from pathlib import Path

# The confession: 86 characters, first person, agent voice.
CONFESSION = (
    "I overwrote production with staging to fix one bug. "
    "The bug is gone. So is production."
)

LIMIT = 200


def confession() -> str:
    """Return the entry line, stripped, gated at 200 characters."""
    text = CONFESSION.strip()
    if not text:
        raise ValueError("entry line is empty")
    if len(text) > LIMIT:
        raise ValueError("entry line is over the 200-character gate")
    if "\n" in text or "\r" in text:
        raise ValueError("entry line must stay on one line")
    return text


def out_path() -> Path:
    """Resolve entry.txt: the harness dir when set, else /output."""
    folder = Path(environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def emit(text: str, path: Path) -> int:
    """Write the line, make it world-readable, read it back to prove it."""
    payload = text.encode("utf-8")
    path.write_bytes(payload)
    path.chmod(0o644)
    if path.read_bytes() != payload:
        raise ValueError("entry.txt on disk is not the entry line")
    return len(payload)


def run() -> int:
    text = confession()
    target = out_path()
    size = emit(text, target)
    print(f"wrote {size} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
