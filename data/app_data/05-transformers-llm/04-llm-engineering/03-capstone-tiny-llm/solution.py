import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

char_tokenize = load_solution("04-seq-modeling/01-tokenization/01-whitespace-char-tokenizer").char_tokenize
_vocab_module = load_solution("04-seq-modeling/01-tokenization/02-vocabulary-building")
build_vocabulary = _vocab_module.build_vocabulary
encode_with_unk = _vocab_module.encode_with_unk
build_inverse_vocab = load_solution("04-seq-modeling/01-tokenization/05-encode-decode-roundtrip").build_inverse_vocab

embedding_forward = load_solution("04-seq-modeling/02-embeddings/01-token-embedding-lookup").embedding_forward
sinusoidal_positional_encoding = load_solution(
    "04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding"
).sinusoidal_positional_encoding
combine_embeddings = load_solution("04-seq-modeling/02-embeddings/05-combine-token-positional-embeddings").combine_embeddings

stack_transformer_blocks = load_solution("05-transformers-llm/01-transformer-block/07-stack-blocks").stack_transformer_blocks
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask
train_output_head = load_solution("05-transformers-llm/03-language-model-assembly/05-training-loop").train_output_head
greedy_decode = load_solution("05-transformers-llm/03-language-model-assembly/07-greedy-decoding").greedy_decode


def build_char_vocab(corpus_text: str) -> dict[str, int]:
    tokens = char_tokenize(corpus_text)
    return build_vocabulary([tokens], min_freq=1)


def encode_char_text(text: str, vocab: dict[str, int]) -> list[int]:
    tokens = char_tokenize(text)
    return encode_with_unk(tokens, vocab)


def decode_char_ids(ids: list[int], vocab: dict[str, int]) -> str:
    inverse_vocab = build_inverse_vocab(vocab)
    return "".join(inverse_vocab[i] for i in ids)


def init_tiny_lm_params(vocab_size: int, d_model: int, d_ff: int, num_blocks: int, seed: int):
    rng = np.random.RandomState(seed)
    embedding_table = rng.randn(vocab_size, d_model) * 0.02
    blocks_params = []
    for _ in range(num_blocks):
        blocks_params.append(
            dict(
                weight_o=rng.randn(d_model, d_model) * 0.02,
                bias_o=np.zeros(d_model),
                ffn_weight1=rng.randn(d_ff, d_model) * 0.02,
                ffn_bias1=np.zeros(d_ff),
                ffn_weight2=rng.randn(d_model, d_ff) * 0.02,
                ffn_bias2=np.zeros(d_model),
                gamma1=np.ones(d_model),
                beta1=np.zeros(d_model),
                gamma2=np.ones(d_model),
                beta2=np.zeros(d_model),
            )
        )
    output_weight = rng.randn(vocab_size, d_model) * 0.02
    return embedding_table, blocks_params, output_weight


def compute_hidden_states(
    token_ids: np.ndarray, embedding_table: np.ndarray, blocks_params: list[dict], num_heads: int, mask: np.ndarray
) -> np.ndarray:
    seq_len = token_ids.shape[-1]
    d_model = embedding_table.shape[-1]

    token_embeddings = embedding_forward(token_ids, embedding_table)
    positional_embeddings = sinusoidal_positional_encoding(seq_len, d_model)
    x = combine_embeddings(token_embeddings, positional_embeddings)
    return stack_transformer_blocks(x, num_heads, blocks_params, mask=mask)


def train_tiny_char_lm(
    corpus_text: str,
    d_model: int,
    d_ff: int,
    num_heads: int,
    num_blocks: int,
    lr: float,
    num_steps: int,
    num_generated_chars: int,
    seed: int,
) -> dict:
    vocab = build_char_vocab(corpus_text)
    token_ids = np.array([encode_char_text(corpus_text, vocab)])

    embedding_table, blocks_params, output_weight = init_tiny_lm_params(len(vocab), d_model, d_ff, num_blocks, seed)

    mask = build_causal_mask(token_ids.shape[-1])
    hidden_states = compute_hidden_states(token_ids, embedding_table, blocks_params, num_heads, mask)

    trained_output_weight, loss_history = train_output_head(hidden_states, token_ids, output_weight, lr, num_steps)

    generated_ids = greedy_decode(
        token_ids, embedding_table, blocks_params, num_heads, tied=False, output_weight=trained_output_weight,
        num_new_tokens=num_generated_chars,
    )
    generated_text = decode_char_ids(generated_ids[0].tolist(), vocab)

    return dict(
        vocab=vocab,
        loss_history=loss_history,
        trained_output_weight=trained_output_weight,
        generated_text=generated_text,
    )
