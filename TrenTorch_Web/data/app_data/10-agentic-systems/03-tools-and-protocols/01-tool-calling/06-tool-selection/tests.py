"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
rank_tools = _module.rank_tools
TOOLS = {
    "get_weather": "get the current weather forecast for a city",
    "send_email": "send an email message to a recipient",
    "search_web": "search the web for pages about a query",
    "create_invoice": "create an invoice for a customer with line items",
    "get_stock_price": "get the latest stock price for a ticker symbol",
}


def test_1_obvious_match_ranks_first():
    assert rank_tools("what is the weather forecast in Pune", TOOLS, 1) == ["get_weather"]
    assert rank_tools("email this message to my boss", TOOLS, 1) == ["send_email"]


def test_2_rare_words_beat_common_words():
    # "get" appears in several descriptions; "invoice" in one
    assert rank_tools("get an invoice", TOOLS, 1) == ["create_invoice"]


def test_3_top_k_limits_the_result_and_is_sorted_by_score():
    out = rank_tools("stock price ticker", TOOLS, 3)
    assert len(out) == 3 and out[0] == "get_stock_price"


def test_4_query_without_overlap_falls_back_to_name_order():
    assert rank_tools("zzz qqq", TOOLS, 5) == sorted(TOOLS)


def test_5_ties_are_broken_by_name():
    tools = {"b_tool": "alpha beta", "a_tool": "alpha beta"}
    assert rank_tools("alpha", tools, 2) == ["a_tool", "b_tool"]


def test_6_matches_an_independent_cosine_computation():
    import math
    tools = {"t1": "red apple", "t2": "green apple pie"}
    # N=2, df(apple)=2, df(red)=1, df(green)=1, df(pie)=1
    idf = lambda df: math.log(3 / (df + 1)) + 1
    q = {"red": idf(1), "apple": idf(2)}
    d1 = {"red": idf(1), "apple": idf(2)}
    d2 = {"green": idf(1), "apple": idf(2), "pie": idf(1)}
    cos = lambda a, b: sum(a[k] * b.get(k, 0) for k in a) / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))
    assert cos(q, d1) > cos(q, d2)
    assert rank_tools("red apple", tools, 2) == ["t1", "t2"]


def test_7_input_untouched_and_empty_toolset():
    snap = dict(TOOLS)
    rank_tools("weather", TOOLS)
    assert TOOLS == snap and rank_tools("anything", {}, 3) == []
