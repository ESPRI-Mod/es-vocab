import es_vocab.db.cvs as cvs
import es_vocab.utils.settings as settings
import os
from es_vocab.apps.validation import is_valid, is_valid_on_all
cvs.TERMS_OF_UNIVERSE = cvs._parse_terms_of_universe(settings.DATA_DESCRIPTORS_PARENT_DIR_PATH)


def test_unit_validation_match_term():
    # validation for matching term
    assert is_valid("ipsl",cvs.TERMS_OF_UNIVERSE["institution"]["ipsl"])
    assert not is_valid("ipsl_toto",cvs.TERMS_OF_UNIVERSE["institution"]["ipsl"])

    # validation for regex term 
    assert is_valid("f3",cvs.TERMS_OF_UNIVERSE["forcing_index"]["multiple_digit"])
    assert not is_valid("f3234c",cvs.TERMS_OF_UNIVERSE["forcing_index"]["multiple_digit"])

    # validation for a composite with a seperator
    assert is_valid("tavg-h02-hxy-x",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])
    assert is_valid("tsum-rho00p5-hys-tree",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])

    assert not is_valid("toto-h02-hxy-x",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])
    assert not is_valid("tavg-toto-hxy-x",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])
    assert not is_valid("tavg-h02-toto-x",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])
    assert not is_valid("tavg-h02-hxy-toto",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])

    assert is_valid("tsum-rho0p5-hys-tree",cvs.TERMS_OF_UNIVERSE["branded_label"]["label"])

def test_over_all_terms():

    assert is_valid_on_all("ipsl")["valid"]
    assert is_valid_on_all("tavg")["valid"]

    assert not is_valid_on_all("toto")["valid"]


