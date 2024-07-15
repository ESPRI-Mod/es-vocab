import es_vocab.db.cvs as cvs
import es_vocab.utils.settings as settings


def test_universe_and_project(caplog):
    caplog.clear()

    # Test universe parsing first and stop in any case of error to avoid side effects with project parsing.
    cvs.TERMS_OF_UNIVERSE = cvs._parse_terms_of_universe(settings.UNIVERSE_DIR_PATH)
    assert (cvs.TERMS_OF_UNIVERSE is not None) and (len(cvs.TERMS_OF_UNIVERSE) > 0)
    count_error_tags = caplog.text.count("ERROR")
    assert count_error_tags == 0

    cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS = cvs._parse_projects(settings.PROJECTS_PARENT_DIR_PATH)
    assert (cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS is not None) and (len(cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS) > 0)
    count_error_tags = caplog.text.count("ERROR")
    assert count_error_tags == 0
