"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
render_chat = _module.render_chat
split_on_specials = _module.split_on_specials


def test_1_render_single_message():
    assert render_chat([{"role": "user", "content": "hi"}]) == "<|user|>\nhi<|end|>\n"


def test_2_render_with_generation_prompt():
    out = render_chat([{"role": "user", "content": "hi"}], add_generation_prompt=True)
    assert out.endswith("<|end|>\n<|assistant|>\n")


def test_3_render_keeps_message_order():
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}, {"role": "assistant", "content": "a"}]
    out = render_chat(msgs)
    assert out.index("<|system|>") < out.index("<|user|>") < out.index("<|assistant|>")


def test_4_split_hand_computed():
    assert split_on_specials("a<|end|>b", ["<|end|>"]) == ["a", "<|end|>", "b"]


def test_5_adjacent_specials_and_edges():
    assert split_on_specials("<|a|><|a|>x", ["<|a|>"]) == ["<|a|>", "<|a|>", "x"]
    assert split_on_specials("", ["<|a|>"]) == []


def test_6_longest_special_wins():
    specials = ["<|end|>", "<|end|>x"]
    assert split_on_specials("q<|end|>xz", specials) == ["q", "<|end|>x", "z"]


def test_7_pieces_reconstruct_text_and_input_untouched():
    specials = ["<|user|>", "<|end|>"]
    text = render_chat([{"role": "user", "content": "hello <|end|> world"}])
    snap = list(specials)
    assert "".join(split_on_specials(text, specials)) == text
    assert specials == snap
