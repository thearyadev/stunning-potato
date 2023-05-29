from indexer.indexer import build_url, extract_film_id
import pytest
from beartype.roar import BeartypeCallHintParamViolation

def test_build_url():
    assert build_url(123) == "https://hqporner.com/hdporn/123.html"
    assert build_url(-456) == "https://hqporner.com/hdporn/-456.html"
    assert build_url(0) == "https://hqporner.com/hdporn/0.html"
    assert build_url(987654321) == "https://hqporner.com/hdporn/987654321.html"
    assert build_url(-987654321) == "https://hqporner.com/hdporn/-987654321.html"

def test_extract_film_id():
    # Test with a simple URL
    assert extract_film_id("https://funstuff.com/hdfun/123.html") == 123

    # Test with a URL containing multiple numbers
    assert extract_film_id("https://funstuff.com/hdfun/456_789.html") == 456

    # Test with a URL containing no numbers
    with pytest.raises(AttributeError):
        extract_film_id("https://funstuff.com/hdfun/abc.html")
    # Test with a URL containing negative numbers
    assert extract_film_id("https://funstuff.com/hdfun/-987.html") == 987

    with pytest.raises(BeartypeCallHintParamViolation):
        extract_film_id(12)
    
    assert extract_film_id("https://funstuff.com/hdfun/askdljsad123zzas.html") == 123