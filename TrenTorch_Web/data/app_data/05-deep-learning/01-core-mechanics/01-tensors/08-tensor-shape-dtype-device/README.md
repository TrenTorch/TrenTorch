---
name: dl-tensor-tensor-shape-dtype-device
title: 'Tensor Properties: Shape, Dtype, Device'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Query tensor metadata: .shape, .dtype, .device, .requires_grad. Move tensors between CPU/GPU. Cast dtypes. Understand implications for memory and computation.

## Theory

### Tensor metadata controls computation

Every tensor has intrinsic properties:

`python
a = torch.randn(3, 4, dtype=torch.float32, device='cuda')
print(a.shape)          # torch.Size([3, 4])
print(a.dtype)          # torch.float32
print(a.device)         # device(type='cuda', index=0)
print(a.requires_grad)  # False (set True for learnable params)
print(a.ndim)           # 2 (number of dimensions)
print(a.numel())        # 12 (total elements)
`

### Device: CPU vs GPU

`python
a = torch.randn(1000, 1000)          # CPU by default
b = a.to('cuda')                     # Move to GPU
c = a.cuda()                         # Alternative
d = b.cpu()                          # Back to CPU
`

### Dtype conversion

`python
f = torch.tensor([1.5, 2.5])         # float32
i = f.to(torch.int32)                # [1, 2] (truncate)
f16 = f.half()                       # float16 (memory saving)
f64 = f.double()                     # float64 (higher precision)
`

### requires_grad for backprop

`python
param = torch.randn(10, requires_grad=True)  # Learnable
const = torch.randn(10)                      # Not learnable
`

### Why metadata matters

- Device: GPU 100x faster for neural nets than CPU
- Dtype: float32 standard; float16 saves memory; float64 rare
- requires_grad: backward() skips non-learnable tensors
- Shape: understanding shapes crucial for debugging

## Explanation

Solutions query metadata, move tensors to different devices, convert dtypes, and understand implications. Key insight: device mismatch (CPU vs GPU) is a common error; always check.
