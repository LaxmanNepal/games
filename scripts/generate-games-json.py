from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GAMES_DIR = ROOT / "games"
OUTPUT = ROOT / "data" / "games.json"


def read_meta(game_dir: Path, name: str, default: str = "") -> str:
    meta = game_dir / "game.json"
    if meta.exists():
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            value = data.get(name)
            if value is not None:
                return str(value)
        except (json.JSONDecodeError, OSError):
            pass
    return default


def title_from_id(game_id: str) -> str:
    return re.sub(r"[-_]+", " ", game_id).title()


def find_logo(game_dir: Path) -> str:
    preferred = ["logo.svg", "logo.webp", "logo.png", "logo.jpg", "logo.jpeg"]
    for filename in preferred:
        if (game_dir / filename).is_file():
            return f"games/{game_dir.name}/{filename}"
    return ""


def main() -> None:
    games = []
    if GAMES_DIR.exists():
        for game_dir in sorted(p for p in GAMES_DIR.iterdir() if p.is_dir()):
            index = game_dir / "index.html"
            if not index.exists():
                continue

            game_id = game_dir.name
            game = {
                "id": game_id,
                "name": read_meta(game_dir, "name", title_from_id(game_id)),
                "description": read_meta(game_dir, "description", "Play this game directly in your browser."),
                "category": read_meta(game_dir, "category", "Arcade"),
                "controls": read_meta(game_dir, "controls", "Keyboard · Touch"),
                "logo": find_logo(game_dir),
                "path": f"games/{game_id}/",
            }
            games.append(game)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({"games": games}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated {len(games)} games in {OUTPUT}")


if __name__ == "__main__":
    main()
