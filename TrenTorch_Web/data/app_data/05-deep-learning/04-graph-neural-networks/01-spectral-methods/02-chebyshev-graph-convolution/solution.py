import numpy as np


def chebyshev_conv(features, adj, weight, k=3):
    """Apply Chebyshev graph convolution.

    Args:
        features: Node features, shape (num_nodes, input_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        weight: Weight matrix, shape (k+1, input_dim, output_dim).
        k: Order of Chebyshev polynomial.

    Returns:
        Updated features, shape (num_nodes, output_dim).
    """
    num_nodes = adj.shape[0]
    degree = np.sum(adj, axis=1)
    degree_inv_sqrt = 1.0 / np.sqrt(degree + 1e-8)
    d_inv_sqrt = np.diag(degree_inv_sqrt)

    adj_norm = d_inv_sqrt @ adj @ d_inv_sqrt
    laplacian = np.eye(num_nodes) - adj_norm

    chebyshev_polys = [np.eye(num_nodes), laplacian]
    for i in range(2, k + 1):
        next_poly = 2 * laplacian @ chebyshev_polys[-1] - chebyshev_polys[-2]
        chebyshev_polys.append(next_poly)

    output = np.zeros((num_nodes, weight.shape[2]))
    for i in range(k + 1):
        conv_feat = chebyshev_polys[i] @ features
        output = output + conv_feat @ weight[i]

    return output
