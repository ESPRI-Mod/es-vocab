import es_vocab.db.cvs as cvs


def test_parse_terms_of_universe():
    assert (cvs.TERMS_OF_UNIVERSE is not None) and (len(cvs.TERMS_OF_UNIVERSE) > 0)


def test_parse_collections_of_project():
    assert (cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS is not None) and (len(cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS) > 0)
