from pathlib import Path

from es_vocab.db.parser import parse_terms_of_universe
from es_vocab.utils.constants import UNIVERSE_DIR_PATH


def test_parse_terms_of_universe():
    parse_terms_of_universe(Path(UNIVERSE_DIR_PATH))
