---
name: txf-llmeng-capstone-tiny-llm
title: 'Capstone: wire tokenization, embeddings, attention and the training loop into one tiny end-to-end LLM'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

This entire curriculum, from `[04-seq-modeling/01-tokenization]`'s very first question onward, has been building ONE thing, piece by independently-verified piece: a working language model. This capstone's job is to actually PROVE that, wiring the tokenizer, the embedding layer, the Transformer blocks, and the output-head training loop together into a single, genuinely runnable pipeline that trains on real text and generates new text, end to end, with nothing left as a disconnected piece.

Honest about scope: `[03-language-model-assembly/05-training-loop]` already explained WHY this capstone trains only the OUTPUT HEAD via real backpropagation (`[02-deep-learning-core/03-losses/02-cross-entropy]`'s gradient, `[03-dl-training/02-layers/02-linear-backward]`'s backward pass), treating the Transformer blocks' output as fixed, randomly-initialized features: this curriculum never built a backward pass for attention or the feed-forward sublayer, so full end-to-end backpropagation through the whole stack is genuinely out of scope. What this capstone DOES demonstrate, completely and correctly, is every OTHER piece of a real language model's lifecycle, working together on real text: tokenizing, building a vocabulary, embedding, running full Transformer blocks (forward), computing a real loss, taking real gradient steps that measurably reduce that loss, and generating genuinely novel text from the trained result.

### From theory to code

Implement `build_char_vocab`/`encode_char_text`/`decode_char_ids` (character-level tokenization, composing `[04-seq-modeling/01-tokenization]`'s pieces), `init_tiny_lm_params` (randomly initializing a small Transformer's weights), `compute_hidden_states` (`[03-language-model-assembly/04-full-forward-pass]`'s pipeline, minus the final output projection), and `train_tiny_char_lm`, wiring everything together: build a vocabulary, compute hidden states, train the output head (`[05-training-loop]`), and generate new text (`[07-greedy-decoding]`).

### Constraints

- Tokenization is CHARACTER-level (`char_tokenize`, not `whitespace_tokenize`): a small vocabulary size is essential for a genuinely tiny, fast-to-run demo model.
- `init_tiny_lm_params` initializes LayerNorm's `gamma` to `1` and `beta` to `0` (an untrained normalization layer should start as the identity transform, a real initialization convention, not an arbitrary choice), and every other weight matrix to small random values.
- `compute_hidden_states` stops BEFORE the output projection (`[04-full-forward-pass]`'s pipeline minus its last step), since `[05-training-loop]`'s `train_output_head` needs `hidden_states` as its own separate input.
- `train_tiny_char_lm` is fully deterministic given a fixed `seed`: identical inputs must always produce an identical trained model and identical generated text.

### Hints

<details>
<summary>Hint 1: Character-level tokenization</summary>

```python
def build_char_vocab(corpus_text):
    tokens = char_tokenize(corpus_text)
    return build_vocabulary([tokens], min_freq=1)
```

</details>

<details>
<summary>Hint 2: The full pipeline</summary>

```python
vocab = build_char_vocab(corpus_text)
token_ids = np.array([encode_char_text(corpus_text, vocab)])
embedding_table, blocks_params, output_weight = init_tiny_lm_params(len(vocab), d_model, d_ff, num_blocks, seed)

mask = build_causal_mask(token_ids.shape[-1])
hidden_states = compute_hidden_states(token_ids, embedding_table, blocks_params, num_heads, mask)
trained_output_weight, loss_history = train_output_head(hidden_states, token_ids, output_weight, lr, num_steps)

generated_ids = greedy_decode(token_ids, embedding_table, blocks_params, num_heads, tied=False, output_weight=trained_output_weight, num_new_tokens=num_generated_chars)
generated_text = decode_char_ids(generated_ids[0].tolist(), vocab)
```

</details>

## Theory

### The simple version

Every earlier question in this curriculum's Sequence Modeling and Transformers Parts was one instrument section rehearsing its own part in isolation: the tokenizer section, the embeddings section, the attention section, the training-loop section. This capstone is the full rehearsal, every section playing together on one real piece of music from start to finish, proving that what was individually correct also correctly PLAYS TOGETHER, not merely a collection of parts that happen to look right on their own.

### The formula

```
text -> char_tokenize -> vocabulary -> token ids
     -> embedding lookup + positional encoding
     -> Transformer blocks (forward, randomly initialized)
     -> [train the output head via real backprop, hidden states fixed]
     -> greedy-decode new characters
     -> decode back to text
```

### How PyTorch actually implements this

nanoGPT and similarly-scoped small, from-scratch LLM implementations run precisely this pipeline (tokenize, embed, Transformer blocks, loss, backward, optimizer step, generate) using `torch.nn` modules and full `autograd`-driven backpropagation through EVERY layer, not just the output head, a real capability this curriculum's own from-scratch NumPy implementation deliberately doesn't extend to, for the reasons `[05-training-loop]` already explained. Scaling this exact pipeline up (a larger vocabulary via `[01-tokenization]`'s BPE rather than raw characters, a much larger `d_model`/`num_blocks`, training on far more text, and genuine backpropagation through every layer) is, at a very real level, simply MORE of exactly what this capstone already demonstrates working correctly at small scale, not a fundamentally different process.

## Explanation

`train_tiny_char_lm` composes every piece this Part and the Sequence Modeling Part built: `build_char_vocab` and `encode_char_text` turn raw text into token ids using `[01-tokenization]`'s character tokenizer and vocabulary builder; `init_tiny_lm_params` randomly initializes an embedding table, a stack of Transformer block parameters, and an output projection; `compute_hidden_states` runs `[04-full-forward-pass]`'s embedding-and-Transformer-blocks pipeline (stopping short of the final projection); `train_output_head` (from `[05-training-loop]`) then takes real gradient-descent steps on the output projection specifically, using the ACTUAL cross-entropy loss on the ACTUAL corpus, genuinely reducing that loss over successive steps; and finally `greedy_decode` (from `[07-greedy-decoding]`), using the now-TRAINED output weights, generates new characters one at a time, decoded back to readable text via `decode_char_ids`. Every step in this chain reuses an already independently-verified piece from earlier in the curriculum; the capstone's entire contribution is proving they compose correctly into one genuine, working, if deliberately small and partially-scoped, language model.
