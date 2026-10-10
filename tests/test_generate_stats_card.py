import importlib.util
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "generate_stats_card.py"
spec = importlib.util.spec_from_file_location("generate_stats_card", SCRIPT)
card = importlib.util.module_from_spec(spec)
spec.loader.exec_module(card)

STATS = {"user": "aayushpanda77", "repos": 7, "followers": 3, "stars": 12, "upstream_prs": 2}


def test_card_is_valid_svg():
    root = ET.fromstring(card.render_card(STATS))
    assert root.tag.endswith("svg")


def test_card_shows_every_number():
    text = card.render_card(STATS)
    for value in ("7", "3", "12", "2"):
        assert f">{value}</text>" in text


def test_user_name_is_escaped():
    text = card.render_card({**STATS, "user": "<script>"})
    assert "<script>" not in text
    ET.fromstring(text)  # still parses


def test_offline_main_writes_file(tmp_path, monkeypatch):
    out = tmp_path / "card.svg"
    monkeypatch.setattr(
        "sys.argv", ["x", "--user", "aayushpanda77", "--offline", "--out", str(out)]
    )
    card.main()
    assert out.read_text(encoding="utf-8").startswith("<svg")
