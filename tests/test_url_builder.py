from src.app import urlBuilder

def test_trace_url():
    trace = "dflkjsfjfdsjd"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    url = urlBuilder(trace, projectID)
    assert url == "https://api.usetrace.com/api/trace/dflkjsfjfdsjd/execute"

def test_tag_url_response():
    trace = "tag:regression"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    url = urlBuilder(trace, projectID)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all"

def test_tag_url_case_insensitivity():
    trace = "TAG:regression"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    url = urlBuilder(trace, projectID)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all"