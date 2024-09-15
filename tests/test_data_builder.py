from src.app import dataBuilder

trace = "fdkjsjfldsjfsdj"
trace_w_tag = "tag:runMe"

def test_basic_data_conditon():
    data = dataBuilder(trace, "http://localhost")
    assert data['reporters'][0]['webhook']['url'] == "http://localhost"

def test_basic_data_condition_does_not_include_tages():
    data = dataBuilder(trace, "http://localhost")
    assert 'tags' not in data

def test_basic_tag_case():
    data = dataBuilder(trace_w_tag, "http://localhost")
    assert 'tags' in data
    assert data['tags'][0] == "runMe"

def test_basic_tag_case_case_insensitive():
    data = dataBuilder("TAG:runMe", "http://localhost")
    assert 'tags' in data
    assert data['tags'][0] == "runMe"