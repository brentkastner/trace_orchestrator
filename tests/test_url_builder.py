from src.app import urlBuilder

def test_trace_url_with_key():
    trace = "dflkjsfjfdsjd"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = "dasdw1dd1sd1d1ds1ddd1d11d"
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/trace/dflkjsfjfdsjd/execute?key=dasdw1dd1sd1d1ds1ddd1d11d"

def test_trace_url_without_secretKey():
    trace = "dflkjsfjfdsjd"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = None
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/trace/dflkjsfjfdsjd/execute"

def test_tag_url_response_with_secretKey():
    trace = "tag:sometag"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = "dasdw1dd1sd1d1ds1ddd1d11d"
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all?key=dasdw1dd1sd1d1ds1ddd1d11d"

def test_tag_url_response_without_secretKey():
    trace = "tag:regression"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = None
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all"

def test_tag_url_case_insensitivity_with_secretKey():
    trace = "TAG:regression"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = "dasdw1dd1sd1d1ds1ddd1d11d"
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all?key=dasdw1dd1sd1d1ds1ddd1d11d"

def test_tag_url_case_insensitivity_without_secretKey():
    trace = "TAG:regression"
    projectID = "ffdslkjfsifisfjsdilfjdsif"
    secretKey = None
    url = urlBuilder(trace, projectID, secretKey)
    assert url == "https://api.usetrace.com/api/project/ffdslkjfsifisfjsdilfjdsif/execute-all"