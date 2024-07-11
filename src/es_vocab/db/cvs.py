from pydantic import BaseModel

from es_vocab.db.parser import parse_terms_of_universe
from es_vocab.utils.constants import UNIVERSE_DIR_PATH

# [datadescriptor_name, dict[term id, term object]
TERMS_OF_UNIVERSE: dict[str, dict[str, BaseModel]] = parse_terms_of_universe(UNIVERSE_DIR_PATH)
