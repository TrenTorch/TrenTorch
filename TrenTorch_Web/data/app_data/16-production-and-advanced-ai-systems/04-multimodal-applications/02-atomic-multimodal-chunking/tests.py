"""pytest data/app_data/16-production-and-advanced-ai-systems/04-multimodal-applications/02-atomic-multimodal-chunking/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

chunk_with_atomic_blocks = load_solution(
    f"16-production-and-advanced-ai-systems/04-multimodal-applications/{Path(__file__).resolve().parent.name}"
).chunk_with_atomic_blocks


def test_1_blocks_pack_greedily_up_to_max_size():
    blocks = [("a", 30), ("b", 30), ("c", 30)]
    assert chunk_with_atomic_blocks(blocks, max_chunk_size=70) == [["a", "b"], ["c"]]


def test_2_all_blocks_fit_in_one_chunk():
    blocks = [("a", 10), ("b", 10), ("c", 10)]
    assert chunk_with_atomic_blocks(blocks, max_chunk_size=100) == [["a", "b", "c"]]


def test_3_oversized_single_block_becomes_its_own_chunk():
    blocks = [("small", 10), ("huge_caption", 500), ("small2", 10)]
    result = chunk_with_atomic_blocks(blocks, max_chunk_size=100)
    assert result == [["small"], ["huge_caption"], ["small2"]]


def test_4_image_caption_never_split_even_when_it_would_overflow_current_chunk():
    blocks = [("para1", 40), ("image_caption", 40), ("para2", 40)]
    # after para1 (40), image_caption (40) would make 80 <= 100, fits;
    # then para2 (40) would make 120 > 100, so it starts a new chunk.
    result = chunk_with_atomic_blocks(blocks, max_chunk_size=100)
    assert result == [["para1", "image_caption"], ["para2"]]


def test_5_empty_blocks_returns_empty_list():
    assert chunk_with_atomic_blocks([], max_chunk_size=100) == []
