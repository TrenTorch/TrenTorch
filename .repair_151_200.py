from pathlib import Path
import re

ROOT = Path("TrenTorch_Web/data/app_data")
SOURCE = Path("/home/aadityansha/Downloads/TrenTorch_250_Problemset_TestReady_v2")

SOLUTIONS = {
151: """import numpy as np

def solve(grads):
    \"\"\"Return the elementwise mean of equally shaped micro-batch gradients.\"\"\"
    if not grads:
        raise ValueError("grads must contain at least one micro-batch")
    arrays = [np.asarray(g, dtype=float) for g in grads]
    if any(g.shape != arrays[0].shape for g in arrays):
        raise ValueError("all gradients must have the same shape")
    return np.mean(np.stack(arrays, axis=0), axis=0)
""",
152: """def solve(backbone, head):
    \"\"\"Freeze backbone parameters and leave task-head parameters trainable.\"\"\"
    for parameter in backbone:
        parameter.requires_grad = False
    for parameter in head:
        parameter.requires_grad = True
    return list(backbone), list(head)
""",
153: """def solve(backbone, head, base_lr, backbone_factor):
    \"\"\"Build optimizer groups with a scaled backbone and base-rate head.\"\"\"
    return [
        {"params": list(backbone), "lr": base_lr * backbone_factor},
        {"params": list(head), "lr": base_lr},
    ]
""",
154: """import numpy as np

def solve(loss, scaled_grads, scale):
    \"\"\"Scale the loss and unscale each gradient using the same positive scale.\"\"\"
    if scale <= 0:
        raise ValueError("scale must be positive")
    return loss * scale, [np.asarray(g, dtype=float) / scale for g in scaled_grads]
""",
155: """import numpy as np

def solve(x):
    \"\"\"Compute log(sum(exp(x))) stably for a non-empty one-dimensional input.\"\"\"
    values = np.asarray(x, dtype=float)
    if values.size == 0:
        raise ValueError("x must not be empty")
    maximum = np.max(values)
    return float(maximum + np.log(np.exp(values - maximum).sum()))
""",
156: """import numpy as np

def solve(X, h0, Wx, Wh, b):
    \"\"\"Return tanh-RNN hidden states in input sequence order.\"\"\"
    hidden = np.asarray(h0, dtype=float)
    states = []
    for value in np.asarray(X):
        hidden = np.tanh(np.asarray(Wx) @ value + np.asarray(Wh) @ hidden + b)
        states.append(hidden.copy())
    return np.asarray(states)
""",
157: """import numpy as np

def solve(x, h, c, W, b):
    \"\"\"Apply one LSTM cell step and return its new hidden and cell states.\"\"\"
    gates = np.asarray(W) @ np.r_[x, h] + b
    i, f, o, g = np.split(gates, 4)
    sigmoid = lambda z: 1 / (1 + np.exp(-z))
    cell = sigmoid(f) * c + sigmoid(i) * np.tanh(g)
    return sigmoid(o) * np.tanh(cell), cell
""",
158: """import numpy as np

def solve(x, h, W, b, Wh, bh):
    \"\"\"Apply a GRU update using reset and update gates, then return the state.\"\"\"
    gates = np.asarray(W) @ np.r_[x, h] + b
    reset, update = np.split(gates, 2)
    sigmoid = lambda z: 1 / (1 + np.exp(-z))
    candidate = np.tanh(np.asarray(Wh) @ np.r_[x, sigmoid(reset) * h] + bh)
    return (1 - sigmoid(update)) * h + sigmoid(update) * candidate
""",
159: """import numpy as np

def solve(forward, backward):
    \"\"\"Concatenate forward and backward hidden states along the feature axis.\"\"\"
    forward = np.asarray(forward)
    backward = np.asarray(backward)
    if forward.shape[:-1] != backward.shape[:-1]:
        raise ValueError("forward and backward states must share leading dimensions")
    return np.concatenate((forward, backward), axis=-1)
""",
160: """import numpy as np

def solve(X, h0, Wx, Wh, b):
    \"\"\"Return the final hidden state after encoding X with a tanh RNN.\"\"\"
    hidden = np.asarray(h0, dtype=float)
    for value in np.asarray(X):
        hidden = np.tanh(np.asarray(Wx) @ value + np.asarray(Wh) @ hidden + b)
    return hidden
""",
161: """def solve(target, predicted, use_target):
    \"\"\"Choose the ground-truth token or model prediction for the next step.\"\"\"
    return target if use_target else predicted
""",
162: """def solve(step_scores, k):
    \"\"\"Return the top k token sequences and cumulative scores after all steps.\"\"\"
    if k <= 0:
        raise ValueError("k must be positive")
    beams = [((), 0.0)]
    for scores in step_scores:
        candidates = [
            (sequence + (token,), score + float(value))
            for sequence, score in beams
            for token, value in enumerate(scores)
        ]
        beams = sorted(candidates, key=lambda item: (-item[1], item[0]))[:k]
    return [(list(sequence), score) for sequence, score in beams]
""",
163: """def solve(beams, alpha):
    \"\"\"Select the beam maximizing score divided by length raised to alpha.\"\"\"
    if not beams:
        raise ValueError("beams must not be empty")
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    return max(beams, key=lambda item: (item[1] / max(1, len(item[0])) ** alpha, tuple(-x for x in item[0])))
""",
164: """import numpy as np

def solve(Q, K, V, mask=None):
    \"\"\"Compute scaled dot-product attention; True mask entries are allowed.\"\"\"
    Q, K, V = (np.asarray(value, dtype=float) for value in (Q, K, V))
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None:
        mask = np.asarray(mask, dtype=bool)
        scores = np.where(mask, scores, -np.inf)
    row_max = np.max(scores, axis=-1, keepdims=True)
    row_max = np.where(np.isfinite(row_max), row_max, 0)
    weights = np.exp(scores - row_max)
    denominator = weights.sum(axis=-1, keepdims=True)
    weights = np.divide(weights, denominator, out=np.zeros_like(weights), where=denominator != 0)
    return weights @ V
""",
165: """import numpy as np

def solve(Q, K, V, mask):
    \"\"\"Compute scaled dot-product attention over True (unmasked) key positions.\"\"\"
    Q, K, V = (np.asarray(value, dtype=float) for value in (Q, K, V))
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    allowed = np.asarray(mask, dtype=bool)
    scores = np.where(allowed, scores, -np.inf)
    row_max = np.max(scores, axis=-1, keepdims=True)
    row_max = np.where(np.isfinite(row_max), row_max, 0)
    weights = np.exp(scores - row_max)
    denominator = weights.sum(axis=-1, keepdims=True)
    weights = np.divide(weights, denominator, out=np.zeros_like(weights), where=denominator != 0)
    return weights @ V
""",
166: """import numpy as np

def solve(n):
    \"\"\"Return an n-by-n boolean causal mask allowing keys at or before each query.\"\"\"
    if n < 0:
        raise ValueError("n must be non-negative")
    return np.tril(np.ones((n, n), dtype=bool))
""",
167: """import numpy as np

def solve(weights, values):
    \"\"\"Return the weighted sum of value vectors for each query position.\"\"\"
    return np.asarray(weights) @ np.asarray(values)
""",
168: """import numpy as np

def solve(query, keys, Wq, Wk, v):
    \"\"\"Return additive-attention scores for one query against all key vectors.\"\"\"
    hidden = np.tanh(np.asarray(query) @ Wq + np.asarray(keys) @ Wk)
    return hidden @ np.asarray(v)
""",
169: """import numpy as np

def solve(ids, pad_id):
    \"\"\"Return a boolean attention mask that is False only at padding tokens.\"\"\"
    return np.asarray(ids) != pad_id
""",
170: """import numpy as np

def solve(sequences, pad_value=0):
    \"\"\"Right-pad variable-length sequences and return the padded batch and lengths.\"\"\"
    sequences = [list(sequence) for sequence in sequences]
    lengths = np.asarray([len(sequence) for sequence in sequences], dtype=int)
    width = int(lengths.max()) if len(lengths) else 0
    padded = np.full((len(sequences), width), pad_value)
    for row, sequence in enumerate(sequences):
        padded[row, :len(sequence)] = sequence
    return padded, lengths
""",
171: """import numpy as np

def solve(ids, pad_id):
    \"\"\"Return a 0/1 mask with one for each non-padding token.\"\"\"
    return (np.asarray(ids) != pad_id).astype(int)
""",
172: """import numpy as np

def solve(n, dim):
    \"\"\"Construct the standard alternating sine/cosine positional encoding.\"\"\"
    if n < 0 or dim <= 0:
        raise ValueError("n must be non-negative and dim must be positive")
    positions = np.arange(n)[:, None]
    dimensions = np.arange(dim)[None, :]
    rates = 1 / np.power(10000, (2 * (dimensions // 2)) / dim)
    angles = positions * rates
    encoding = np.empty((n, dim), dtype=float)
    encoding[:, 0::2] = np.sin(angles[:, 0::2])
    encoding[:, 1::2] = np.cos(angles[:, 1::2])
    return encoding
""",
173: """import numpy as np

def solve(embeddings, length):
    \"\"\"Return the first length rows of a learned positional-embedding table.\"\"\"
    table = np.asarray(embeddings)
    if length < 0 or length > len(table):
        raise ValueError("length must be within the embedding table")
    return table[:length].copy()
""",
174: """import numpy as np

def solve(lengths):
    \"\"\"Return exclusive cumulative offsets for concatenated variable-length rows.\"\"\"
    lengths = np.asarray(lengths, dtype=int)
    if np.any(lengths < 0):
        raise ValueError("lengths must be non-negative")
    return np.cumsum(np.r_[0, lengths[:-1]])
""",
175: """import numpy as np

def solve(embeddings, mask):
    \"\"\"Mean-pool unmasked token embeddings, returning zero for an empty row.\"\"\"
    values = np.asarray(embeddings, dtype=float)
    valid = np.asarray(mask, dtype=bool)[..., None]
    totals = np.sum(np.where(valid, values, 0), axis=1)
    counts = valid.sum(axis=1)
    return np.divide(totals, counts, out=np.zeros_like(totals), where=counts != 0)
""",
176: """from collections import Counter

def solve(tokens, k):
    \"\"\"Return the k most frequent tokens as (token, count) pairs.\"\"\"
    if k < 0:
        raise ValueError("k must be non-negative")
    counts = Counter(tokens)
    order = {token: index for index, token in enumerate(dict.fromkeys(tokens))}
    return sorted(counts.items(), key=lambda item: (-item[1], order[item[0]]))[:k]
""",
177: """def solve(tokens, vocab, unk_id):
    \"\"\"Map each token to its vocabulary ID, using unk_id for unseen tokens.\"\"\"
    return [vocab.get(token, unk_id) for token in tokens]
""",
178: """import numpy as np

def solve(X, n_heads):
    \"\"\"Split (batch, time, features) into (batch, heads, time, head_features).\"\"\"
    values = np.asarray(X)
    batch, time, features = values.shape
    if n_heads <= 0 or features % n_heads:
        raise ValueError("feature size must be divisible by positive n_heads")
    return values.reshape(batch, time, n_heads, features // n_heads).transpose(0, 2, 1, 3)
""",
179: """import numpy as np

def solve(heads):
    \"\"\"Merge (batch, heads, time, head_features) into feature-concatenated states.\"\"\"
    values = np.asarray(heads)
    batch, n_heads, time, width = values.shape
    return values.transpose(0, 2, 1, 3).reshape(batch, time, n_heads * width)
""",
180: """import numpy as np

def solve(x, sublayer):
    \"\"\"Apply a residual connection by adding the sublayer output to x.\"\"\"
    values = np.asarray(x)
    return values + np.asarray(sublayer(values))
""",
181: """import numpy as np

def solve(x, W1, b1, W2, b2):
    \"\"\"Apply a two-layer position-wise feed-forward network with ReLU.\"\"\"
    hidden = np.maximum(0, np.asarray(x) @ W1 + b1)
    return hidden @ W2 + b2
""",
182: """def solve(x, norm, attention, ff):
    \"\"\"Apply a pre-norm transformer block with attention and feed-forward residuals.\"\"\"
    first = x + attention(norm(x))
    return first + ff(norm(first))
""",
183: """def solve(x, norm, attention, ff):
    \"\"\"Apply a post-norm transformer block, normalizing after each residual sum.\"\"\"
    first = norm(x + attention(x))
    return norm(first + ff(first))
""",
184: """from collections import Counter

def solve(corpus):
    \"\"\"Return the most frequent adjacent token pair and its count.\"\"\"
    counts = Counter()
    for sequence in corpus:
        counts.update(zip(sequence, sequence[1:]))
    if not counts:
        raise ValueError("corpus must contain at least one adjacent token pair")
    first_seen = {}
    for sequence in corpus:
        for pair in zip(sequence, sequence[1:]):
            first_seen.setdefault(pair, len(first_seen))
    pair = min(counts, key=lambda item: (-counts[item], first_seen[item]))
    return pair, counts[pair]
""",
185: """def solve(seq, pair):
    \"\"\"Merge non-overlapping occurrences of an adjacent token pair from left to right.\"\"\"
    merged = []
    index = 0
    while index < len(seq):
        if index + 1 < len(seq) and tuple(seq[index:index + 2]) == tuple(pair):
            merged.append(seq[index] + seq[index + 1])
            index += 2
        else:
            merged.append(seq[index])
            index += 1
    return merged
""",
186: """def solve(pair_count, left_count, right_count):
    \"\"\"Compute the WordPiece pair score pair_count / (left_count * right_count).\"\"\"
    if left_count <= 0 or right_count <= 0:
        raise ValueError("token counts must be positive")
    return pair_count / (left_count * right_count)
""",
187: """import numpy as np

def solve(ids):
    \"\"\"Return next-token inputs and one-position-shifted targets.\"\"\"
    values = np.asarray(ids)
    return values[:-1], values[1:]
""",
188: """import numpy as np

def solve(ids, mask, ignore_index=-100):
    \"\"\"Keep original IDs and expose only selected positions as training labels.\"\"\"
    values = np.asarray(ids).copy()
    selected = np.asarray(mask, dtype=bool)
    labels = np.full(values.shape, ignore_index, dtype=np.result_type(values.dtype, type(ignore_index)))
    labels[selected] = values[selected]
    return values, labels
""",
189: """import numpy as np

def solve(mean_nll):
    \"\"\"Convert mean negative log-likelihood to perplexity with exp(mean_nll).\"\"\"
    return float(np.exp(mean_nll))
""",
190: """import numpy as np

def solve(logits, k, rng):
    \"\"\"Sample a token from the softmax distribution restricted to the top k logits.\"\"\"
    logits = np.asarray(logits, dtype=float)
    if not 1 <= k <= len(logits):
        raise ValueError("k must be between one and the vocabulary size")
    indices = np.argsort(-logits, kind="stable")[:k]
    shifted = logits[indices] - np.max(logits[indices])
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum()
    return int(rng.choice(indices, p=probabilities))
""",
191: """import numpy as np

def solve(logits, p_cut, rng):
    \"\"\"Nucleus-sample from the smallest descending-probability prefix reaching p_cut.\"\"\"
    logits = np.asarray(logits, dtype=float)
    if not 0 < p_cut <= 1 or logits.size == 0:
        raise ValueError("p_cut must be in (0, 1] and logits must be non-empty")
    shifted = logits - np.max(logits)
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum()
    order = np.argsort(-probabilities, kind="stable")
    cumulative = np.cumsum(probabilities[order])
    cutoff = np.searchsorted(cumulative, p_cut, side="left") + 1
    retained = order[:cutoff]
    selected = probabilities[retained]
    selected /= selected.sum()
    return int(rng.choice(retained, p=selected))
""",
192: """import numpy as np

def solve(logits, temperature):
    \"\"\"Return temperature-scaled softmax probabilities over logits.\"\"\"
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    values = np.asarray(logits, dtype=float) / temperature
    values -= values.max()
    probabilities = np.exp(values)
    return probabilities / probabilities.sum()
""",
193: """import numpy as np

def solve(logits):
    \"\"\"Return the index of the largest logit, choosing the first index on ties.\"\"\"
    return int(np.argmax(logits))
""",
194: """import numpy as np

def solve(cache, new_value):
    \"\"\"Append one new key/value position along the cache sequence axis (-2).\"\"\"
    return np.concatenate((np.asarray(cache), np.expand_dims(new_value, axis=-2)), axis=-2)
""",
195: """import numpy as np

def solve(x, A, B):
    \"\"\"Apply the low-rank adapter update B @ (A @ x).\"\"\"
    return np.asarray(B) @ (np.asarray(A) @ np.asarray(x))
""",
196: """def solve(in_features, out_features, r):
    \"\"\"Count trainable LoRA parameters for rank r: r times both matrix widths.\"\"\"
    if min(in_features, out_features, r) < 0:
        raise ValueError("feature counts and rank must be non-negative")
    return r * (in_features + out_features)
""",
197: """def solve(context_limit, prompt_tokens):
    \"\"\"Return remaining context capacity, floored at zero when the prompt is too long.\"\"\"
    return max(0, context_limit - prompt_tokens)
""",
198: """import numpy as np

def solve(labels):
    \"\"\"Return the most common label; ties resolve to the smallest sorted label.\"\"\"
    values, counts = np.unique(labels, return_counts=True)
    if values.size == 0:
        raise ValueError("labels must not be empty")
    return values[np.argmax(counts)]
""",
199: """import numpy as np

def solve(rewards):
    \"\"\"Return rewards standardized with the population mean and standard deviation.\"\"\"
    values = np.asarray(rewards, dtype=float)
    if values.size == 0:
        raise ValueError("rewards must not be empty")
    deviation = values.std()
    if deviation == 0:
        return np.zeros_like(values)
    return (values - values.mean()) / deviation
""",
200: """def solve(predictions, targets):
    \"\"\"Return exact-match accuracy after trimming surrounding whitespace.\"\"\"
    if len(predictions) != len(targets):
        raise ValueError("predictions and targets must have equal length")
    if not targets:
        raise ValueError("predictions and targets must not be empty")
    matches = [
        prediction.strip() == target.strip()
        if isinstance(prediction, str) and isinstance(target, str)
        else prediction == target
        for prediction, target in zip(predictions, targets)
    ]
    return sum(matches) / len(targets)
""",
}

DETAILS = {
151: ("Gradient Accumulation", "Average equally shaped gradient arrays from several micro-batches before an optimizer update.", "The average preserves the effective gradient scale of one combined batch. Stack each same-shaped array and reduce across the micro-batch axis.", "ḡ = (1/m) Σᵢ gᵢ", ["Check that every micro-batch contributes once.", "Reject an empty collection before dividing.", "Average elementwise across the leading stacked axis."], "Each gradient has at most 512 elements per axis; the number of micro-batches is 1–1024."),
152: ("Transfer Learning Freeze", "Freeze all backbone parameters while leaving the task-specific head trainable.", "Transfer learning reuses a pretrained feature extractor and updates a smaller prediction head. Set each parameter object's `requires_grad` flag according to its group.", "∂L/∂θ_backbone = 0; ∂L/∂θ_head is enabled", ["Iterate over the two groups independently.", "Backbone entries become non-trainable.", "Head entries remain trainable; return the groups as lists."], "The backbone and head each contain 0–10,000 parameter objects."),
153: ("Fine-Tuning Learning-Rate Groups", "Create separate optimizer groups for a pretrained backbone and a newly initialized head.", "A smaller learning rate limits destructive changes to pretrained features; the head can learn at the base rate.", "η_backbone = η_base × factor; η_head = η_base", ["Keep parameter membership in its original group.", "Multiply only the backbone learning rate by its factor.", "Return the two groups in backbone-then-head order."], "Learning rates are finite non-negative numbers; each group has at most 10,000 parameters."),
154: ("Mixed-Precision Loss Scale", "Scale a loss before backpropagation and undo that scale on supplied gradients.", "Loss scaling helps low-precision gradients avoid underflow. Gradients produced from the scaled loss must be divided by the same positive scale.", "L_scaled = sL; g = g_scaled / s", ["Use one shared positive scale.", "Multiply the scalar loss.", "Divide every gradient array elementwise by that scale."], "The scale is positive and at most 2²⁴; gradient arrays have at most 512 elements per axis."),
155: ("Stable LogSumExp", "Compute log(sum(exp(x))) without overflowing for large inputs.", "Subtracting the maximum leaves the result unchanged algebraically while bounding exponential arguments above by zero.", "log Σ exp(xᵢ) = m + log Σ exp(xᵢ − m), m=max(x)", ["Find the largest value first.", "Exponentiate the shifted values.", "Add the maximum back after taking the logarithm."], "Input is a non-empty vector of at most 100,000 finite values."),
156: ("Vanilla RNN Sequence", "Apply a tanh recurrent cell to every input vector and return every hidden state.", "Each time step combines the current input with the previous hidden state. The recurrence makes sequence order significant.", "hₜ = tanh(Wₓxₜ + Wₕhₜ₋₁ + b)", ["Initialize the state from h0.", "Update it once per input row.", "Append a copy after each update so later steps cannot alter earlier states."], "Sequence length is 1–10,000; input and hidden dimensions are at most 512."),
157: ("LSTM Cell", "Compute one LSTM cell update and return both hidden and cell state.", "The input, forget, output, and candidate gates control how information enters, persists in, and leaves the cell memory.", "c′ = σ(f)c + σ(i)tanh(g); h′ = σ(o)tanh(c′)", ["Multiply W by the concatenated input and previous hidden state.", "Split the result into four equal gates.", "Update c before computing h."], "Input and hidden vectors have dimensions at most 256; W has four hidden-size rows."),
158: ("GRU Cell", "Compute one gated recurrent unit update from input and previous hidden state.", "The reset gate controls candidate context; the update gate interpolates between old state and candidate.", "h′ = (1−z)h + z·tanh(Wₕ[x; r⊙h]+bₕ)", ["Compute reset and update gates from the concatenated state.", "Use the reset gate only in the candidate calculation.", "Interpolate candidate and old state with the update gate."], "Input and hidden vectors have dimensions at most 256; all gate matrices have compatible shapes."),
159: ("Bidirectional RNN Merge", "Concatenate forward and backward hidden features at every matching sequence position.", "The two directions encode past and future context. Joining on the final feature axis preserves all leading batch and time dimensions.", "Hₜ = [hₜ→ ; hₜ←]", ["Require matching batch/time dimensions.", "Do not reverse either input here; both arrays are already position-aligned.", "Concatenate along the last axis."], "The arrays have matching leading dimensions and feature widths of 1–512."),
160: ("Seq2Seq Encoder State", "Return the final hidden vector produced by a tanh RNN encoder.", "An encoder compresses its input sequence into the state after the last recurrent update.", "hₜ = tanh(Wₓxₜ + Wₕhₜ₋₁ + b); return hₜ at the final step", ["Start from h0.", "Apply the recurrence in the given order.", "Return the final state, not the full state sequence."], "The sequence length is 1–10,000; input and hidden dimensions are at most 512."),
161: ("Teacher Forcing Step", "Choose the next decoder input from the target token or the model prediction.", "Teacher forcing feeds the known next token during training; without it, generation feeds the model's own prediction.", "uₜ₊₁ = yₜ₊₁ if enabled, otherwise ŷₜ₊₁", ["Treat the flag as a selection, not a numeric blend.", "Return the original target object when enabled.", "Return the prediction when disabled."], "The target and prediction are single token IDs; the flag is boolean."),
162: ("Beam Search Top K", "Expand token sequences step by step and retain the k highest cumulative scores.", "Each active sequence branches over the next-step scores. Pruning after every step limits the search while cumulative log-scores rank candidates.", "score(y₁:ₜ) = Σⱼ log p(yⱼ | y₁:ⱼ₋₁)", ["Expand every current beam by every token.", "Add the new step score to its existing score.", "Sort by score and use token sequence order to break ties deterministically."], "There are 1–100 steps, 1–1,000 tokens per step, and 1 ≤ k ≤ 100."),
163: ("Length-Normalized Beam Search", "Choose the beam with the largest score after dividing by length raised to alpha.", "Length normalization reduces the preference for short sequences created by summing non-positive log probabilities.", "normalized_score = score / max(1, length)ᵅ", ["Compute one normalized score per beam.", "Treat an empty sequence as length one for the denominator.", "Return the original beam tuple with the best score."], "There are 1–10,000 beams; sequence lengths are at most 10,000 and alpha is non-negative."),
164: ("Scaled Dot-Product Attention", "Use query-key similarities to produce a weighted sum of value vectors.", "Scaling keeps dot products from growing with key dimension. A stable softmax converts scores into attention weights.", "Attention(Q,K,V)=softmax(QKᵀ/√dₖ)V", ["Compute the query-key matrix.", "Divide scores by square-root key width and normalize each row.", "Use the weights to combine V; a supplied mask marks allowed pairs."], "Query and key widths are equal and at most 512; there are at most 1,024 queries and keys."),
165: ("Masked Attention", "Compute attention while excluding key positions marked False by a boolean mask.", "Masking removes padding or otherwise invalid keys before softmax. Disallowed keys receive zero probability.", "Aᵢⱼ ∝ exp(sᵢⱼ) for allowed j; Aᵢⱼ=0 otherwise", ["Compute scaled dot-product scores.", "Set disallowed scores to negative infinity before normalization.", "An all-masked query returns a zero value vector."], "The mask is broadcastable to the query-key score shape; dimensions are at most 512."),
166: ("Causal Mask", "Build a boolean square mask that permits each position to attend to itself and earlier positions.", "Autoregressive models must not inspect future tokens. A lower triangle expresses the causal ordering.", "Mᵢⱼ = True iff j ≤ i", ["Create row and column position indices.", "Compare each key index to its query index.", "The diagonal is included; the result shape is n by n."], "0 ≤ n ≤ 4,096."),
167: ("Attention Weighted Sum", "Combine value vectors with already-computed attention weights.", "Attention weights specify the contribution of each value. Matrix multiplication reduces over the value-position axis.", "O = AV", ["Keep the weight and value-position axes aligned.", "Multiply weights by value vectors.", "Return one weighted feature vector per query."], "There are at most 1,024 queries and values; feature width is at most 512."),
168: ("Additive Attention Score", "Score each key by projecting a query and keys into a shared hidden space.", "Additive attention applies a learned nonlinearity to the sum of query and key projections, then projects that hidden vector to a scalar.", "eᵢ = vᵀ tanh(qWq + kᵢWk)", ["Project the query once and each key with its own matrix.", "Broadcast-add projections and apply tanh.", "Project each hidden vector onto v."], "There are 1–1,024 keys; input and hidden dimensions are at most 512."),
169: ("Attention Padding Mask", "Mark non-padding token IDs as valid attention positions.", "Padding is a batching convenience, not real content. A boolean mask prevents the model from attending to pad tokens.", "maskᵢ = (token_idᵢ ≠ pad_id)", ["Compare each ID with the padding ID.", "Keep the original sequence dimensions.", "Return booleans with True for real tokens."], "The ID sequence contains at most 100,000 integer tokens."),
170: ("Sequence Padding", "Right-pad a batch of variable-length token sequences and return their original lengths.", "Padding aligns sequence rows into a rectangular array while lengths retain the boundary between real tokens and padding.", "Pᵢⱼ = sequenceᵢⱼ when j < lengthᵢ, otherwise pad_value", ["Measure each sequence length.", "Allocate a rectangular array at the maximum length.", "Copy each sequence into the left side and return lengths alongside it."], "There are at most 1,024 sequences and each sequence has at most 10,000 tokens."),
171: ("Sequence Mask", "Create an integer mask identifying positions whose ID differs from the padding ID.", "The mask lets downstream sequence operations ignore padding without changing token IDs.", "maskᵢ = 1[idᵢ ≠ pad_id]", ["Compare each element to pad_id.", "Convert the boolean comparison to integers.", "Preserve the input shape."], "The input contains at most 100,000 integer IDs."),
172: ("Positional Encoding", "Construct sinusoidal positional vectors with alternating sine and cosine dimensions.", "Sinusoidal frequencies let a transformer distinguish token positions without learned position parameters.", "PE(pos,2i)=sin(pos/10000^(2i/d)); PE(pos,2i+1)=cos(pos/10000^(2i/d))", ["Compute the frequency assigned to every dimension pair.", "Multiply frequencies by each position.", "Apply sine to even columns and cosine to odd columns, including odd model widths."], "0 ≤ n ≤ 10,000; 1 ≤ dim ≤ 512."),
173: ("Learned Positional Embeddings", "Select the first requested number of rows from a learned position table.", "A learned table assigns one trainable vector to each position. The sequence uses rows in order from position zero.", "Pₜ = table[t], 0 ≤ t < length", ["Validate the requested length against the table.", "Select the leading rows without reordering.", "Return a copy so callers cannot mutate the input table through the result."], "The table has 1–10,000 rows and embedding width at most 512."),
174: ("Packed Sequence Lengths", "Compute starting offsets for sequences stored consecutively in a packed array.", "Exclusive prefix sums identify where each sequence begins; the initial offset is always zero.", "offsetᵢ = Σⱼ<ᵢ lengthⱼ", ["Start with offset zero.", "Add each earlier sequence length.", "Return one offset for each input length."], "There are at most 100,000 non-negative sequence lengths."),
175: ("Masked Mean Pooling", "Average only the token embeddings selected by a per-token mask.", "A masked mean excludes padding from both numerator and denominator; a row with no selected tokens maps to a zero vector.", "pooledᵢ = Σₜ maskᵢₜxᵢₜ / max(1, Σₜ maskᵢₜ)", ["Expand the mask over the feature axis.", "Sum selected vectors and count selected positions.", "Divide elementwise, returning zeros when a count is zero."], "Batch size and sequence length are at most 1,024; embedding width is at most 512."),
176: ("Vocabulary Frequency Count", "Return the k most frequent tokens and their counts, breaking ties by first appearance.", "A vocabulary can be built by counting token occurrences. Stable tie handling preserves the order in which tokens first entered the corpus.", "rank(token) = (−count(token), first_position(token))", ["Count each token occurrence.", "Record first appearance for tie-breaking.", "Sort by descending count and then first appearance; return at most k pairs."], "The token list has at most 100,000 items; 0 ≤ k ≤ 100,000."),
177: ("Unknown Token Mapping", "Convert tokens to IDs and map missing vocabulary entries to a supplied unknown ID.", "An unknown-token fallback ensures every input token can be represented even when absent from the training vocabulary.", "id(token) = vocab[token] if present, else unk_id", ["Look up each token independently.", "Do not alter known IDs.", "Use unk_id only for absent keys and preserve order."], "There are at most 100,000 tokens and vocabulary entries."),
178: ("Multi-Head Attention Split", "Reshape feature-concatenated states into separate attention heads.", "Each head receives a disjoint slice of the feature dimension. Transposing moves the head axis before time for attention computation.", "X(B,T,H·Dₕ) → (B,H,T,Dₕ)", ["Check that the feature width divides evenly by head count.", "Reshape the final axis into heads and per-head width.", "Transpose the head axis before the time axis."], "Batch, time, and feature dimensions are at most 512; head count is a positive divisor."),
179: ("Multi-Head Attention Merge", "Join per-head outputs back into one feature dimension.", "After attention, each head contributes its feature slice at every time step. Transpose time before heads, then flatten the last two axes.", "(B,H,T,Dₕ) → (B,T,H·Dₕ)", ["Move time before the head axis.", "Preserve each time position's head ordering.", "Flatten heads and their features into one final axis."], "Batch, head, time, and per-head dimensions are at most 512."),
180: ("Transformer Residual Block", "Add the output of a callable sublayer to its input.", "Residual paths preserve the original representation while allowing a sublayer to learn a refinement.", "y = x + sublayer(x)", ["Call the sublayer exactly once on x.", "Convert its result to an array.", "Add elementwise to the original input."], "Input contains at most 1,000,000 finite numeric values; output shape matches input."),
181: ("Transformer Feed-Forward", "Apply a position-wise two-layer network with ReLU between its affine transforms.", "The feed-forward sublayer expands and contracts each token representation independently.", "FFN(x)=max(0,xW₁+b₁)W₂+b₂", ["Compute the first affine transform.", "Clamp negative activations to zero.", "Apply the second affine transform and bias."], "Input width is at most 512 and hidden width at most 2,048."),
182: ("Pre-Norm Transformer Block", "Apply normalization before attention and feed-forward sublayers, each with a residual connection.", "Pre-norm places normalization inside each residual branch, helping gradients flow through deep transformer stacks.", "z=x+Attention(Norm(x)); y=z+FF(Norm(z))", ["Normalize x before attention.", "Add attention output to the unnormalized residual x.", "Normalize the intermediate result before the feed-forward residual."], "Input feature width is at most 512; each callable returns an array with the input shape."),
183: ("Post-Norm Transformer Block", "Apply attention and feed-forward residuals, normalizing after each addition.", "Post-norm normalizes each updated representation, placing normalization outside the residual branch.", "z=Norm(x+Attention(x)); y=Norm(z+FF(z))", ["Apply attention to x.", "Add its output and normalize the sum.", "Apply feed-forward to the normalized state, add, and normalize again."], "Input feature width is at most 512; each callable returns an array with the input shape."),
184: ("BPE Pair Counting", "Count adjacent token pairs across a corpus and return the most frequent pair and count.", "Byte-pair encoding repeatedly merges the most common adjacent pair. Pair counts are accumulated independently within each sequence.", "count(a,b)=Σ_sequences count of adjacent (a,b)", ["Count pairs without crossing sequence boundaries.", "Retain first-seen ordering for equal counts.", "Return the winning pair together with its frequency."], "There are at most 100,000 total tokens across 1–10,000 sequences."),
185: ("BPE Merge", "Merge every non-overlapping occurrence of one adjacent token pair.", "A single BPE merge scans left to right. Once a pair is combined, its tokens are not reused in another merge during that pass.", "ab a b → ab; otherwise copy the next token", ["Compare the next two tokens with the requested pair.", "On a match, concatenate and advance by two.", "Otherwise copy one token and advance by one."], "The sequence contains at most 100,000 string tokens."),
186: ("WordPiece Score", "Compute a pair association score from pair and individual token counts.", "The WordPiece score favors a pair that occurs often relative to the independent frequencies of its parts.", "score(a,b)=count(a,b)/(count(a)·count(b))", ["Require positive individual token counts.", "Multiply the left and right counts.", "Divide the pair count by that product."], "Counts are non-negative integers at most 10⁹; left and right counts are positive."),
187: ("Causal LM Shift", "Create next-token prediction inputs and targets by shifting token IDs by one position.", "At each position the model sees the prefix ending at the input token and predicts the following token.", "inputs=ids[:-1]; targets=ids[1:]", ["Keep all but the last ID as inputs.", "Keep all but the first ID as labels.", "Both outputs are one position shorter than ids."], "The token sequence contains 1–100,000 integer IDs."),
188: ("Masked LM Labels", "Keep original token IDs and place labels only at selected positions.", "Masked language modeling trains only on chosen token positions. All other labels receive the ignore index.", "labelᵢ = idᵢ if maskᵢ else ignore_index", ["Copy the input IDs.", "Initialize every label to ignore_index.", "Copy token IDs at True mask positions."], "IDs and mask have matching shapes with at most 100,000 positions."),
189: ("Perplexity From NLL", "Convert a mean negative log-likelihood into perplexity.", "Perplexity is the exponential of average negative log-likelihood and can be interpreted as an effective number of choices.", "PPL = exp(mean_nll)", ["Use the natural exponential.", "Do not exponentiate a sum when the input is already a mean.", "Return a scalar floating-point value."], "mean_nll is a finite real value in [0, 20]."),
190: ("Top-K Sampling", "Sample a token from the softmax probabilities of the k largest logits only.", "Top-k truncation sets aside all but k candidates before normalizing and sampling.", "pᵢ ∝ exp(logitᵢ) for i in top-k; pᵢ=0 otherwise", ["Find the k highest logits with stable tie order.", "Softmax only those logits for numerical stability.", "Pass the resulting probabilities and original token indices to rng.choice."], "The vocabulary has 1–100,000 logits and 1 ≤ k ≤ vocabulary size."),
191: ("Top-P Sampling", "Sample from the smallest high-probability token set whose cumulative probability reaches p_cut.", "Nucleus sampling adapts candidate count to the distribution's uncertainty rather than fixing k.", "retain the smallest prefix with Σpᵢ ≥ p_cut", ["Softmax all logits.", "Sort candidates by descending probability and accumulate mass.", "Include the token that reaches the threshold, renormalize, then sample."], "The vocabulary has 1–100,000 logits and 0 < p_cut ≤ 1."),
192: ("Temperature Sampling", "Return softmax probabilities after dividing logits by a positive temperature.", "Low temperatures sharpen a distribution; high temperatures flatten it. Subtracting the maximum stabilizes exponentiation.", "pᵢ = exp(zᵢ/T) / Σⱼ exp(zⱼ/T)", ["Divide every logit by temperature.", "Subtract the largest scaled logit.", "Exponentiate and normalize to sum to one."], "There are 1–100,000 finite logits; temperature is positive."),
193: ("Greedy Decoding", "Choose the first token index with the largest logit.", "Greedy decoding chooses the locally most likely next token without sampling or beam expansion.", "token = argmaxᵢ logitsᵢ", ["Compare logits directly; softmax is unnecessary.", "Use the first occurrence when maxima tie.", "Return the selected index as a Python integer."], "The vocabulary has 1–100,000 finite logits."),
194: ("KV Cache Append", "Append one position along the sequence axis of a key/value cache.", "A cache stores prior key/value vectors so autoregressive decoding need not recompute them. Sequence is the penultimate axis.", "cache′ = concat(cache, expand_dims(new_value, axis=−2), axis=−2)", ["Insert a length-one sequence axis into new_value.", "Keep every cache prefix unchanged.", "Concatenate on the penultimate axis."], "Cache rank is at least two; all dimensions except sequence length match."),
195: ("LoRA Update", "Apply the low-rank adapter transformation to an input vector.", "LoRA represents a weight update as a product of two narrow matrices, avoiding a full dense update.", "Δy = B(Ax)", ["Project x through A.", "Project the low-dimensional result through B.", "Do not add a base-model output; this function returns only the adapter update."], "The rank is 1–256; matrix shapes are compatible with x."),
196: ("LoRA Parameter Count", "Count trainable parameters in the two low-rank matrices.", "For input width d_in, output width d_out, and rank r, A has r·d_in values and B has d_out·r.", "count = r·(d_in+d_out)", ["Count A's parameters.", "Count B's parameters.", "Add both counts; do not count frozen base weights."], "Input/output widths are 0–1,000,000; rank is 0–min(widths)."),
197: ("Prompt Token Budget", "Compute how many tokens remain for a response after accounting for a prompt.", "The response budget cannot be negative, even when the prompt already exceeds the context limit.", "remaining = max(0, context_limit − prompt_tokens)", ["Subtract prompt tokens from the context limit.", "Clamp negative results to zero.", "Return the remaining integer budget."], "Token counts are non-negative integers at most 10⁷."),
198: ("In-Context Majority Vote", "Return the most frequent label, choosing the smallest label if counts tie.", "Multiple demonstrations or sampled answers can be aggregated by majority vote. A fixed tie rule makes the result deterministic.", "label* = argmax_label count(label)", ["Count labels.", "Choose the largest count.", "Because unique labels are sorted, select the smallest tied label."], "There are 1–100,000 integer or string labels."),
199: ("RLHF Reward Normalization", "Standardize reward values using their population mean and standard deviation.", "Reward normalization gives a batch zero mean and unit variance; a constant batch maps to all zeros to avoid division by zero.", "zᵢ=(rᵢ−μ)/σ; if σ=0, zᵢ=0", ["Compute the batch mean and population standard deviation.", "Subtract the mean from each reward.", "Divide by σ, or return zeros for a constant batch."], "There are 1–100,000 finite rewards."),
200: ("Benchmark Accuracy", "Compute exact-match accuracy after trimming surrounding whitespace from string values.", "Accuracy is the fraction of predictions equal to their corresponding targets. A length mismatch is invalid rather than silently truncating the comparison.", "accuracy = matching pairs / number of targets", ["Compare predictions and targets pairwise.", "For strings, ignore surrounding whitespace only.", "Divide the number of matches by the non-empty target count."], "Predictions and targets have equal non-zero length of at most 100,000."),
}

def main():
    folders = {}
    for number in range(151, 201):
        matches = list(ROOT.glob(f"**/{number:03d}-problem-*"))
        assert len(matches) == 1, (number, matches)
        folder = matches[0]
        source_matches = list(SOURCE.glob(f"**/{number:03d}-problem-*"))
        assert len(source_matches) == 1, (number, source_matches)
        source = source_matches[0]
        for filename in ("README.md", "starter.py", "solution.py", "tests.py"):
            assert (source / filename).is_file() and (folder / filename).is_file()
            (source / filename).read_text(encoding="utf-8")
            (folder / filename).read_text(encoding="utf-8")
        folders[number] = folder
        solution = SOLUTIONS[number]
        (folder / "solution.py").write_text(solution, encoding="utf-8")
        function = re.search(r"^def solve\(.*?^\s{4}\"\"\".*?^\s{4}\"\"\"",
                             solution, re.M | re.S)
        if function:
            starter = function.group(0) + "\n    pass\n"
        else:
            signature = re.search(r"^def solve\(.*\):", solution, re.M).group(0)
            doc = re.search(r'^\s{4}\"\"\".*?\"\"\"', solution, re.M | re.S)
            starter = f"{signature}\n    {doc.group(0).strip() if doc else '\"\"\"Implement the stated operation.\"\"\"'}\n    pass\n"
        imports = "\n".join(line for line in solution.splitlines() if line.startswith("import ") or line.startswith("from "))
        (folder / "starter.py").write_text((imports + "\n\n" if imports else "") + starter, encoding="utf-8")
        title, statement, theory, formula, hints, constraints = DETAILS[number]
        old = (folder / "README.md").read_text(encoding="utf-8")
        front = old.split("---", 2)[1]
        front = re.sub(r"(?m)^difficulty:.*$", f"difficulty: {'Beginner' if number in {151, 152, 161, 166, 169, 171, 174, 176, 177, 186, 187, 189, 193, 196, 197, 198, 200} else ('Advanced' if number in {157, 158, 162, 164, 165, 168, 172, 178, 179, 181, 182, 183, 190, 191, 199} else 'Intermediate')}", front)
        front = re.sub(r"(?m)^kind:.*$", "kind: problemset", front)
        front = re.sub(r"(?m)^caseCompany:.*\\n?", "", front)
        front = re.sub(r"(?m)^company:.*\\n?", "", front)
        frontmatter = "---" + front.strip() + "\n---\n"
        tags = re.search(r"(?m)^tags:.*$", front)
        if tags is None:
            frontmatter = frontmatter.replace("kind: problemset\n", "kind: problemset\ntags: [problemset]\n")
        else:
            tagline = tags.group(0)
            vals = re.findall(r"[\w-]+", tagline.split(":", 1)[1])
            vals = [v for v in vals if v.lower() not in {"company", "casecompany"}]
            if "problemset" not in vals:
                vals.append("problemset")
            frontmatter = re.sub(r"(?m)^tags:.*$", "tags: [" + ", ".join(vals) + "]", frontmatter)
        examples = EXAMPLES[number]
        rendered = [
            frontmatter,
            f"\n## Statement\n\n{statement}\n\n",
            "### Input Format\n\nCall the function directly with Python arguments; there is no stdin or stdout parsing.\n\n```python\nsolve" + examples[0][0] + "\n```\n\n",
            "### Output Format\n\nReturn the computed Python value; do not print it.\n\n",
            "### Constraints\n\n- " + constraints + "\n- All numeric inputs are finite unless a specific boundary is stated.\n- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).\n\n",
            "### Examples\n\n"
        ]
        for index, (call, output, explanation) in enumerate(examples, 1):
            rendered.append(f"**Example {index}**\n\n**Input**\n\n```python\nsolve{call}\n```\n\n**Output**\n\n```text\n{output}\n```\n\n{explanation}\n\n")
        rendered.append("### Hints\n\n")
        for i, hint in enumerate(hints, 1):
            rendered.append(f"<details><summary>Hint {i}</summary>\n\n{hint}\n\n</details>\n\n")
        rendered.extend([
            f"## Theory\n\n### Core idea\n\n{theory}\n\n### Mathematical contract\n\n`{formula}`\n\n",
            f"## Explanation\n\n{statement} The implementation follows the contract step by step and returns the requested value without printing. Its behavior on the worked examples follows directly from the formula above.\n"
        ])
        (folder / "README.md").write_text("".join(rendered), encoding="utf-8")

    print(f"Updated {len(folders)} question folders.")

# Each entry contains (function-call arguments, verified output, short worked explanation).
EXAMPLES = {
151: [("([[1.0, 3.0], [3.0, 5.0]])", "[2.0, 4.0]", "Each coordinate is averaged independently."),
      ("([[2.0, -2.0], [4.0, 0.0], [6.0, 2.0]])", "[4.0, 0.0]", "The three gradients sum to [12, 0] and are divided by three.")],
152: [("([p0, p1], [p2])", "([p0, p1], [p2])", "Both backbone parameters are frozen; the head parameter stays trainable."),
      ("([p0], [p1, p2])", "([p0], [p1, p2])", "The function preserves group membership while setting trainability flags.")],
153: [("([\"backbone\"], [\"head\"], 0.01, 0.1)", "[{'params': ['backbone'], 'lr': 0.001}, {'params': ['head'], 'lr': 0.01}]", "The backbone receives one tenth of the base rate."),
      ("([], [\"classifier\"], 0.2, 0.25)", "[{'params': [], 'lr': 0.05}, {'params': ['classifier'], 'lr': 0.2}]", "An empty backbone group is valid; the head retains the base rate.")],
154: [("(2.0, [[8.0, -4.0], [2.0]], 4.0)", "(8.0, [[2.0, -1.0], [0.5]])", "The loss is multiplied by four and each gradient is divided by four."),
      ("(-1.5, [[0.0, 6.0]], 2.0)", "(-3.0, [[0.0, 3.0]])", "Scaling applies equally to negative loss and each gradient coordinate.")],
155: [("([0.0, 0.0])", "0.6931471805599453", "The logarithm of two unit exponentials is log(2)."),
      ("([1000.0, 1000.0])", "1000.6931471805599", "Subtracting 1000 keeps exponentiation finite.")],
156: [("([[1.0], [0.0]], [0.0], [[1.0]], [[1.0]], [0.0])", "[[0.7615941559557649], [0.6420149920119997]]", "The second state uses tanh(1 × 0 + 1 × h₁)."),
      ("([[0.0]], [0.5], [[2.0]], [[0.0]], [0.0])", "[[0.7615941559557649]]", "The single step returns tanh(1), since the weighted input is one.")],
157: [("([0.0], [0.0], [0.0], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [0.0, 0.0, 0.0, 0.0])", "([0.0], [0.0])", "Zero gates keep the cell and hidden states at zero."),
      ("([1.0], [0.0], [0.0], [[0.0, 0.0]] * 4, [0.0, 0.0, 0.0, 0.0])", "([0.0], [0.0])", "With zero gate activations, the candidate is zero and no memory is added.")],
158: [("([0.0], [0.0], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0])", "[0.0, 0.0]", "Zero gates and candidate leave the zero hidden state unchanged."),
      ("([1.0], [2.0], [[0.0, 0.0]] * 2, [0.0, 0.0], [[0.0, 0.0]] * 2, [0.0, 0.0])", "[1.0, 1.0]", "A zero update gate interpolates halfway because sigmoid(0) is one half.")],
159: [("([[1, 2], [3, 4]], [[5], [6]])", "[[1, 2, 5], [3, 4, 6]]", "Features from both directions are joined position by position."),
      ("([[[1], [2]]], [[[3, 4], [5, 6]]])", "[[[1, 3, 4], [2, 5, 6]]]", "The batch and time axes are preserved while features concatenate.")],
160: [("([[1.0], [0.0]], [0.0], [[1.0]], [[1.0]], [0.0])", "[0.6420149920119997]", "After two updates, the encoder returns the second hidden state."),
      ("([[0.0]], [0.5], [[2.0]], [[0.0]], [0.0])", "[0.7615941559557649]", "The final state is tanh(1).")],
161: [("(42, 7, True)", "42", "With teacher forcing enabled, the target token is selected."),
      ("(42, 7, False)", "7", "Without teacher forcing, the predicted token is selected.")],
162: [("([[0.0, -1.0], [-0.2, -0.1]], 2)", "[([1, 1], -1.1), ([0, 1], -0.1)]", "The surviving sequences have the two highest cumulative scores."),
      ("([[0.0, 0.0]], 1)", "[([0], 0.0)]", "Equal scores use ascending token sequence order.")],
163: [("([([1, 2], -2.0), ([3], -1.5)], 1.0)", "([3], -1.5)", "The one-token beam has the higher normalized score."),
      ("([([0, 1], -4.0), ([2, 3], -2.0)], 0.0)", "([2, 3], -2.0)", "With alpha zero, the raw score determines the winner.")],
164: [("([[1.0]], [[1.0], [0.0]], [[2.0], [4.0]])", "[[2.5378828427399904]]", "The first key has greater score, so its value dominates."),
      ("([[0.0]], [[0.0], [0.0]], [[2.0], [4.0]])", "[[3.0]]", "Equal scores give equal attention to the two values.")],
165: [("([[0.0]], [[0.0], [0.0]], [[2.0], [4.0]], [True, False])", "[[2.0]]", "The false mask excludes the second value."),
      ("([[1.0]], [[1.0], [0.0]], [[2.0], [4.0]], [False, True])", "[[4.0]]", "Only the second key is allowed.")],
166: [("(3)", "[[True, False, False], [True, True, False], [True, True, True]]", "Each row admits only positions up through its diagonal."),
      ("(1)", "[[True]]", "A one-position sequence can attend to itself.")],
167: [("([[0.25, 0.75]], [[2.0], [6.0]])", "[[5.0]]", "The weighted value is 0.25×2 + 0.75×6."),
      ("([[1.0, 0.0], [0.0, 1.0]], [[3.0, 4.0], [5.0, 6.0]])", "[[3.0, 4.0], [5.0, 6.0]]", "One-hot weights select their corresponding value vectors.")],
168: [("([1.0], [[1.0], [0.0]], [[1.0, 0.0]], [[0.0, 1.0]], [1.0, 0.0])", "[0.7615941559557649, 0.0]", "The first key has hidden activation tanh(1); the second has zero."),
      ("([0.0], [[2.0], [-2.0]], [[1.0, 0.0]], [[0.0, 1.0]], [0.0, 1.0])", "[0.0, 0.0]", "The query projection is zero, so the selected v projection is zero.")],
169: [("([5, 0, 7, 0], 0)", "[True, False, True, False]", "Only IDs equal to the padding ID are masked."),
      ("(([2, 2, 2]), 2)", "[False, False, False]", "A sequence of padding IDs is entirely invalid for attention.")],
170: [("([[1, 2, 3], [4]], 0)", "([[1, 2, 3], [4, 0, 0]], [3, 1])", "The shorter row is right-padded to the longest length."),
      ("(([], [7, 8]), -1)", "([[-1, -1], [7, 8]], [0, 2])", "An empty row receives only padding and has length zero.")],
171: [("([4, 0, 5], 0)", "[1, 0, 1]", "Non-padding IDs map to one and padding maps to zero."),
      ("(([2, 2]), 2)", "[0, 0]", "Every position is masked when all IDs are padding.")],
172: [("(2, 3)", "[[0.0, 1.0, 0.0], [0.8414709848078965, 0.5403023058681398, 0.002154433023365604]]", "Even columns use sine and odd columns cosine, with an odd width supported."),
      ("(1, 4)", "[[0.0, 1.0, 0.0, 1.0]]", "At position zero, sine columns are zero and cosine columns are one.")],
173: [("([[1, 2], [3, 4], [5, 6]], 2)", "[[1, 2], [3, 4]]", "The first two learned position vectors are selected."),
      ("(([[0.5], [1.5]]), 0)", "[]", "A zero-length prefix has zero rows.")],
174: [("([3, 0, 2])", "[0, 3, 3]", "The second sequence starts after three items; the third starts at the same offset because the second is empty."),
      ("(([1, 1, 1]),)", "[0, 1, 2]", "Unit lengths produce consecutive offsets.")],
175: [("([[[1.0, 2.0], [3.0, 4.0], [9.0, 9.0]]], [[1, 1, 0]])", "[[2.0, 3.0]]", "The masked final token does not affect the mean."),
      ("(([[[7.0, 8.0], [9.0, 10.0]]]), [[0, 0]])", "[[0.0, 0.0]]", "No selected tokens produce a zero vector.")],
176: [("((['a', 'b', 'a', 'c', 'b', 'a']), 2)", "[('a', 3), ('b', 2)]", "The two most frequent tokens appear in descending count order."),
      ("((['x', 'y', 'y', 'x']), 2)", "[('x', 2), ('y', 2)]", "Ties preserve first appearance order.")],
177: [("((['cat', 'dog', 'bird']), {'cat': 1, 'dog': 2}, 0)", "[1, 2, 0]", "Known tokens keep their IDs and bird uses the unknown ID."),
      ("((['x', 'x']), {}, 99)", "[99, 99]", "Every token maps to unk_id for an empty vocabulary.")],
178: [("(([[[0, 1, 2, 3], [4, 5, 6, 7]]]), 2)", "[[[[0, 1], [4, 5]], [[2, 3], [6, 7]]]]", "Two feature heads are split and moved before the time axis."),
      ("(([[[0, 1, 2, 3]]]), 1)", "[[[[0, 1, 2, 3]]]]", "One head retains the entire feature width.")],
179: [("(([[[[0, 1], [2, 3]], [[4, 5], [6, 7]]]]),)", "[[[0, 1, 4, 5], [2, 3, 6, 7]]]", "At each time step, features from both heads are concatenated."),
      ("(([[[[9]], [[8]]]]),)", "[[[9, 8]]]", "A single time position merges its per-head features.")],
180: [("(([1.0, 2.0], lambda x: x * 2))", "[3.0, 6.0]", "The sublayer output is added elementwise to the residual input."),
      ("(([3, 4], lambda x: x * 0))", "[3, 4]", "A zero sublayer leaves the input unchanged.")],
181: [("([[-1.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0], [[1.0], [2.0]], [0.0])", "[[4.0]]", "ReLU removes the negative first activation before the second projection."),
      ("(([1.0]), [[1.0]], [0.0], [[2.0]], [1.0])", "[3.0]", "A one-dimensional positive activation is projected and biased.")],
182: [("([1.0], lambda x: x * 2, lambda x: x + 1, lambda x: x * 3)", "[12.0]", "Attention sees norm(x)=2; the two residual additions yield 12."),
      ("([0.0, 1.0], lambda x: x, lambda x: x * 0, lambda x: x * 0)", "[0.0, 1.0]", "Zero sublayers preserve the input through both residual paths.")],
183: [("([1.0], lambda x: x * 2, lambda x: x + 1, lambda x: x * 3)", "[1.0]", "The first and second residual sums are each normalized by the supplied function."),
      ("([0.0, 1.0], lambda x: x, lambda x: x * 0, lambda x: x * 0)", "[0.0, 1.0]", "Identity normalization and zero sublayers preserve x.")],
184: [("(([['a', 'b', 'a'], ['a', 'b']]),)", "(['a', 'b'], 2)", "The pair a,b occurs twice across the two sequences."),
      ("((['x', 'y', 'z'],),)", "(['x', 'y'], 1)", "All pairs tie, so the first encountered pair wins.")],
185: [("((['a', 'b', 'a', 'b', 'c']), ('a', 'b'))", "['ab', 'ab', 'c']", "Both non-overlapping occurrences merge from left to right."),
      ("((['a', 'a', 'a']), ('a', 'a'))", "['aa', 'a']", "The first pair merges; its second token is not reused.")],
186: [("(4, 8, 2)", "0.25", "The score is 4 divided by 8×2."),
      ("(3, 3, 3)", "0.3333333333333333", "The score is one third.")],
187: [("([10, 11, 12, 13])", "([10, 11, 12], [11, 12, 13])", "Each input token is paired with its immediate successor."),
      ("(([5, 6]),)", "([5], [6])", "A two-token sequence produces one input-target pair.")],
188: [("([10, 11, 12], [False, True, False])", "([10, 11, 12], [-100, 11, -100])", "Only the selected middle token remains as a training label."),
      ("(([3, 4]), [True, True], -1)", "([3, 4], [3, 4])", "All positions are selected and use their original IDs.")],
189: [("(0.0)", "1.0", "The exponential of zero is one."),
      ("(1.0)", "2.718281828459045", "A mean NLL of one has perplexity e.")],
190: [("([1.0, 3.0, 2.0], 2, rng)", "one of indices 1 or 2", "Only the two highest-logit candidates can be sampled."),
      ("(([5.0, 1.0]), 1, rng)", "0", "With k equal to one, the maximum-logit token is certain.")],
191: [("([4.0, 0.0, -1.0], 0.5, rng)", "0", "The dominant token alone exceeds the requested cumulative probability."),
      ("(([0.0, 0.0]), 1.0, rng)", "either index 0 or 1", "At p_cut one, the complete vocabulary remains eligible.")],
192: [("([0.0, 0.0], 1.0)", "[0.5, 0.5]", "Equal logits at unit temperature give a uniform distribution."),
      ("(([0.0, 1.0]), 1.0)", "[0.2689414213699951, 0.7310585786300049]", "Softmax subtracts the maximum before exponentiating.")],
193: [("([1.0, 3.0, 2.0])", "1", "Index one contains the largest logit."),
      ("(([4.0, 4.0, 1.0]),)", "0", "The first index wins when maximum logits tie.")],
194: [("([[1, 2], [3, 4]], [5, 6])", "[[1, 2], [3, 4], [5, 6]]", "The new vector becomes one row at the end of the sequence axis."),
      ("(([[1], [2]]), [3])", "[[1], [2], [3]]", "A one-feature cache appends the third position.")],
195: [("([1.0, 2.0], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 3.0]])", "[2.0, 6.0]", "A is identity; B scales the two coordinates by two and three."),
      ("(([3.0]), [[2.0]], [[4.0]])", "[24.0]", "The scalar chain multiplies 3 by 2 and then by 4.")],
196: [("(4, 6, 2)", "20", "Rank two gives 2×(4+6) parameters."),
      ("(10, 10, 1)", "20", "Rank one uses one input-width and one output-width matrix.")],
197: [("(100, 35)", "65", "Subtracting prompt usage leaves 65 context tokens."),
      ("((20, 25),)", "0", "An overlong prompt leaves no response budget.")],
198: [("([2, 1, 2, 3, 2])", "2", "Label two has the largest vote count."),
      ("(([3, 1, 3, 1]),)", "1", "Equal vote counts resolve to the smaller label.")],
199: [("([1.0, 2.0, 3.0])", "[-1.224744871391589, 0.0, 1.224744871391589]", "Subtracting mean two and dividing by population standard deviation gives the z-scores."),
      ("(([5.0, 5.0]),)", "[0.0, 0.0]", "A constant reward batch maps to zeros instead of dividing by zero.")],
200: [("((['cat', ' dog '], ['cat', 'dog']),)", "1.0", "Both string pairs match after surrounding whitespace is trimmed."),
      ("(([1, 2, 3], [1, 0, 3]),)", "0.6666666666666666", "Two of the three predictions match exactly.")],
}

if __name__ == "__main__":
    main()
