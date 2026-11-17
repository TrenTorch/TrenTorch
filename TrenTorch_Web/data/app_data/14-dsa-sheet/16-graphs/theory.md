> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Graphs)

Graphs are everywhere: maps, friendships, web pages, game boards, task lists. This course teaches how to think about them and how to answer the questions interviewers love to ask. It assumes only that you can write loops and a simple function.

The course is a staircase. **Chapter 1 is gentle**: what a graph is and how to store one. Chapters 2 and 3 teach the two basic ways of walking through a graph. After that each chapter adds one new tool: finding cycles, putting tasks in order, shortest paths, union-find, spanning trees, and bridges and strongly connected components. The last two chapters combine graphs with dynamic programming, first on graphs without cycles and then on graphs with cycles. If a later chapter looks hard, do not worry; every chapter only uses what came before.

Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Graphs from scratch

## 1.1 What a graph is

A **graph** is a collection of dots joined by lines. The dots are called **vertices** (or nodes) and the lines are called **edges**. Think of a map: cities are vertices and roads are edges. Or a social network: people are vertices and friendships are edges. Even the web is a graph, with pages as vertices and links as edges.

An edge can be **undirected**, meaning it works in both directions like a friendship, or **directed**, meaning it works in one direction only like a one-way street. An edge can also carry a **weight**, a number such as the length of a road. A **path** is a walk along edges from one vertex to another, and a **cycle** is a path that comes back to where it started. A graph is **connected** when you can walk from any vertex to any other.

Throughout this course the vertices are numbered $0, 1, \dots, n-1$, and the graph is given as a list of edges, each a pair of numbers. The first job is always to turn that list into something a program can walk through quickly.

## 1.2 Storing a graph

The usual choice is the **adjacency list**: for every vertex we keep a list of its neighbours. For the edges 0-1, 1-2 and 2-3 the lists are `0: [1]`, `1: [0, 2]`, `2: [1, 3]` and `3: [2]`. Because the edges are undirected, each edge is written twice, once in each endpoint's list. For a directed graph you write it once only, in the list of the vertex where the arrow starts.

```python
def build_adj(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj

assert build_adj(4, [(0, 1), (1, 2), (2, 3)]) == [[1], [0, 2], [1, 3], [2]]
assert build_adj(3, [(0, 1), (1, 2)], True) == [[1], [2], []]
```

```cpp
vector<vector<int>> build_adj(int n, const vector<pair<int,int>>& edges, bool directed = false) {
    vector<vector<int>> adj(n);
    for (auto [u, v] : edges) {
        adj[u].push_back(v);
        if (!directed) adj[v].push_back(u);
    }
    return adj;
}
```

When edges have weights, we store pairs `(neighbour, weight)` instead of plain numbers. We will do that in the chapter on shortest paths.

The other classic choice is the **adjacency matrix**, an $n \times n$ table where entry `[u][v]` is 1 if the edge exists and 0 otherwise. It answers "is there an edge between $u$ and $v$?" in a single step, but it always uses $O(n^2)$ memory, and listing the neighbours of a vertex means scanning a whole row. The list needs only $O(n+m)$ memory for $m$ edges and lists neighbours instantly, so it is the right default whenever the graph is sparse, which is almost always. We use adjacency lists for the rest of the course.

## 1.3 A grid is a graph

A maze or a chessboard is a graph too: every cell is a vertex, and a cell is joined to the cells above, below, left and right of it, when those exist. Nobody builds an adjacency list for a grid. Instead we write the four moves once, as a **direction array**, and loop over them. A cell $(r, c)$ then has the neighbours $(r + dr_k, c + dc_k)$ for $k = 0, 1, 2, 3$, and we keep only those inside the grid.

```python
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]

def neighbours(R, C, r, c):
    result = []
    for k in range(4):
        nr, nc = r + DR[k], c + DC[k]
        if 0 <= nr < R and 0 <= nc < C:
            result.append((nr, nc))
    return result

assert neighbours(2, 3, 0, 0) == [(0, 1), (1, 0)]
assert neighbours(2, 3, 1, 1) == [(0, 1), (1, 2), (1, 0)]
```

```cpp
const int DR[4] = {-1, 0, 1, 0};
const int DC[4] = {0, 1, 0, -1};

vector<pair<int,int>> neighbours(int R, int C, int r, int c) {
    vector<pair<int,int>> result;
    for (int k = 0; k < 4; ++k) {
        int nr = r + DR[k], nc = c + DC[k];
        if (0 <= nr && nr < R && 0 <= nc && nc < C) result.push_back({nr, nc});
    }
    return result;
}
```

The moves are in the order up, right, down, left. In the second test the cell in row 1, column 1 of a grid with 2 rows and 3 columns has no cell below it, so it has three neighbours. If a problem also allows diagonal moves, extend both arrays to eight entries and nothing else changes.

## 1.4 Connected components

Take an undirected graph and start walking from some vertex, always stepping to neighbours you have not seen yet. Sooner or later you run out of new vertices. Everything you reached forms one **connected component**: a group of vertices that can all reach each other, with no edge leaving the group. Every vertex belongs to exactly one component.

To find all components, keep a `seen` array and a to-do pile (a plain stack). For each vertex in turn, if it is not seen, a new component starts there. Mark it, put it on the pile, and then, while the pile is not empty, take a vertex off it and put each unseen neighbour on the pile after marking it. Counting how many times a new component starts gives the number of components. (Chapters 2 and 3 study the two classic orders for walking, breadth-first and depth-first. For counting, any order works.)

Take $n = 5$ and the edges 0-1, 1-2, 3-4. Vertex 0 starts component one and reaches 1 and 2. Vertex 3 starts component two and reaches 4. Nothing is left, so the answer is 2. This is exactly the problem _Number of Connected Components_.

```python
def count_components(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    count = 0
    for start in range(n):
        if seen[start]:
            continue
        count += 1
        seen[start] = True
        pile = [start]
        while pile:
            v = pile.pop()
            for u in adj[v]:
                if not seen[u]:
                    seen[u] = True
                    pile.append(u)
    return count

assert count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
assert count_components(3, []) == 3
```

```cpp
int count_components(int n, const vector<pair<int,int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto [u, v] : edges) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<bool> seen(n, false);
    int count = 0;
    for (int start = 0; start < n; ++start) {
        if (seen[start]) continue;
        ++count;
        seen[start] = true;
        vector<int> pile = {start};
        while (!pile.empty()) {
            int v = pile.back();
            pile.pop_back();
            for (int u : adj[v]) {
                if (!seen[u]) {
                    seen[u] = true;
                    pile.push_back(u);
                }
            }
        }
    }
    return count;
}
```

Each vertex is marked once and each edge is looked at twice, so this runs in $O(n+m)$ time and uses $O(n+m)$ space.

The same walk answers "is there a path from $a$ to $b$?". Start the walk at $a$ and report whether $b$ gets reached. This is exactly the problem _Is There a Path?_. We can even stop as soon as $b$ comes off the pile.

```python
def has_path(n, edges, a, b):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    seen[a] = True
    pile = [a]
    while pile:
        v = pile.pop()
        if v == b:
            return True
        for u in adj[v]:
            if not seen[u]:
                seen[u] = True
                pile.append(u)
    return False

assert has_path(3, [(0, 1), (1, 2), (2, 0)], 0, 2)
assert not has_path(6, [(0, 1), (0, 2), (3, 5), (5, 4), (4, 3)], 0, 5)
```

```cpp
bool has_path(int n, const vector<pair<int,int>>& edges, int a, int b) {
    vector<vector<int>> adj(n);
    for (auto [u, v] : edges) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<bool> seen(n, false);
    seen[a] = true;
    vector<int> pile = {a};
    while (!pile.empty()) {
        int v = pile.back();
        pile.pop_back();
        if (v == b) return true;
        for (int u : adj[v]) {
            if (!seen[u]) {
                seen[u] = true;
                pile.push_back(u);
            }
        }
    }
    return false;
}
```

## 1.5 Check yourself

1. How many connected components has a graph with 6 vertices and the edges 0-1, 1-2 and 4-5?
2. Why is an edge of an undirected graph stored twice in an adjacency list?
3. A grid has 3 rows and 4 columns. How many neighbours does the cell in row 0, column 0 have?
4. Why do we mark a vertex as seen when we put it on the pile, rather than when we take it off?

# Chapter 2. Breadth-first search

## 2.1 Exploring in rings

Imagine dropping a pebble into a pond. A ripple spreads out in rings: first everything one step away, then everything two steps away, then three, and so on. **Breadth-first search**, or **BFS**, explores a graph in exactly this way. It starts at one vertex, called the **source**, visits all of its neighbours, then all of their neighbours, and keeps going outward ring by ring.

This ring-by-ring order has a very useful side effect. The first time BFS reaches a vertex, it has used the fewest possible edges to get there. That is why BFS is the standard tool for finding shortest paths when every edge counts the same.

## 2.2 The queue and the visited array

To explore ring by ring we need to remember which vertices are waiting for their turn. We use a **queue**, a line where the first vertex to join is the first one to be served. We also keep a **visited** array, so that we never put the same vertex into the line twice.

The recipe is short. Put the source in the queue and mark it visited. Then repeat: take the vertex at the front of the queue, look at each of its neighbours, and for every neighbour that is not visited yet, mark it visited and add it to the back of the queue. Stop when the queue is empty.

Let us trace it on a small graph with five vertices and the edges 0-1, 0-2, 1-3, 2-4 and 3-4:

```
0 --- 1
|     |
2     3
|     |
4 ----+
```

We start at vertex 0, so the queue is `[0]`. We take 0 and find the neighbours 1 and 2, which are new, so the queue becomes `[1, 2]`. We take 1 and find 3, so the queue is `[2, 3]`. We take 2 and find 4, so the queue is `[3, 4]`. Taking 3 and then 4 discovers nothing new, because all their neighbours are already visited. The queue is empty and every vertex has been reached.

We usually store, for every vertex, the **distance** from the source, which is the number of edges on the way. A distance of `-1` can mean "not reached yet", which also replaces the visited array.

```python
from collections import deque

def bfs(n, adj, source):
    dist = [-1] * n
    dist[source] = 0
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for u in adj[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                queue.append(u)
    return dist

adj = [[1, 2], [0, 3], [0, 4], [1, 4], [2, 3]]
assert bfs(5, adj, 0) == [0, 1, 1, 2, 2]
```

```cpp
vector<int> bfs(int n, const vector<vector<int>>& adj, int source) {
    vector<int> dist(n, -1);
    dist[source] = 0;
    queue<int> q;
    q.push(source);
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int u : adj[v]) {
            if (dist[u] == -1) {
                dist[u] = dist[v] + 1;
                q.push(u);
            }
        }
    }
    return dist;
}
```

Every vertex enters the queue at most once and every edge is looked at a constant number of times, so BFS runs in $O(n+m)$ time for $n$ vertices and $m$ edges, and uses $O(n)$ extra space.

## 2.3 Why BFS finds shortest paths

Vertices leave the queue in order of their distance: first the source (distance 0), then everything at distance 1, then everything at distance 2, and so on. A vertex at distance $d+1$ can only be discovered by a vertex at distance $d$, and all vertices at distance $d$ are served before any vertex at distance $d+1$. So when a vertex is discovered, it is discovered through a shortest route, and its recorded distance never needs to be corrected.

If you need the path itself and not only its length, remember for every vertex who discovered it, in an array called `parent`. Then walk from the target back to the source and reverse what you collected.

```python
from collections import deque

def shortest_path(n, adj, source, target):
    parent = [-1] * n
    seen = [False] * n
    seen[source] = True
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for u in adj[v]:
            if not seen[u]:
                seen[u] = True
                parent[u] = v
                queue.append(u)
    if not seen[target]:
        return []
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])
    return path[::-1]

adj = [[1, 2], [0, 3], [0, 4], [1, 4], [2, 3]]
assert shortest_path(5, adj, 0, 4) == [0, 2, 4]
assert shortest_path(5, adj, 0, 0) == [0]
```

```cpp
vector<int> shortest_path(int n, const vector<vector<int>>& adj, int source, int target) {
    vector<int> parent(n, -1);
    vector<bool> seen(n, false);
    queue<int> q;
    seen[source] = true;
    q.push(source);
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int u : adj[v]) {
            if (!seen[u]) {
                seen[u] = true;
                parent[u] = v;
                q.push(u);
            }
        }
    }
    if (!seen[target]) return {};
    vector<int> path = {target};
    while (path.back() != source) path.push_back(parent[path.back()]);
    reverse(path.begin(), path.end());
    return path;
}
```

## 2.4 BFS on a grid: shortest path in a binary matrix

A grid is a graph whose vertices are cells, as we saw in Chapter 1. This is exactly the problem _Shortest Path in Binary Matrix_. We are given a grid of `0` (open) and `1` (blocked) cells and want the shortest route from the top-left cell to the bottom-right cell. In this problem we may also move diagonally, so every cell has up to 8 neighbours. The answer counts the cells on the path, both ends included.

We run BFS from the top-left cell. Instead of a separate visited array we store the distance in a table `dist`, which starts as `-1` everywhere.

```python
from collections import deque

def shortest_path_binary_matrix(grid):
    n = len(grid)
    if n == 0 or grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    dist = [[-1] * n for _ in range(n)]
    dist[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return dist[r][c]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
    return -1

assert shortest_path_binary_matrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
assert shortest_path_binary_matrix([[0, 1], [1, 0]]) == 2
assert shortest_path_binary_matrix([[1, 0], [0, 0]]) == -1
```

```cpp
int shortest_path_binary_matrix(vector<vector<int>>& grid) {
    int n = grid.size();
    if (n == 0 || grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
    vector<vector<int>> dist(n, vector<int>(n, -1));
    dist[0][0] = 1;
    queue<pair<int, int>> q;
    q.push({0, 0});
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        if (r == n - 1 && c == n - 1) return dist[r][c];
        for (int dr = -1; dr <= 1; dr++) {
            for (int dc = -1; dc <= 1; dc++) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0 && dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
    }
    return -1;
}
```

In the first example the path is $(0,0) \to (0,1) \to (1,2) \to (2,2)$, which has 4 cells. The loop also tries the move $(0,0)$ to itself, but that cell already has a distance, so it is skipped. The cost is $O(n^2)$ for an $n \times n$ grid, because each cell is handled once.

## 2.5 Many starting points at once

Sometimes there is not one source but many. This is exactly the problem _Distance to Nearest Zero_: for every cell of a grid with `0`s and `1`s, find how far the nearest `0` is.

Running one BFS from every cell would be slow. The trick is to flip the question and start from all the zeros together. Put every `0` cell into the queue at the beginning with distance 0. The BFS then spreads out from all of them at the same time, and the first ripple to reach a cell is the one from its nearest zero. This is called **multi-source BFS**, and it costs only $O(nm)$ for an $n \times m$ grid.

```python
from collections import deque

def nearest_zero(mat):
    rows = len(mat)
    if rows == 0:
        return []
    cols = len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist

assert nearest_zero([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
```

```cpp
vector<vector<int>> nearest_zero(vector<vector<int>>& mat) {
    int rows = mat.size();
    if (rows == 0) return {};
    int cols = mat[0].size();
    vector<vector<int>> dist(rows, vector<int>(cols, -1));
    queue<pair<int, int>> q;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (mat[r][c] == 0) {
                dist[r][c] = 0;
                q.push({r, c});
            }
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[r][c] + 1;
                q.push({nr, nc});
            }
        }
    }
    return dist;
}
```

## 2.6 Spreading over time: rotting oranges

Multi-source BFS also describes things that spread as time passes. In _Rotting Oranges_ a grid holds empty cells (`0`), fresh oranges (`1`) and rotten oranges (`2`). Each minute, every fresh orange next to a rotten one becomes rotten. We want the number of minutes until no fresh orange is left, or `-1` if some orange can never rot.

Every rotten orange starts in the queue. One ring of the BFS is one minute, so we process the queue one whole ring at a time and count the rings. We also count the fresh oranges, so that at the end we can tell whether any are left over.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0]) if grid else 0
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1

assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert oranges_rotting([[0, 2]]) == 0
```

```cpp
int oranges_rotting(vector<vector<int>>& grid) {
    int rows = grid.size(), cols = rows ? grid[0].size() : 0;
    queue<pair<int, int>> q;
    int fresh = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 2) q.push({r, c});
            else if (grid[r][c] == 1) fresh++;
        }
    int minutes = 0;
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    while (!q.empty() && fresh > 0) {
        int size = q.size();
        while (size--) {
            auto [r, c] = q.front();
            q.pop();
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    q.push({nr, nc});
                }
            }
        }
        minutes++;
    }
    return fresh == 0 ? minutes : -1;
}
```

## 2.7 Graphs made from a rule: word ladder

Not every graph is handed to us as a list of edges. In _Word Ladder_ the vertices are words, and two words are neighbours if they differ in exactly one letter. We start from a word `begin` and want the shortest chain of words to `end`, where every word after the first must come from a given list. The answer is the number of words in the chain.

We never build the whole graph. When BFS is standing on a word, we simply try changing each letter to each of the 26 letters, and keep the new word if it is in the list and unseen. A set makes the lookup fast. For words of length $L$ and a list of $W$ words, this costs about $O(W \cdot L \cdot 26 \cdot L)$ in the worst case, because building each candidate word takes $O(L)$.

```python
from collections import deque

def ladder_length(begin, end, words):
    word_set = set(words)
    if end not in word_set:
        return 0
    dist = {begin: 1}
    queue = deque([begin])
    while queue:
        word = queue.popleft()
        if word == end:
            return dist[word]
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in word_set and nxt not in dist:
                    dist[nxt] = dist[word] + 1
                    queue.append(nxt)
    return 0

assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
```

```cpp
int ladder_length(string begin, string end, vector<string>& words) {
    unordered_set<string> word_set(words.begin(), words.end());
    if (!word_set.count(end)) return 0;
    unordered_map<string, int> dist;
    dist[begin] = 1;
    queue<string> q;
    q.push(begin);
    while (!q.empty()) {
        string word = q.front();
        q.pop();
        if (word == end) return dist[word];
        for (int i = 0; i < (int)word.size(); i++) {
            string next = word;
            for (char ch = 'a'; ch <= 'z'; ch++) {
                next[i] = ch;
                if (word_set.count(next) && !dist.count(next)) {
                    dist[next] = dist[word] + 1;
                    q.push(next);
                }
            }
        }
    }
    return 0;
}
```

## 2.8 0-1 BFS

What if some edges cost 0 and the others cost 1? A plain queue is no longer enough, because a free edge should not count as a step. The fix is a **deque**, a queue that lets us add at both ends. When we cross an edge of cost 0, the new vertex is as close as the current one, so it goes to the **front** and is served next. When we cross an edge of cost 1, it goes to the **back**, as in normal BFS. This keeps the vertices in order of distance, and we may update a vertex's distance more than once, as long as the new distance is smaller. The running time is still $O(n+m)$.

```python
from collections import deque

def zero_one_bfs(n, adj, source):
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    dq = deque([source])
    while dq:
        v = dq.popleft()
        for u, w in adj[v]:
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                if w == 0:
                    dq.appendleft(u)
                else:
                    dq.append(u)
    return dist

adj = [[(1, 0), (2, 1)], [(3, 1)], [(4, 0)], [(4, 1)], []]
assert zero_one_bfs(5, adj, 0) == [0, 0, 1, 1, 1]
```

```cpp
vector<int> zero_one_bfs(int n, const vector<vector<pair<int, int>>>& adj, int source) {
    vector<int> dist(n, INT_MAX);
    dist[source] = 0;
    deque<int> dq;
    dq.push_back(source);
    while (!dq.empty()) {
        int v = dq.front();
        dq.pop_front();
        for (auto [u, w] : adj[v]) {
            if (dist[v] + w < dist[u]) {
                dist[u] = dist[v] + w;
                if (w == 0) dq.push_front(u);
                else dq.push_back(u);
            }
        }
    }
    return dist;
}
```

## 2.9 Check yourself

1. Why does BFS use a queue and not a stack?
2. In the multi-source BFS of Section 2.5, why is the first distance written into a cell always the right one?
3. In rotting oranges, why do we process the queue one whole ring at a time?
4. In 0-1 BFS, why does a cost-0 edge send the vertex to the front of the deque?

# Chapter 3. Depth-first search

## 3.1 The idea: go deep, then back up

Imagine standing at the entrance of a maze with a piece of chalk. You walk forward until you hit a dead end, marking each junction you pass. Then you walk back to the last junction that still has an unexplored passage and go down that one. You keep going, always as deep as you can before backing up, until every corridor you can reach has been seen. That is **depth-first search**, or **DFS**.

Where breadth-first search (Chapter 2) explores in rings and uses a queue, DFS dives along one route at a time. It is easiest to write with **recursion**, a function that calls itself: `dfs(v)` marks `v` as visited and then calls `dfs(u)` for every neighbour `u` that is not visited yet. The mark is what stops us from walking around a cycle forever. The calls waiting for their turn form a stack, and that stack plays the role the queue played in BFS.

## 3.2 Recursive DFS traced by hand

Take five vertices with the edges 0-1, 0-2, 1-3 and 2-4. The adjacency lists are `0: [1, 2]`, `1: [0, 3]`, `2: [0, 4]`, `3: [1]` and `4: [2]`.

We call `dfs(0)`. Vertex 0 is marked and its first neighbour 1 is unvisited, so we call `dfs(1)`. Vertex 1 looks at 0 (already visited) and then at 3, so we call `dfs(3)`. Vertex 3 sees only 1, which is visited, so the call to `dfs(3)` returns. Back in vertex 1 there is nothing left, so it returns too. Now vertex 0 moves on to its second neighbour 2 and calls `dfs(2)`, which in turn calls `dfs(4)`. Both return, and so does `dfs(0)`.

The vertices were visited in the order 0, 1, 3, 2, 4. Notice how the walk went all the way down the branch 0, 1, 3 before it came back to try 2.

```python
def dfs_order(adj, start):
    visited = [False] * len(adj)
    order = []

    def dfs(v):
        visited[v] = True
        order.append(v)
        for u in adj[v]:
            if not visited[u]:
                dfs(u)

    dfs(start)
    return order

adj = [[1, 2], [0, 3], [0, 4], [1], [2]]
assert dfs_order(adj, 0) == [0, 1, 3, 2, 4]
```

```cpp
vector<int> dfs_order(const vector<vector<int>>& adj, int start) {
    vector<bool> visited(adj.size(), false);
    vector<int> order;
    function<void(int)> dfs = [&](int v) {
        visited[v] = true;
        order.push_back(v);
        for (int u : adj[v]) {
            if (!visited[u]) dfs(u);
        }
    };
    dfs(start);
    return order;
}
```

Every vertex is entered once and every edge is looked at a constant number of times, so DFS runs in $O(n+m)$ time. The stack of waiting calls can be as deep as $n$ (on a long path), so the extra space is $O(n)$. One practical warning: Python stops a recursion at about a thousand levels by default. For graphs with a very long path, such as a big grid full of land, use the explicit-stack style of the next sections.

## 3.3 Flood fill and counting islands

A grid of 0s and 1s is a graph in which every cell is a vertex joined to its four neighbours (Chapter 1). A group of land cells (1s) joined up, down, left and right is an **island**. Counting islands is exactly counting connected components: scan the cells in order, and every time you meet a land cell that is not visited yet, you have found a new island, so you count it and flood the whole island so that none of its cells is counted again.

Take this grid.

```
1 1 0
0 1 0
0 0 1
```

Scanning row by row, we meet the land cell (0, 0) first. Flooding from it reaches (0, 1) and then (1, 1), three cells in all. The scan continues and the next unvisited land cell is (2, 2), whose island has one cell. So there are 2 islands, and the largest has 3 cells. This is exactly the problem _Number of Islands_, and keeping the biggest flood size instead of counting floods is exactly the problem _Largest Island_.

To avoid the recursion limit on big grids, the flood below uses an explicit stack. It does the same thing as the recursive version: take a cell off the stack, push its unvisited land neighbours. It returns how many cells it flooded.

```python
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]

def flood(grid, seen, r, c):
    # marks the island containing (r, c) and returns its size
    R, C = len(grid), len(grid[0])
    seen[r][c] = True
    stack = [(r, c)]
    size = 0
    while stack:
        r, c = stack.pop()
        size += 1
        for k in range(4):
            nr, nc = r + DR[k], c + DC[k]
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1 and not seen[nr][nc]:
                seen[nr][nc] = True
                stack.append((nr, nc))
    return size

def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and not seen[r][c]:
                count += 1
                flood(grid, seen, r, c)
    return count

def max_island_area(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    best = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and not seen[r][c]:
                best = max(best, flood(grid, seen, r, c))
    return best

g = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
assert num_islands(g) == 2
assert max_island_area(g) == 3
assert num_islands([[0, 0], [0, 0]]) == 0
```

```cpp
const int DR[4] = {-1, 0, 1, 0};
const int DC[4] = {0, 1, 0, -1};

int flood(const vector<vector<int>>& grid, vector<vector<bool>>& seen, int r, int c) {
    int R = grid.size(), C = grid[0].size();
    seen[r][c] = true;
    vector<pair<int,int>> stack = {{r, c}};
    int size = 0;
    while (!stack.empty()) {
        auto [cr, cc] = stack.back();
        stack.pop_back();
        ++size;
        for (int k = 0; k < 4; ++k) {
            int nr = cr + DR[k], nc = cc + DC[k];
            if (0 <= nr && nr < R && 0 <= nc && nc < C && grid[nr][nc] == 1 && !seen[nr][nc]) {
                seen[nr][nc] = true;
                stack.push_back({nr, nc});
            }
        }
    }
    return size;
}

int num_islands(const vector<vector<int>>& grid) {
    if (grid.empty() || grid[0].empty()) return 0;
    int R = grid.size(), C = grid[0].size();
    vector<vector<bool>> seen(R, vector<bool>(C, false));
    int count = 0;
    for (int r = 0; r < R; ++r)
        for (int c = 0; c < C; ++c)
            if (grid[r][c] == 1 && !seen[r][c]) {
                ++count;
                flood(grid, seen, r, c);
            }
    return count;
}

int max_island_area(const vector<vector<int>>& grid) {
    if (grid.empty() || grid[0].empty()) return 0;
    int R = grid.size(), C = grid[0].size();
    vector<vector<bool>> seen(R, vector<bool>(C, false));
    int best = 0;
    for (int r = 0; r < R; ++r)
        for (int c = 0; c < C; ++c)
            if (grid[r][c] == 1 && !seen[r][c])
                best = max(best, flood(grid, seen, r, c));
    return best;
}
```

Each cell is pushed at most once, so both functions run in $O(R \cdot C)$ time and use $O(R \cdot C)$ space for the `seen` table and the stack.

**Flood fill** is the paint-bucket tool of a drawing program. You click a cell, and its colour spreads to every connected cell of the same original colour. The walk is the same as before, except that no `seen` table is needed: recolouring a cell already marks it, because a cell with the new colour no longer matches the old colour. The one trap is when the new colour equals the old one. Then recolouring would not mark anything and the walk would never stop, so we return at once. This is exactly the problem _Flood Fill_.

```python
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    R, C = len(image), len(image[0])
    image[sr][sc] = color
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        for k in range(4):
            nr, nc = r + DR[k], c + DC[k]
            if 0 <= nr < R and 0 <= nc < C and image[nr][nc] == old:
                image[nr][nc] = color
                stack.append((nr, nc))
    return image

assert flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert flood_fill([[0, 0], [0, 0]], 0, 0, 0) == [[0, 0], [0, 0]]
```

```cpp
vector<vector<int>> flood_fill(vector<vector<int>> image, int sr, int sc, int color) {
    int old = image[sr][sc];
    if (old == color) return image;
    int R = image.size(), C = image[0].size();
    image[sr][sc] = color;
    vector<pair<int,int>> stack = {{sr, sc}};
    while (!stack.empty()) {
        auto [r, c] = stack.back();
        stack.pop_back();
        for (int k = 0; k < 4; ++k) {
            int nr = r + DR[k], nc = c + DC[k];
            if (0 <= nr && nr < R && 0 <= nc && nc < C && image[nr][nc] == old) {
                image[nr][nc] = color;
                stack.push_back({nr, nc});
            }
        }
    }
    return image;
}
```

## 3.4 DFS from the borders

Sometimes the cheap way to answer a question about every cell is to run the search backwards from the answer. In _Pacific Atlantic Water Flow_ each cell has a height, and water flows from a cell to a neighbour of equal or lower height. The Pacific touches the top and left edges of the grid and the Atlantic touches the bottom and right edges. We want every cell from which water can reach both oceans.

Starting a search from each cell would repeat the same work over and over. Instead start from the ocean. The cells next to the Pacific can obviously reach it. A cell next to one of those can reach it too if water can flow from that cell into it, which means the neighbour must be **at least as high**. So we flood from all the Pacific-side border cells at once, moving only to neighbours of greater or equal height, and mark everything we reach. We do the same from the Atlantic side. The cells marked by both floods are the answer.

Take this 3 by 3 grid.

```
2 1 3
1 4 2
3 1 1
```

The Pacific flood starts from the whole top row and the whole left column. From the 1 at (0, 1) it can step to (1, 1), because 4 is higher than 1 (water on the 4 can flow down to the 1 and so on to the Pacific). From (1, 1) the neighbours (1, 2) = 2 and (2, 1) = 1 are lower than 4, so they are not reached this way, and (1, 2) is not reached from (0, 2) either, since 2 is lower than 3. The Pacific set is (0, 0), (0, 1), (0, 2), (1, 0), (1, 1) and (2, 0). The Atlantic flood, from the bottom row and right column, reaches (0, 2), (1, 1), (1, 2), (2, 0), (2, 1) and (2, 2). The two sets share exactly (0, 2), (1, 1) and (2, 0).

```python
def pacific_atlantic(heights):
    if not heights or not heights[0]:
        return []
    R, C = len(heights), len(heights[0])
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]

    def reach(starts):
        seen = [[False] * C for _ in range(R)]
        stack = []
        for r, c in starts:
            if not seen[r][c]:
                seen[r][c] = True
                stack.append((r, c))
        while stack:
            r, c = stack.pop()
            for k in range(4):
                nr, nc = r + DR[k], c + DC[k]
                if (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]
                        and heights[nr][nc] >= heights[r][c]):
                    seen[nr][nc] = True
                    stack.append((nr, nc))
        return seen

    pacific = reach([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
    atlantic = reach([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
    return [[r, c] for r in range(R) for c in range(C) if pacific[r][c] and atlantic[r][c]]

assert pacific_atlantic([[2, 1, 3], [1, 4, 2], [3, 1, 1]]) == [[0, 2], [1, 1], [2, 0]]
assert pacific_atlantic([[1]]) == [[0, 0]]
```

```cpp
vector<vector<int>> pacific_atlantic(const vector<vector<int>>& heights) {
    if (heights.empty() || heights[0].empty()) return {};
    int R = heights.size(), C = heights[0].size();
    int DR[4] = {-1, 0, 1, 0};
    int DC[4] = {0, 1, 0, -1};

    auto reach = [&](const vector<pair<int,int>>& starts) {
        vector<vector<bool>> seen(R, vector<bool>(C, false));
        vector<pair<int,int>> stack;
        for (auto [r, c] : starts) {
            if (!seen[r][c]) {
                seen[r][c] = true;
                stack.push_back({r, c});
            }
        }
        while (!stack.empty()) {
            auto [r, c] = stack.back();
            stack.pop_back();
            for (int k = 0; k < 4; ++k) {
                int nr = r + DR[k], nc = c + DC[k];
                if (0 <= nr && nr < R && 0 <= nc && nc < C && !seen[nr][nc]
                        && heights[nr][nc] >= heights[r][c]) {
                    seen[nr][nc] = true;
                    stack.push_back({nr, nc});
                }
            }
        }
        return seen;
    };

    vector<pair<int,int>> pacStarts, atlStarts;
    for (int c = 0; c < C; ++c) { pacStarts.push_back({0, c}); atlStarts.push_back({R - 1, c}); }
    for (int r = 0; r < R; ++r) { pacStarts.push_back({r, 0}); atlStarts.push_back({r, C - 1}); }
    auto pacific = reach(pacStarts);
    auto atlantic = reach(atlStarts);

    vector<vector<int>> answer;
    for (int r = 0; r < R; ++r)
        for (int c = 0; c < C; ++c)
            if (pacific[r][c] && atlantic[r][c]) answer.push_back({r, c});
    return answer;
}
```

Each of the two floods touches every cell at most once, so the time is $O(R \cdot C)$ and the space is $O(R \cdot C)$. The trick of searching **from the targets, in the reverse direction** shows up again whenever a question asks "which starting points can reach X?".

## 3.5 Entry and exit times

While DFS runs we can write down two moments for every vertex using a counter that goes up by one at each event. The **entry time** `tin[v]` is the counter value when DFS first arrives at `v`. The **exit time** `tout[v]` is the counter value when DFS has finished everything below `v` and leaves it. These numbers make the structure of the walk visible: vertex `u` is an **ancestor** of `v` (meaning DFS reached `v` while still inside `u`) exactly when `u` was entered before `v` and left after `v`. Chapter 9 relies on entry times.

On the five-vertex graph of Section 3.2, the events happen in this order: enter 0, enter 1, enter 3, leave 3, leave 1, enter 2, enter 4, leave 4, leave 2, leave 0. Numbering them from 0 gives `tin = [0, 1, 5, 2, 6]` and `tout = [9, 4, 8, 3, 7]`. Vertex 1 is an ancestor of 3 because $1 \le 2$ and $3 \le 4$, but 1 is not an ancestor of 2 because 2 was entered after 1 was already left.

To compute these numbers without recursion we keep our own stack of frames. A frame holds a vertex and the position of the next neighbour to try. At each step we look at the top frame. If it has a neighbour left, we advance its position, and if that neighbour is new we enter it and push a new frame. If it has no neighbours left, we record its exit time and pop it. This copies exactly what the call stack does in the recursive version.

```python
def dfs_times(adj, start):
    n = len(adj)
    tin = [-1] * n
    tout = [-1] * n
    timer = 0
    tin[start] = timer
    timer += 1
    stack = [[start, 0]]  # [vertex, index of next neighbour to try]
    while stack:
        frame = stack[-1]
        v = frame[0]
        if frame[1] < len(adj[v]):
            u = adj[v][frame[1]]
            frame[1] += 1
            if tin[u] == -1:
                tin[u] = timer
                timer += 1
                stack.append([u, 0])
        else:
            tout[v] = timer
            timer += 1
            stack.pop()
    return tin, tout

def is_ancestor(tin, tout, u, v):
    return tin[u] <= tin[v] and tout[v] <= tout[u]

adj = [[1, 2], [0, 3], [0, 4], [1], [2]]
tin, tout = dfs_times(adj, 0)
assert tin == [0, 1, 5, 2, 6]
assert tout == [9, 4, 8, 3, 7]
assert is_ancestor(tin, tout, 1, 3)
assert not is_ancestor(tin, tout, 1, 2)
```

```cpp
pair<vector<int>, vector<int>> dfs_times(const vector<vector<int>>& adj, int start) {
    int n = adj.size();
    vector<int> tin(n, -1), tout(n, -1);
    int timer = 0;
    tin[start] = timer++;
    vector<pair<int,int>> stack = {{start, 0}};  // {vertex, index of next neighbour}
    while (!stack.empty()) {
        int v = stack.back().first;
        int idx = stack.back().second;
        if (idx < (int)adj[v].size()) {
            stack.back().second++;
            int u = adj[v][idx];
            if (tin[u] == -1) {
                tin[u] = timer++;
                stack.push_back({u, 0});
            }
        } else {
            tout[v] = timer++;
            stack.pop_back();
        }
    }
    return {tin, tout};
}

bool is_ancestor(const vector<int>& tin, const vector<int>& tout, int u, int v) {
    return tin[u] <= tin[v] && tout[v] <= tout[u];
}
```

The time is $O(n+m)$ and the space is $O(n)$, with no risk of overflowing the call stack.

## 3.6 Check yourself

1. In recursive DFS, why do we mark a vertex as visited before calling DFS on its neighbours?
2. A grid is a single row of 1000 land cells. How deep can a recursive flood from one end go, and why can that be a problem in Python?
3. In the Pacific Atlantic problem, why do we start at the ocean and move to cells of greater or equal height?
4. If `tin[u] = 5`, `tout[u] = 12`, `tin[v] = 7` and `tout[v] = 10`, is `u` an ancestor of `v`?

# Chapter 4. Cycles, two colours and safe nodes

## 4.1 Cycles in an undirected graph

A cycle is a walk that leaves a vertex and returns to it without using the same edge twice. Depth-first search finds one the moment it stumbles on a vertex it has already visited, with one exception: the edge we just came along always leads back to a visited vertex (the one we came from), and that is not a cycle. So the rule is: **while exploring `v`, if an edge leads to an already visited vertex, and it is not the very edge we used to enter `v`, there is a cycle.**

Notice that we say "the very edge", not "the parent vertex". If the input contains the same edge twice, say `0-1` and `1-0`, they form a cycle of length 2 even though both lead to the same neighbour. Giving every edge a number and remembering the number of the edge we arrived by handles that case, and also self-loops (an edge from a vertex to itself), for free. In the adjacency list we therefore store pairs `(neighbour, edge number)`.

Let us trace it on the edges 0-1 (number 0), 1-2 (number 1), 2-0 (number 2) and 1-3 (number 3), starting at vertex 0. We go from 0 to 1 along edge 0. At 1 we skip edge 0, because it is the edge we arrived by, and go to 2 along edge 1. At 2 we skip edge 1 and then meet vertex 0 along edge 2. Vertex 0 is already visited and edge 2 is not the edge we came by, so we report a cycle. This is exactly the problem _Cycle in an Undirected Graph_.

```python
def has_cycle_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    visited = [False] * n

    def dfs(v, parent_edge):
        visited[v] = True
        for u, e in adj[v]:
            if e == parent_edge:
                continue
            if visited[u] or dfs(u, e):
                return True
        return False

    for v in range(n):
        if not visited[v] and dfs(v, -1):
            return True
    return False

assert has_cycle_undirected(4, [[0, 1], [1, 2], [2, 0], [1, 3]])
assert not has_cycle_undirected(4, [[0, 1], [1, 2], [2, 3]])
assert has_cycle_undirected(2, [[0, 1], [1, 0]])
assert has_cycle_undirected(1, [[0, 0]])
```

```cpp
bool has_cycle_undirected(int n, const vector<vector<int>>& edges) {
    vector<vector<pair<int,int>>> adj(n);
    for (int i = 0; i < (int)edges.size(); ++i) {
        int u = edges[i][0], v = edges[i][1];
        adj[u].push_back({v, i});
        adj[v].push_back({u, i});
    }
    vector<bool> visited(n, false);
    function<bool(int,int)> dfs = [&](int v, int parent_edge) {
        visited[v] = true;
        for (auto [u, e] : adj[v]) {
            if (e == parent_edge) continue;
            if (visited[u] || dfs(u, e)) return true;
        }
        return false;
    };
    for (int v = 0; v < n; ++v)
        if (!visited[v] && dfs(v, -1)) return true;
    return false;
}
```

The search touches each vertex and edge a constant number of times, so the time is $O(n+m)$ and the space is $O(n+m)$. For very long paths the recursion can get too deep in Python. A neat alternative needs no recursion at all: a connected component with $k$ vertices and $e$ edges is a tree exactly when $e = k-1$, so a cycle exists as soon as some component has $e \ge k$. Chapter 7 gives a third method, union-find.

## 4.2 Cycles in a directed graph

In a directed graph "visited before" is not enough. Take the edges 0→1, 0→2 and 1→2. DFS from 0 visits 1, then 2, then comes back and sees 2 again as a neighbour of 0, but there is no cycle, because the arrows never lead back to 0. What matters is whether the vertex we meet is still **being explored**, that is, whether it is one of the vertices on the current chain of calls.

So we use three colours. A vertex is **white** if DFS has not seen it, **grey** if DFS is inside it right now (it was entered but not finished), and **black** if DFS has completely finished it. Following an edge into a white vertex continues the search. Following an edge into a black vertex is harmless, because that vertex finished without finding a way back. But an edge into a grey vertex goes back to a vertex on our current chain, so the chain plus this edge is a cycle.

Take the edges 0→1, 1→2, 2→0 and 3→4. DFS from 0 turns 0, 1 and 2 grey in turn. At 2 the edge to 0 leads to a grey vertex, so we report a cycle. This is exactly the problem _Cycle in a Directed Graph_. Had that edge not existed, vertices would turn black on the way back (2, then 1, then 0), and the search from 3 would colour 4 and then 3 black without a surprise.

```python
def has_cycle_directed(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    WHITE, GREY, BLACK = 0, 1, 2
    colour = [WHITE] * n

    def dfs(v):
        colour[v] = GREY
        for u in adj[v]:
            if colour[u] == GREY:
                return True
            if colour[u] == WHITE and dfs(u):
                return True
        colour[v] = BLACK
        return False

    for v in range(n):
        if colour[v] == WHITE and dfs(v):
            return True
    return False

assert has_cycle_directed(5, [[0, 1], [1, 2], [2, 0], [3, 4]])
assert not has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]])
assert has_cycle_directed(1, [[0, 0]])
```

```cpp
bool has_cycle_directed(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back(e[1]);
    const int WHITE = 0, GREY = 1, BLACK = 2;
    vector<int> colour(n, WHITE);
    function<bool(int)> dfs = [&](int v) {
        colour[v] = GREY;
        for (int u : adj[v]) {
            if (colour[u] == GREY) return true;
            if (colour[u] == WHITE && dfs(u)) return true;
        }
        colour[v] = BLACK;
        return false;
    };
    for (int v = 0; v < n; ++v)
        if (colour[v] == WHITE && dfs(v)) return true;
    return false;
}
```

Time is $O(n+m)$ and space is $O(n+m)$.

## 4.3 Bipartite graphs and two colours

A graph is **bipartite** if its vertices can be split into two teams so that every edge joins one team to the other, with no edge inside a team. Equivalently, you can paint every vertex with one of two colours so that the two ends of every edge have different colours. A square 0-1-2-3-0 is bipartite (paint 0 and 2 red, 1 and 3 blue), but a triangle is not.

The test is a search that paints as it goes. Start at an unpainted vertex and paint it 0. Take a vertex off the queue, and for each neighbour: if it is unpainted, paint it with the opposite colour and queue it; if it is already painted with the same colour as the current vertex, two teammates are joined by an edge and the answer is no. Because a graph may have several components, we restart the painting from every unpainted vertex. The reason a triangle fails is that colours must alternate along a walk, so after three steps you are back at the start with the wrong colour. The same happens for any cycle with an odd number of vertices, and a graph with no odd cycle always paints successfully. This is exactly the problem _Is the Graph Bipartite?_.

```python
from collections import deque

def is_bipartite(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    colour = [-1] * n
    for start in range(n):
        if colour[start] != -1:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for u in adj[v]:
                if colour[u] == -1:
                    colour[u] = colour[v] ^ 1
                    queue.append(u)
                elif colour[u] == colour[v]:
                    return False
    return True

assert is_bipartite(4, [[0, 1], [1, 2], [2, 3], [3, 0]])
assert not is_bipartite(3, [[0, 1], [1, 2], [2, 0]])
assert not is_bipartite(1, [[0, 0]])
```

```cpp
bool is_bipartite(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<int> colour(n, -1);
    for (int start = 0; start < n; ++start) {
        if (colour[start] != -1) continue;
        colour[start] = 0;
        queue<int> q;
        q.push(start);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (colour[u] == -1) {
                    colour[u] = colour[v] ^ 1;
                    q.push(u);
                } else if (colour[u] == colour[v]) {
                    return false;
                }
            }
        }
    }
    return true;
}
```

The expression `colour[v] ^ 1` flips 0 to 1 and 1 to 0. The time is $O(n+m)$ and the space is $O(n+m)$.

## 4.4 Eventual safe states

In a directed graph, call a vertex a **terminal** if it has no outgoing edges. A vertex is **safe** if every path that starts at it ends at a terminal, in other words if it can never get trapped walking round a cycle forever. A vertex on a cycle is not safe, and neither is a vertex that has some path leading into a cycle.

Checking each vertex separately would repeat a lot of work, so let us flip the question around. A terminal is safe. A vertex is safe if all of its outgoing edges lead to safe vertices. This suggests peeling the graph from the end, a lot like the course-ordering idea of the next chapter. Count the outgoing edges of every vertex. Put the terminals (count 0) in a queue. When a vertex `v` is taken from the queue it is safe, so each vertex `u` that has an edge `u→v` has one fewer unsafe-or-unknown edge left: lower `u`'s count by one, and when it reaches 0, all of `u`'s edges lead to safe vertices, so `u` is safe too and joins the queue. To find the vertices `u` pointing at `v` we store the **reversed** graph.

Take the edges 0→1, 1→2, 2→3, 3→4, 4→5, 5→6, 6→3 (a cycle on 3, 4, 5, 6) and 7→8, 8→9, with 10 vertices. The only terminal is 9. Taking 9 lowers the count of 8 to zero, so 8 joins. Taking 8 frees 7. Taking 7 frees nobody. The vertices 3 to 6 each keep one outgoing edge that never gets removed, and 0, 1, 2 keep an edge into the cycle, so the safe vertices are 7, 8 and 9. This is exactly the problem _Eventual Safe Nodes_.

```python
from collections import deque

def eventual_safe_nodes(n, edges):
    reverse = [[] for _ in range(n)]
    out_count = [0] * n
    for u, v in edges:
        reverse[v].append(u)
        out_count[u] += 1
    queue = deque(v for v in range(n) if out_count[v] == 0)
    safe = [False] * n
    while queue:
        v = queue.popleft()
        safe[v] = True
        for u in reverse[v]:
            out_count[u] -= 1
            if out_count[u] == 0:
                queue.append(u)
    return [v for v in range(n) if safe[v]]

edges = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 3], [7, 8], [8, 9]]
assert eventual_safe_nodes(10, edges) == [7, 8, 9]
assert eventual_safe_nodes(7, [[0, 1], [0, 2], [1, 2], [1, 3], [2, 5], [3, 0], [4, 5]]) == [2, 4, 5, 6]
```

```cpp
vector<int> eventual_safe_nodes(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> reverse_adj(n);
    vector<int> out_count(n, 0);
    for (auto& e : edges) {
        reverse_adj[e[1]].push_back(e[0]);
        out_count[e[0]]++;
    }
    queue<int> q;
    for (int v = 0; v < n; ++v)
        if (out_count[v] == 0) q.push(v);
    vector<bool> safe(n, false);
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        safe[v] = true;
        for (int u : reverse_adj[v]) {
            if (--out_count[u] == 0) q.push(u);
        }
    }
    vector<int> answer;
    for (int v = 0; v < n; ++v)
        if (safe[v]) answer.push_back(v);
    return answer;
}
```

Each vertex enters the queue once and each edge is processed once, so the time is $O(n+m)$ and the space is $O(n+m)$.

## 4.5 Check yourself

1. In undirected cycle detection, why do we skip the edge we arrived by, and why is skipping it by number safer than skipping the parent vertex?
2. What does a grey vertex mean during a directed DFS, and why does meeting one prove that a cycle exists?
3. Can a graph that contains a triangle be bipartite? Answer in one sentence.
4. In the safe-nodes algorithm, why do we start the queue with the vertices that have no outgoing edges?

# Chapter 5. Topological sort

## 5.1 Prerequisites as arrows

Imagine a set of tasks where some must be finished before others can start: socks before shoes, foundations before walls, a course before the course that needs it. Draw an arrow from each task to the tasks that depend on it and you get a **directed graph**. A **topological order** is a way to line up all the tasks so that every arrow points forward, that is, every task appears after everything it depends on.

Here is a small graph with four tasks, drawn with edges 0→1, 0→2, 1→3 and 2→3.

```
0 → 1
↓   ↓
2 → 3
```

Both `[0, 1, 2, 3]` and `[0, 2, 1, 3]` are valid orders. If the arrows form a cycle (A before B, B before C, C before A), no order can exist, since each task would have to come before itself. So a topological order exists exactly when the graph has no directed cycle. Such a graph is called a **DAG**, a directed acyclic graph.

## 5.2 Kahn's algorithm

The first task in any order must be one that nothing points to, so its **in-degree**, the number of arrows coming in, is zero. Kahn's algorithm uses this repeatedly: put every vertex of in-degree zero in a queue. Take a vertex out, write it in the answer, and "remove" it from the graph, which means lowering by one the in-degree of every vertex it points to. Any vertex whose in-degree drops to zero has had all its prerequisites written down, so it joins the queue. Continue until the queue is empty.

Trace it on the graph above. The in-degrees are 0, 1, 1, 2 for vertices 0 to 3, so the queue starts as `[0]`. We take 0, which lowers the in-degrees of 1 and 2 to zero, so the queue is `[1, 2]`. We take 1, which lowers vertex 3 from 2 to 1. We take 2, which lowers vertex 3 to 0, so 3 joins. We take 3. The answer is `[0, 1, 2, 3]`.

If the graph has a cycle, the vertices on it never reach in-degree zero, because each waits for another one on the cycle. The queue then runs dry while some vertices are still unwritten. So **if the answer has fewer than $n$ vertices, a cycle exists.**

```python
from collections import deque

def topological_order(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == n else None

assert topological_order(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) == [0, 1, 2, 3]
assert topological_order(3, [[0, 1], [1, 2], [2, 0]]) is None
```

```cpp
// returns an empty vector when a cycle exists (for n > 0)
vector<int> topological_order(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        indeg[e[1]]++;
    }
    queue<int> q;
    for (int v = 0; v < n; ++v)
        if (indeg[v] == 0) q.push(v);
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    if ((int)order.size() == n) return order;
    return {};
}
```

Every vertex enters the queue once and every edge is relaxed once, so the time is $O(n+m)$ and the space is $O(n+m)$.

## 5.3 The DFS version

Depth-first search gives a second way. Run DFS, and write a vertex down at the moment it is **finished**, meaning all the vertices reachable from it have already been finished. A vertex is always finished after everything it points to, so the finishing list has every arrow pointing backwards, and reversing it gives a valid order. Cycles show up as in Chapter 4: meeting a vertex that is still being explored (grey) means a cycle.

On our graph, DFS from 0 goes to 1, then to 3. Vertex 3 finishes, then 1 finishes. Next 0 tries 2, whose only neighbour 3 is already done, so 2 finishes, and finally 0 finishes. The finishing list is `[3, 1, 2, 0]`, and reversed it is `[0, 2, 1, 3]`, another valid order.

```python
def topological_order_dfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    state = [0] * n  # 0 = new, 1 = being explored, 2 = finished
    finished = []

    def dfs(u):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1:
                return False
            if state[v] == 0 and not dfs(v):
                return False
        state[u] = 2
        finished.append(u)
        return True

    for u in range(n):
        if state[u] == 0 and not dfs(u):
            return None
    return finished[::-1]

assert topological_order_dfs(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) == [0, 2, 1, 3]
assert topological_order_dfs(3, [[0, 1], [1, 2], [2, 0]]) is None
```

```cpp
// returns an empty vector when a cycle exists (for n > 0)
vector<int> topological_order_dfs(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back(e[1]);
    vector<int> state(n, 0), finished;
    function<bool(int)> dfs = [&](int u) {
        state[u] = 1;
        for (int v : adj[u]) {
            if (state[v] == 1) return false;
            if (state[v] == 0 && !dfs(v)) return false;
        }
        state[u] = 2;
        finished.push_back(u);
        return true;
    };
    for (int u = 0; u < n; ++u)
        if (state[u] == 0 && !dfs(u)) return {};
    reverse(finished.begin(), finished.end());
    return finished;
}
```

The time is $O(n+m)$ and the space is $O(n+m)$. Kahn's algorithm is easier to turn into an iterative loop and to tweak (as in Section 5.5), while the DFS version is the one that generalises to the strongly connected components of Chapter 9.

## 5.4 Course schedule

In _Course Schedule_ you get `num_courses` courses and pairs `[a, b]` meaning "take `b` before `a`", and must decide whether all courses can be taken. Each pair is the arrow `b → a`. All courses can be taken exactly when no directed cycle exists, which is what Kahn's algorithm tells us: count the courses it manages to take. This is exactly the problem _Course Schedule_. The only new work is reading the pairs in the right direction.

```python
from collections import deque

def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:  # b must come before a
        adj[b].append(a)
        indeg[a] += 1
    queue = deque(v for v in range(num_courses) if indeg[v] == 0)
    taken = 0
    while queue:
        u = queue.popleft()
        taken += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return taken == num_courses

assert can_finish(2, [[1, 0]])
assert not can_finish(2, [[1, 0], [0, 1]])
assert can_finish(3, [])
```

```cpp
bool can_finish(int num_courses, const vector<vector<int>>& prerequisites) {
    vector<vector<int>> adj(num_courses);
    vector<int> indeg(num_courses, 0);
    for (auto& p : prerequisites) {  // p[1] must come before p[0]
        adj[p[1]].push_back(p[0]);
        indeg[p[0]]++;
    }
    queue<int> q;
    for (int v = 0; v < num_courses; ++v)
        if (indeg[v] == 0) q.push(v);
    int taken = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        ++taken;
        for (int v : adj[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    return taken == num_courses;
}
```

## 5.5 The smallest order first

Often there are many valid orders and a problem asks for the **lexicographically smallest** one, meaning the one that wins when you compare the first entries, then the second, and so on. The greedy answer is simple: at every step, among all the vertices that are available (in-degree zero), take the smallest. Kahn's queue gives no such promise, so we replace it by a **min-heap**, a container from which you can always pull out the smallest item quickly.

Take 5 courses with the arrows 3→0, 3→1, 4→1 and 1→2. At the start the available courses are 3 and 4, and we take 3. Now 0 becomes available while 1 still waits for 4, so the heap holds 0 and 4 and we take 0. Then only 4 is available, we take it, which frees 1, and 1 in turn frees 2. The order is `[3, 0, 4, 1, 2]`. A plain queue would have produced `[3, 4, 0, 1, 2]`, which is valid but not the smallest. This is exactly the problem _Course Order_.

```python
import heapq

def smallest_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:  # b must come before a
        adj[b].append(a)
        indeg[a] += 1
    heap = [v for v in range(num_courses) if indeg[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    return order if len(order) == num_courses else []

assert smallest_order(5, [[0, 3], [1, 3], [1, 4], [2, 1]]) == [3, 0, 4, 1, 2]
assert smallest_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
assert smallest_order(2, [[1, 0], [0, 1]]) == []
```

```cpp
vector<int> smallest_order(int num_courses, const vector<vector<int>>& prerequisites) {
    vector<vector<int>> adj(num_courses);
    vector<int> indeg(num_courses, 0);
    for (auto& p : prerequisites) {  // p[1] must come before p[0]
        adj[p[1]].push_back(p[0]);
        indeg[p[0]]++;
    }
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int v = 0; v < num_courses; ++v)
        if (indeg[v] == 0) heap.push(v);
    vector<int> order;
    while (!heap.empty()) {
        int u = heap.top();
        heap.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--indeg[v] == 0) heap.push(v);
        }
    }
    if ((int)order.size() == num_courses) return order;
    return {};
}
```

Each vertex goes through the heap once, so the time is $O(n \log n + m)$ and the space is $O(n+m)$.

## 5.6 Alien dictionary

Sometimes the graph is hidden. In _Alien Dictionary_ you get words that are sorted by an unknown alphabet, and you must recover an order of the letters that explains the list. Each pair of neighbouring words tells us one fact: at the first position where the two words differ, the letter of the first word comes before the letter of the second. Letters after that position tell us nothing, and neither do the letters before it, since they are equal.

For `["wrt", "wrf", "er", "ett", "rftt"]` the neighbouring pairs give `t→f` (from wrt, wrf), `w→e` (from wrf, er), `r→t` (from er, ett) and `e→r` (from ett, rftt). The graph has the unique topological order `w, e, r, t, f`, so the answer is `"wertf"`.

There are two traps. If a longer word is placed directly before its own prefix (`"abc"` then `"ab"`) the list cannot be sorted in any alphabet, so we return an empty string. And letters with no constraints between them can come in any order, so to return the smallest alphabetical order we use the heap of the previous section. If the letters contain a cycle, the answer is again the empty string. This is exactly the problem _Alien Dictionary_.

```python
import heapq

def alien_order(words):
    letters = sorted(set("".join(words)))
    after = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for w1, w2 in zip(words, words[1:]):
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in after[c1]:
                    after[c1].add(c2)
                    indeg[c2] += 1
                break
        else:
            if len(w1) > len(w2):
                return ""
    heap = [c for c in letters if indeg[c] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        c = heapq.heappop(heap)
        order.append(c)
        for d in after[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                heapq.heappush(heap, d)
    return "".join(order) if len(order) == len(letters) else ""

assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
assert alien_order(["ba", "bc"]) == "abc"
assert alien_order(["abc", "ab"]) == ""
assert alien_order(["z", "x", "z"]) == ""
```

```cpp
string alien_order(const vector<string>& words) {
    set<char> letters;
    for (auto& w : words) for (char c : w) letters.insert(c);
    map<char, set<char>> after;
    map<char, int> indeg;
    for (char c : letters) indeg[c] = 0;
    for (size_t i = 0; i + 1 < words.size(); ++i) {
        const string& w1 = words[i];
        const string& w2 = words[i + 1];
        size_t len = min(w1.size(), w2.size());
        size_t j = 0;
        while (j < len && w1[j] == w2[j]) ++j;
        if (j == len) {
            if (w1.size() > w2.size()) return "";
        } else if (!after[w1[j]].count(w2[j])) {
            after[w1[j]].insert(w2[j]);
            indeg[w2[j]]++;
        }
    }
    priority_queue<char, vector<char>, greater<char>> heap;
    for (char c : letters)
        if (indeg[c] == 0) heap.push(c);
    string order;
    while (!heap.empty()) {
        char c = heap.top();
        heap.pop();
        order.push_back(c);
        for (char d : after[c]) {
            if (--indeg[d] == 0) heap.push(d);
        }
    }
    if (order.size() == letters.size()) return order;
    return "";
}
```

The graph has at most 26 vertices and at most one edge per pair of neighbouring words, so building it takes time proportional to the total length of the words, and the topological sort itself is tiny.

## 5.7 Check yourself

1. In a graph with the arrows 0→1 and 1→2, what are the in-degrees of the vertices, and which vertex goes first?
2. Why does Kahn's algorithm stop with fewer than $n$ vertices when the graph has a cycle?
3. In the DFS version, why does reversing the finishing list give a valid order?
4. For the words `["ab", "ac"]`, which fact about the alphabet do we learn, and why do the letters before the difference teach us nothing?

# Chapter 6. Shortest paths with weights

## 6.1 Why BFS is not enough

Breadth-first search finds the shortest path when every edge costs the same, because it explores in layers and the first time it reaches a vertex it has used the fewest edges. When edges have different costs, the path with the fewest edges is not always the cheapest.

Take three vertices with the one-way edges 0→1 costing 5, 0→2 costing 2, and 2→1 costing 2. BFS from 0 reaches vertex 1 in a single step and stops caring. But the route 0→2→1 uses two edges and costs only 4, which beats the direct edge costing 5. We need an algorithm that always works on the vertex with the smallest **total cost so far**, not the fewest edges. That idea is Dijkstra's algorithm.

## 6.2 Dijkstra: the idea and a worked example

Dijkstra's algorithm keeps a best-known distance for every vertex: 0 for the start and infinity for the others. It repeatedly takes the unfinished vertex with the smallest best-known distance, declares that distance final, and then **relaxes** the edges leaving it. To relax an edge from `u` to `v` of cost `w` means to ask: is `dist[u] + w` smaller than the best-known `dist[v]`? If so, we have found a better route to `v`, and we update it.

Why is the smallest unfinished distance already final? Any other route to that vertex must leave the finished region through some unfinished vertex, whose distance is at least as large, and since edge costs are never negative, going further can only add to it. So no route can beat the smallest one.

Let us trace it on four vertices with the undirected edges 0-1 (cost 1), 0-2 (cost 4), 1-3 (cost 2) and 2-3 (cost 1), starting at 0.

| Step | Take vertex | Relaxations               | dist afterwards |
| ---- | ----------- | ------------------------- | --------------- |
| 0    | none        | none                      | [0, ∞, ∞, ∞]    |
| 1    | 0 (dist 0)  | 1 becomes 1, 2 becomes 4  | [0, 1, 4, ∞]    |
| 2    | 1 (dist 1)  | 3 becomes 1 + 2 = 3       | [0, 1, 4, 3]    |
| 3    | 3 (dist 3)  | 3 + 1 = 4 does not beat 4 | [0, 1, 4, 3]    |
| 4    | 2 (dist 4)  | nothing improves          | [0, 1, 4, 3]    |

To find the unfinished vertex with the smallest distance quickly we keep a **min-heap** of pairs `(distance, vertex)`. Whenever a distance improves, we push the new pair. The old, larger pair for the same vertex stays in the heap; when it is popped later its distance no longer matches `dist[vertex]`, so we simply skip it. This is exactly the problem _Dijkstra: Shortest Distances_, where unreachable vertices are reported as `-1`.

```python
import heapq

def shortest_distances(n, edges, source):
    # directed edges [a, b, w] with w >= 0; unreachable -> -1
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    INF = 10**18
    dist = [INF] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue  # an old, outdated entry
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return [-1 if d == INF else d for d in dist]

assert shortest_distances(3, [[0, 1, 4], [0, 2, 1], [2, 1, 2]], 0) == [0, 3, 1]
assert shortest_distances(3, [[1, 2, 5]], 0) == [0, -1, -1]
undirected = [[0, 1, 1], [1, 0, 1], [0, 2, 4], [2, 0, 4], [1, 3, 2], [3, 1, 2], [2, 3, 1], [3, 2, 1]]
assert shortest_distances(4, undirected, 0) == [0, 1, 4, 3]
```

```cpp
vector<long long> shortest_distances(int n, const vector<vector<int>>& edges, int source) {
    vector<vector<pair<int,int>>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back({e[1], e[2]});
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    dist[source] = 0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> heap;
    heap.push({0, source});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d != dist[u]) continue;  // an old, outdated entry
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                heap.push({dist[v], v});
            }
        }
    }
    for (auto& d : dist)
        if (d == INF) d = -1;
    return dist;
}
```

Each edge can push at most one heap entry, so the heap holds at most $m$ entries and each operation costs $O(\log m)$. The total time is $O((n+m)\log n)$ and the space is $O(n+m)$. Scanning all vertices to find the smallest each time would cost $O(n^2)$ instead, which is too slow for large sparse graphs.

## 6.3 Why Dijkstra needs non-negative weights

The argument of the previous section breaks as soon as an edge has a negative cost, because then going further can make a route cheaper. Take 0→1 costing 1, 0→2 costing 2, and 2→1 costing $-4$. Dijkstra starts at 0 and learns that vertex 1 is at distance 1 and vertex 2 at distance 2. The smaller one, vertex 1, is declared final with distance 1. Only later does it look at vertex 2 and see that 0→2→1 costs $2 - 4 = -2$, but vertex 1 is already final and is never fixed. The answer 1 is wrong. For graphs with negative edges we need Bellman-Ford (Section 6.6).

## 6.4 Minimum effort paths

Sometimes the cost of a route is not the sum of its steps but the **worst single step**. In _Path With Minimum Effort_ you walk across a grid of heights from the top-left to the bottom-right cell, and the effort of a walk is the largest height difference between two neighbouring cells on it. We want the walk with the smallest effort.

Dijkstra still works if we change just one line. Instead of the new cost `d + w`, the cost of arriving at a neighbour is `max(d, w)`, the larger of the effort so far and the new step. This cost never decreases along a walk, which is the only property the correctness argument needed. Let us trace the grid `[[1, 3], [4, 2]]`. From the start (effort 0) we can reach 3 with effort 2 or 4 with effort 3. We take the effort-2 cell first. From it the step to the bottom-right 2 has difference 1, so the effort there is $\max(2, 1) = 2$. When we take that cell, we are done: the answer is 2, and the other route (effort 3) is never needed. This is exactly the problem _Path With Minimum Effort_.

```python
import heapq

def minimum_effort_path(heights):
    R, C = len(heights), len(heights[0])
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    INF = 10**18
    best = [[INF] * C for _ in range(R)]
    best[0][0] = 0
    heap = [(0, 0, 0)]  # (effort, row, col)
    while heap:
        effort, r, c = heapq.heappop(heap)
        if effort != best[r][c]:
            continue
        if r == R - 1 and c == C - 1:
            return effort
        for k in range(4):
            nr, nc = r + DR[k], c + DC[k]
            if 0 <= nr < R and 0 <= nc < C:
                ne = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if ne < best[nr][nc]:
                    best[nr][nc] = ne
                    heapq.heappush(heap, (ne, nr, nc))
    return -1

assert minimum_effort_path([[1, 3], [4, 2]]) == 2
assert minimum_effort_path([[7]]) == 0
assert minimum_effort_path([[1, 10, 6, 7, 9, 10, 4, 9]]) == 9
```

```cpp
int minimum_effort_path(const vector<vector<int>>& heights) {
    int R = heights.size(), C = heights[0].size();
    int DR[4] = {-1, 0, 1, 0};
    int DC[4] = {0, 1, 0, -1};
    const int INF = INT_MAX;
    vector<vector<int>> best(R, vector<int>(C, INF));
    best[0][0] = 0;
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> heap;
    heap.push({0, 0, 0});  // (effort, row, col)
    while (!heap.empty()) {
        auto [effort, r, c] = heap.top();
        heap.pop();
        if (effort != best[r][c]) continue;
        if (r == R - 1 && c == C - 1) return effort;
        for (int k = 0; k < 4; ++k) {
            int nr = r + DR[k], nc = c + DC[k];
            if (0 <= nr && nr < R && 0 <= nc && nc < C) {
                int ne = max(effort, abs(heights[nr][nc] - heights[r][c]));
                if (ne < best[nr][nc]) {
                    best[nr][nc] = ne;
                    heap.push({ne, nr, nc});
                }
            }
        }
    }
    return -1;
}
```

The grid has $R \cdot C$ vertices, so the time is $O(RC \log (RC))$ and the space is $O(RC)$.

_Swim in Rising Water_ is the same idea with a different step cost. The water level rises with time, and you may enter a cell once the level reaches its height. So a walk needs time equal to the **largest height it touches**, including the starting cell. The cost of arriving at a neighbour is therefore `max(time so far, height of the neighbour)`, and we want the smallest such time for reaching the bottom-right corner. On `[[0, 2], [1, 3]]` the start has time 0, the neighbour 1 costs time 1 and the neighbour 2 costs time 2; from the cell with 1 the corner costs $\max(1, 3) = 3$, and from 2 also 3. The answer is 3. This is exactly the problem _Swim in Rising Water_.

```python
def swim_in_water(grid):
    R, C = len(grid), len(grid[0])
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    INF = 10**18
    best = [[INF] * C for _ in range(R)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if t != best[r][c]:
            continue
        if r == R - 1 and c == C - 1:
            return t
        for k in range(4):
            nr, nc = r + DR[k], c + DC[k]
            if 0 <= nr < R and 0 <= nc < C:
                nt = max(t, grid[nr][nc])
                if nt < best[nr][nc]:
                    best[nr][nc] = nt
                    heapq.heappush(heap, (nt, nr, nc))
    return -1

assert swim_in_water([[0, 2], [1, 3]]) == 3
assert swim_in_water([[0]]) == 0
assert swim_in_water([[3, 2], [0, 1]]) == 3
```

```cpp
int swim_in_water(const vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size();
    int DR[4] = {-1, 0, 1, 0};
    int DC[4] = {0, 1, 0, -1};
    const int INF = INT_MAX;
    vector<vector<int>> best(R, vector<int>(C, INF));
    best[0][0] = grid[0][0];
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> heap;
    heap.push({grid[0][0], 0, 0});
    while (!heap.empty()) {
        auto [t, r, c] = heap.top();
        heap.pop();
        if (t != best[r][c]) continue;
        if (r == R - 1 && c == C - 1) return t;
        for (int k = 0; k < 4; ++k) {
            int nr = r + DR[k], nc = c + DC[k];
            if (0 <= nr && nr < R && 0 <= nc && nc < C) {
                int nt = max(t, grid[nr][nc]);
                if (nt < best[nr][nc]) {
                    best[nr][nc] = nt;
                    heap.push({nt, nr, nc});
                }
            }
        }
    }
    return -1;
}
```

## 6.5 Counting shortest paths

How many different routes achieve the shortest distance? While Dijkstra runs, keep a second array `ways`, where `ways[v]` is the number of shortest routes found so far to `v`. When a relaxation finds a **strictly shorter** distance to `v` through `u`, all earlier routes are obsolete, so `ways[v]` becomes `ways[u]`. When it finds an **equal** distance, we have found additional routes, so `ways[u]` is added to `ways[v]`. Because every road takes at least 1 unit of time, `u` is finished before any vertex that is reached through it, so `ways[u]` is complete at the moment we use it. (With zero-length edges this argument would fail.)

Take five vertices with the roads 0-1, 0-2, 1-3, 2-3, 3-4, each taking time 1, and one long road 0-4 taking time 10. The distances from 0 are 0, 1, 1, 2, 3. Vertex 3 can be reached through 1 or through 2, both at distance 2, so `ways[3] = 1 + 1 = 2`. Vertex 4 is reached from 3 at distance 3 (better than the long road, which costs 10), so `ways[4] = 2`. This is exactly the problem _Number of Shortest Paths_, where the count is taken modulo $10^9+7$ because it can be huge.

```python
import heapq

def count_shortest_paths(n, roads):
    MOD = 10**9 + 7
    adj = [[] for _ in range(n)]
    for a, b, t in roads:
        adj[a].append((b, t))
        adj[b].append((a, t))
    INF = 10**18
    dist = [INF] * n
    ways = [0] * n
    dist[0] = 0
    ways[0] = 1
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, t in adj[u]:
            if d + t < dist[v]:
                dist[v] = d + t
                ways[v] = ways[u]
                heapq.heappush(heap, (dist[v], v))
            elif d + t == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n - 1]

roads = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]]
assert count_shortest_paths(5, roads) == 2
assert count_shortest_paths(1, []) == 1
assert count_shortest_paths(2, []) == 0
```

```cpp
int count_shortest_paths(int n, const vector<vector<int>>& roads) {
    const int MOD = 1'000'000'007;
    vector<vector<pair<int,int>>> adj(n);
    for (auto& r : roads) {
        adj[r[0]].push_back({r[1], r[2]});
        adj[r[1]].push_back({r[0], r[2]});
    }
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    vector<int> ways(n, 0);
    dist[0] = 0;
    ways[0] = 1;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> heap;
    heap.push({0, 0});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d != dist[u]) continue;
        for (auto [v, t] : adj[u]) {
            if (d + t < dist[v]) {
                dist[v] = d + t;
                ways[v] = ways[u];
                heap.push({dist[v], v});
            } else if (d + t == dist[v]) {
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }
    return ways[n - 1];
}
```

The time is $O((n+m)\log n)$ and the space is $O(n+m)$. Chapter 10 shows the same idea as a dynamic program over the shortest-path graph.

## 6.6 Bellman-Ford and negative weights

Bellman-Ford handles negative edges with a very simple loop: **scan all edges and relax each one, and repeat**. A shortest path never needs more than $n-1$ edges (a longer one would revisit a vertex, which can be cut out without raising the cost, if there is no negative cycle). After round $i$, every shortest path using at most $i$ edges has been found, so after $n-1$ rounds all distances are correct.

Trace it on the edges 0→1 (cost 4), 0→2 (cost 5) and 2→1 (cost $-3$), scanned in this order from vertex 0. Round 1: `dist[1]` becomes 4, `dist[2]` becomes 5, then the edge 2→1 gives $5 - 3 = 2$, which beats 4, so `dist[1]` becomes 2. Round 2 changes nothing, so we stop with `[0, 2, 5]`.

A **negative cycle** is a cycle whose costs add up to less than zero; going around it again and again lowers the cost forever, so shortest distances do not exist. If a negative cycle is reachable from the start, relaxation never settles, and some edge still relaxes in round $n$. So: if round $n$ still changes something, report the negative cycle. In this sheet problem we return an empty list for it, and `None` for unreachable vertices. This is exactly the problem _Bellman-Ford With Negative Edges_.

```python
def bellman_ford(n, edges, source):
    INF = 10**18
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n):
        changed = False
        for a, b, w in edges:
            if dist[a] != INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                changed = True
        if not changed:
            break
    else:
        return []  # still changing in round n: a negative cycle is reachable
    return [None if d == INF else d for d in dist]

assert bellman_ford(3, [[0, 1, 4], [0, 2, 5], [2, 1, -3]], 0) == [0, 2, 5]
assert bellman_ford(3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0) == []
assert bellman_ford(3, [[1, 2, -5]], 0) == [0, None, None]
```

```cpp
vector<optional<long long>> bellman_ford(int n, const vector<vector<int>>& edges, int source) {
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    dist[source] = 0;
    bool settled = false;
    for (int round = 0; round < n; ++round) {
        bool changed = false;
        for (auto& e : edges) {
            int a = e[0], b = e[1], w = e[2];
            if (dist[a] != INF && dist[a] + w < dist[b]) {
                dist[b] = dist[a] + w;
                changed = true;
            }
        }
        if (!changed) {
            settled = true;
            break;
        }
    }
    if (!settled) return {};  // a negative cycle is reachable
    vector<optional<long long>> result(n);
    for (int v = 0; v < n; ++v)
        if (dist[v] != INF) result[v] = dist[v];
    return result;
}
```

The time is $O(n \cdot m)$ and the space is $O(n)$. Notice the `dist[a] != INF` test: without it, the sum `INF + w` with a negative `w` would look like a real distance.

## 6.7 Cheapest flights within K stops

In _Cheapest Flights Within K Stops_ we want the cheapest trip from a source to a destination that uses at most $k$ stops in between, which means at most $k+1$ flights. Plain Dijkstra fails here: the cheapest route may need too many flights, and a pricier route with fewer flights is the one allowed.

Bellman-Ford fits perfectly, because after round $i$ it knows the cheapest cost using **at most $i$ edges**. We simply run exactly $k+1$ rounds. There is one catch: in each round we must relax using the distances of the **previous** round only, otherwise one round could chain several flights together. So we write the new distances into a copy.

Take four cities with the flights 0→1 (10), 1→2 (10), 2→3 (10) and 0→3 (100), going from 0 to 3. After round 1 (one flight) the distances are `[0, 10, ∞, 100]`. After round 2 they are `[0, 10, 20, 100]`. After round 3 they are `[0, 10, 20, 30]`. So with $k = 1$ (two flights) the answer is 100, and with $k = 2$ it is 30. This is exactly the problem _Cheapest Flights Within K Stops_.

```python
def cheapest_price(n, flights, src, dst, k):
    INF = 10**18
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        new = dist[:]
        for a, b, price in flights:
            if dist[a] != INF and dist[a] + price < new[b]:
                new[b] = dist[a] + price
        dist = new
    return -1 if dist[dst] == INF else dist[dst]

flights = [[0, 1, 10], [1, 2, 10], [2, 3, 10], [0, 3, 100]]
assert cheapest_price(4, flights, 0, 3, 1) == 100
assert cheapest_price(4, flights, 0, 3, 2) == 30
assert cheapest_price(4, flights, 3, 0, 3) == -1
```

```cpp
int cheapest_price(int n, const vector<vector<int>>& flights, int src, int dst, int k) {
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    dist[src] = 0;
    for (int round = 0; round <= k; ++round) {
        vector<long long> next = dist;
        for (auto& f : flights) {
            int a = f[0], b = f[1], price = f[2];
            if (dist[a] != INF && dist[a] + price < next[b])
                next[b] = dist[a] + price;
        }
        dist = next;
    }
    return dist[dst] == INF ? -1 : (int)dist[dst];
}
```

The time is $O(k \cdot m)$ and the space is $O(n)$. Another way to see the same problem is to let the vertex of a Dijkstra search be the pair (city, flights used so far). Chapter 11 shows that idea.

## 6.8 Floyd-Warshall: all pairs

Sometimes we need the shortest distance between **every** pair of vertices. Floyd-Warshall keeps a table `dist[i][j]`, starting with 0 on the diagonal, the edge cost where an edge exists, and infinity elsewhere. Then it allows the vertices as stopovers one at a time. After deciding the vertices $0, 1, \dots, k$ may be used as stopovers, `dist[i][j]` is the shortest distance from `i` to `j` using only those as intermediate vertices. Allowing vertex $k$ means trying, for every pair, the route through it:

$$\text{dist}[i][j] = \min(\text{dist}[i][j],\ \text{dist}[i][k] + \text{dist}[k][j])$$

Take the edges 0→1 (cost 2), 1→2 (cost 3) and 0→2 (cost 10). Initially `dist[0][2]` is 10. Allowing vertex 0 as stopover changes nothing (nothing points into 0). Allowing vertex 1 finds the route $0 \to 1 \to 2$ costing $2 + 3 = 5$, which beats 10. Allowing vertex 2 changes nothing. So `dist[0][2] = 5`. The outer loop over $k$ must be outermost, which is the most common mistake. This is exactly the problem _Floyd-Warshall: All Pairs_, where unreachable pairs are reported as `-1`.

```python
def all_pairs_shortest(n, edges):
    INF = 10**18
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for a, b, w in edges:
        dist[a][b] = min(dist[a][b], w)
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return [[-1 if d >= INF else d for d in row] for row in dist]

assert all_pairs_shortest(3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]]) == [[0, 4, 5], [-1, 0, 1], [-1, -1, 0]]
assert all_pairs_shortest(2, []) == [[0, -1], [-1, 0]]
assert all_pairs_shortest(3, [[0, 1, 2], [1, 2, 3], [0, 2, 10]])[0][2] == 5
```

```cpp
vector<vector<long long>> all_pairs_shortest(int n, const vector<vector<int>>& edges) {
    const long long INF = (long long)1e18;
    vector<vector<long long>> dist(n, vector<long long>(n, INF));
    for (int i = 0; i < n; ++i) dist[i][i] = 0;
    for (auto& e : edges) dist[e[0]][e[1]] = min(dist[e[0]][e[1]], (long long)e[2]);
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; ++j)
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
        }
    for (auto& row : dist)
        for (auto& d : row)
            if (d >= INF) d = -1;
    return dist;
}
```

The three loops give a time of $O(n^3)$, and the table takes $O(n^2)$ space. We skip rows where `dist[i][k]` is infinite, and an unreachable `dist[k][j]` equals $10^{18}$, so the sum can never beat a real distance. With negative edges (but no negative cycles) the same code still works, and a negative number on the diagonal `dist[i][i]` reveals a negative cycle through `i`.

## 6.9 Check yourself

1. In the worked Dijkstra table, why is vertex 3 taken before vertex 2 in step 3?
2. Give a three-vertex graph with a negative edge on which Dijkstra gives the wrong answer.
3. In the minimum-effort variation, why can we replace "add the edge cost" by "take the larger of the two"?
4. In cheapest flights, why do we write the new distances into a copy of the array?
5. In Floyd-Warshall, why must the loop over the stopover vertex be the outermost loop?

# Chapter 7. Disjoint sets (union-find)

## 7.1 Groups that keep merging

Picture a school on the first day. Nobody knows anybody, so every student is in a group of one. As days pass, friendships form and groups merge: when Asha befriends Ben, Asha's whole group and Ben's whole group become one big group. At any moment we want to answer one question quickly: **are these two students in the same group?**

The data structure built for exactly this is called a **disjoint set union**, or **DSU**, and also **union-find**. "Disjoint" means that no student belongs to two groups at once. It supports two actions. `find(x)` tells us which group `x` is in, and `union(a, b)` merges the group of `a` with the group of `b`.

Graphs fit this picture perfectly. Vertices are the students, and an edge is a friendship that merges two groups. After adding some edges, the groups are exactly the connected components we met in Chapter 1.

## 7.2 The parent array

We give every group a **leader**, one chosen member who stands for the whole group. Every vertex stores a `parent`. A leader is its own parent. Everyone else points to someone closer to the leader, so following parents always ends at the leader. `find(x)` follows the parents until it meets a vertex that is its own parent. `union(a, b)` finds both leaders and makes one of them the parent of the other.

```python
def make_sets(n):
    return list(range(n))

def find(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x

def union(parent, a, b):
    a, b = find(parent, a), find(parent, b)
    if a != b:
        parent[b] = a

parent = make_sets(5)
union(parent, 0, 1)
union(parent, 3, 4)
assert find(parent, 1) == find(parent, 0)
assert find(parent, 0) != find(parent, 3)
union(parent, 1, 4)
assert find(parent, 0) == find(parent, 3)
```

```cpp
vector<int> make_sets(int n) {
    vector<int> parent(n);
    iota(parent.begin(), parent.end(), 0);
    return parent;
}

int find(vector<int>& parent, int x) {
    while (parent[x] != x) x = parent[x];
    return x;
}

void unite(vector<int>& parent, int a, int b) {
    a = find(parent, a);
    b = find(parent, b);
    if (a != b) parent[b] = a;
}
```

This works, but it can become slow. If we keep attaching a long chain of vertices under each other, the chain grows tall, and every `find` has to walk along the whole chain. In the worst case one `find` costs $O(n)$.

## 7.3 Two tricks that make it fast

The first trick is **path compression**. After `find` has walked up to the leader, we make every vertex on the way point directly at the leader. The next `find` from any of them takes a single step. We pay a little extra now and save a lot later.

The second trick is **union by size**. When merging two groups, we hang the smaller group under the leader of the bigger one. That way the trees stay short, because a vertex only moves one level deeper when its group at least doubles in size, and that can happen only about $\log_2 n$ times.

Together, the two tricks make each operation take almost constant time, formally $O(\alpha(n))$, where $\alpha$ grows so slowly that it stays below 5 for any input you can ever store. We will treat each operation as $O(1)$. Below is the version we will use for the rest of this chapter. It also keeps the group sizes and the number of groups, and `union` tells us whether it actually merged two different groups.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.groups -= 1
        return True

d = DSU(6)
assert d.union(0, 1) and d.union(1, 2)
assert not d.union(0, 2)
assert d.groups == 4
assert d.size[d.find(0)] == 3
```

```cpp
struct DSU {
    vector<int> parent, size;
    int groups;

    DSU(int n) : parent(n), size(n, 1), groups(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        groups--;
        return true;
    }
};
```

## 7.4 Spotting cycles

The code in the rest of this chapter uses the `DSU` class from Section 7.3.

Here is the most useful fact about union-find. Suppose we add the edges of a graph one by one. If an edge joins two vertices that are **already in the same group**, then those two vertices were already connected by a path, and the new edge closes a **cycle**. If the edge joins two different groups, it just merges them. Our `union` function returns `False` exactly in the first case, so cycle detection is one line.

This is the heart of _Redundant Connection_. The input is a tree with one extra edge, and we must return the edge that can be removed, choosing the last one if there are several. We add the edges in the given order. The first edge whose ends are already in the same group is the one that closes the cycle, and it is the last edge of that cycle in the list.

```python
def first_cycle_edge(n, edges):
    dsu = DSU(n + 1)  # vertices are numbered from 1
    for a, b in edges:
        if not dsu.union(a, b):
            return [a, b]
    return None

assert first_cycle_edge(3, [[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert first_cycle_edge(4, [[1, 2], [2, 3], [3, 4], [1, 4]]) == [1, 4]
assert first_cycle_edge(3, [[1, 2], [2, 3]]) is None
```

```cpp
vector<int> first_cycle_edge(int n, const vector<vector<int>>& edges) {
    DSU dsu(n + 1);
    for (auto& e : edges)
        if (!dsu.unite(e[0], e[1])) return e;
    return {};
}
```

_Is Graph a Tree_ asks whether a graph is connected and has no cycle. A tree on $n$ vertices has exactly $n-1$ edges, so we can check that the number of edges is $n-1$ and that every union succeeded (no cycle). Then the graph is connected too, because $n-1$ edges that never closed a cycle must have merged all $n$ vertices into one group.

_Connect the Network_ has a different flavour. We have $n$ computers and some cables, and we may move a cable that is not needed to join two separate groups. The number of groups tells us how many joins we need: to connect $g$ groups we need $g-1$ extra cables. The cables that closed a cycle during the union step are exactly the spare ones, so the answer is $g-1$ if at least that many spares exist, and $-1$ otherwise. Counting is even simpler: we need at least $n-1$ cables overall.

```python
def operations_to_connect(n, connections):
    if len(connections) < n - 1:
        return -1
    dsu = DSU(n)
    for a, b in connections:
        dsu.union(a, b)
    return dsu.groups - 1

assert operations_to_connect(4, [[0, 1], [0, 2], [1, 2]]) == 1
assert operations_to_connect(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
assert operations_to_connect(3, [[0, 1], [1, 2]]) == 0
```

```cpp
int operations_to_connect(int n, const vector<vector<int>>& connections) {
    if ((int)connections.size() < n - 1) return -1;
    DSU dsu(n);
    for (auto& c : connections) dsu.unite(c[0], c[1]);
    return dsu.groups - 1;
}
```

## 7.5 Grouping by a rule

Union-find is not only for graphs that are given as edges. Whenever a rule says "these two things belong together", we can call `union` and let the groups form by themselves.

In _Satisfiability of Equality Equations_ every equation is either `a==b` or `a!=b`. Equal variables must be in the same group, so we first read all the `==` equations and union the two letters. After that, every `!=` equation must connect letters from different groups. If we ever see `a!=b` with `a` and `b` in the same group, the equations contradict each other.

```python
def equations_possible(equations):
    dsu = DSU(26)
    for eq in equations:
        if eq[1] == "=":
            dsu.union(ord(eq[0]) - 97, ord(eq[3]) - 97)
    for eq in equations:
        if eq[1] == "!" and dsu.find(ord(eq[0]) - 97) == dsu.find(ord(eq[3]) - 97):
            return False
    return True

assert equations_possible(["a==b", "b==c", "a==c"])
assert not equations_possible(["a==b", "b!=a"])
assert equations_possible(["a==b", "b!=c", "c==a"]) is False
```

```cpp
bool equations_possible(const vector<string>& equations) {
    DSU dsu(26);
    for (auto& eq : equations)
        if (eq[1] == '=') dsu.unite(eq[0] - 'a', eq[3] - 'a');
    for (auto& eq : equations)
        if (eq[1] == '!' && dsu.find(eq[0] - 'a') == dsu.find(eq[3] - 'a')) return false;
    return true;
}
```

In _Most Stones Removed_ a stone may be removed if another stone remains in its row or column. Stones that share a row or a column belong together, and the rule chains: a stone linked to a stone that is linked to a third one is in the same group. So we want the groups, and inside each group we can remove all stones but one. The trick that makes it easy is to turn each stone `(x, y)` into an edge between a "row vertex" `x` and a "column vertex" `y`. We shift the column numbers so they do not collide with row numbers, for example by using the vertex `y + 10001`. A group of stones becomes one group of rows and columns. The answer is the number of stones minus the number of groups that contain at least one stone.

```python
def removable_stones(stones):
    dsu = DSU(20002)
    used = set()
    for x, y in stones:
        dsu.union(x, y + 10001)
        used.add(x)
    roots = {dsu.find(x) for x in used}
    return len(stones) - len(roots)

assert removable_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]) == 5
assert removable_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]) == 3
assert removable_stones([[0, 0]]) == 0
```

```cpp
int removable_stones(const vector<vector<int>>& stones) {
    DSU dsu(20002);
    set<int> used;
    for (auto& s : stones) {
        dsu.unite(s[0], s[1] + 10001);
        used.insert(s[0]);
    }
    set<int> roots;
    for (int x : used) roots.insert(dsu.find(x));
    return (int)stones.size() - (int)roots.size();
}
```

## 7.6 Sizes live at the leader

Our `DSU` keeps `size` at the leader of each group, so the size of the group of any vertex is `dsu.size[dsu.find(v)]`. This helps in _Making a Large Island_. The grid has water (`0`) and land (`1`), and we may turn one water cell into land. We want the largest island we can end up with.

First we group the land cells. For every land cell we union it with its land neighbours, so each island becomes one group, and its size is stored at its leader. Then we try every water cell. Looking at its four neighbours, we collect the **different** island leaders (a set removes duplicates, because one island can touch the water cell from two sides). Flipping this cell joins all those islands, plus the cell itself, so the new island has size $1 + {}$the sum of their sizes. The answer is the best value over all water cells, or the biggest existing island if there is no water.

```python
def largest_island(grid):
    n, m = len(grid), len(grid[0])
    dsu = DSU(n * m)
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 1:
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
                        dsu.union(r * m + c, nr * m + nc)
    best = max((dsu.size[dsu.find(r * m + c)]
                for r in range(n) for c in range(m) if grid[r][c] == 1), default=0)
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 0:
                roots = set()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
                        roots.add(dsu.find(nr * m + nc))
                best = max(best, 1 + sum(dsu.size[x] for x in roots))
    return best

assert largest_island([[1, 0], [0, 1]]) == 3
assert largest_island([[1, 1], [1, 1]]) == 4
assert largest_island([[0, 0], [0, 0]]) == 1
```

```cpp
int largest_island(vector<vector<int>>& grid) {
    int n = grid.size(), m = grid[0].size();
    DSU dsu(n * m);
    int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++)
            if (grid[r][c] == 1)
                for (int k = 0; k < 4; k++) {
                    int nr = r + dr[k], nc = c + dc[k];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < m && grid[nr][nc] == 1)
                        dsu.unite(r * m + c, nr * m + nc);
                }
    int best = 0;
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++)
            if (grid[r][c] == 1) best = max(best, dsu.size[dsu.find(r * m + c)]);
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++)
            if (grid[r][c] == 0) {
                set<int> roots;
                for (int k = 0; k < 4; k++) {
                    int nr = r + dr[k], nc = c + dc[k];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < m && grid[nr][nc] == 1)
                        roots.insert(dsu.find(nr * m + nc));
                }
                int total = 1;
                for (int x : roots) total += dsu.size[x];
                best = max(best, total);
            }
    return best;
}
```

The whole thing runs in about $O(nm)$ time, since every cell does a constant number of union and find calls.

## 7.7 Check yourself

1. Why does a `union` that returns `False` prove that the new edge closes a cycle?
2. In the parent-array version, what kind of input makes `find` slow, and which trick fixes it?
3. In _Connect the Network_, why is the answer the number of groups minus one, and when is it impossible?
4. In _Most Stones Removed_, why do we shift the column numbers by 10001 before calling `union`?

# Chapter 8. Minimum spanning trees

## 8.1 What a spanning tree is

Suppose a company must lay cables so that four offices are all connected, directly or through other offices. Every possible cable has a price. We do not need cables that loop around, because a loop wastes money: one of its cables could be removed and everyone would still be connected. So the cheapest plan is always a **tree**.

A **spanning tree** of a connected graph is a set of edges that touches every vertex, keeps the graph connected, and contains no cycle. For $n$ vertices it always uses exactly $n-1$ edges. A **minimum spanning tree**, or **MST**, is a spanning tree whose total weight is as small as possible. This is exactly the problem _Minimum Spanning Tree_. If the graph is not connected, no spanning tree exists.

There are two classic ways to build one, and both are greedy: they keep choosing the cheapest option that is safe.

## 8.2 Kruskal: cheapest edge first

**Kruskal's algorithm** looks at all edges from the cheapest to the most expensive. It takes an edge if it joins two vertices that are not yet connected, and skips it if it would close a cycle. We already have the perfect tool to check this: the union-find structure from Chapter 7. To keep this chapter self-contained, here is its short form again (path compression and union by size). `union` returns `False` exactly when the two vertices are already in the same group, that is, when an edge would close a cycle.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.groups -= 1
        return True

d = DSU(3)
assert d.union(0, 1) and not d.union(1, 0)
assert d.groups == 2
```

```cpp
struct DSU {
    vector<int> parent, size;
    int groups;

    DSU(int n) : parent(n), size(n, 1), groups(n) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        groups--;
        return true;
    }
};
```

Let us trace it on four vertices 0, 1, 2, 3 with the edges (0,1) weight 1, (1,2) weight 2, (0,2) weight 3, (2,3) weight 4 and (1,3) weight 5. Sorted by weight, the order is already the order we listed them.

We take (0,1): the groups were {0}, {1}, so it joins them. We take (1,2): it joins {0,1} with {2}. Next is (0,2) with weight 3, but 0 and 2 are already in the same group, so this edge would close a cycle and we skip it. We take (2,3): it joins {0,1,2} with {3}. Now we have $3 = n-1$ edges, so we stop. The tree is (0,1), (1,2), (2,3) with total weight $1+2+4=7$.

```python
def kruskal(n, edges):
    dsu = DSU(n)
    total = 0
    for a, b, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(a, b):
            total += w
    return total if dsu.groups == 1 else -1

edges = [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]]
assert kruskal(4, edges) == 7
assert kruskal(4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 5]]) == 6
assert kruskal(4, [[0, 1, 1], [2, 3, 1]]) == -1
assert kruskal(1, []) == 0
```

```cpp
long long kruskal(int n, vector<vector<int>> edges) {
    sort(edges.begin(), edges.end(), [](auto& x, auto& y) { return x[2] < y[2]; });
    DSU dsu(n);
    long long total = 0;
    for (auto& e : edges)
        if (dsu.unite(e[0], e[1])) total += e[2];
    return dsu.groups == 1 ? total : -1;
}
```

Sorting the $m$ edges costs $O(m \log m)$ and the union-find work is almost free, so Kruskal runs in $O(m \log m)$ time. At the end, if more than one group is left, the graph was not connected and we return $-1$.

## 8.3 Prim: grow one tree

**Prim's algorithm** works differently. It starts from one vertex and grows a single tree. At every step it looks at all edges that leave the tree, picks the cheapest one, and adds the new vertex at its other end. To find the cheapest leaving edge quickly we use a **min-heap**, a structure that always hands us the smallest item first.

Let us use the same graph and start at vertex 0. The edges leaving $\{0\}$ are (0,1) with weight 1 and (0,2) with weight 3. The cheapest is (0,1), so vertex 1 joins the tree. Now the leaving edges are (0,2) weight 3, (1,2) weight 2 and (1,3) weight 5. The cheapest is (1,2), so vertex 2 joins. The leaving edges are now (2,3) weight 4 and (1,3) weight 5, and the edge (0,2) leads back into the tree, so it is ignored. We take (2,3) with weight 4. Total: $1+2+4=7$, the same tree as before.

```python
import heapq

def prim(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((w, b))
        adj[b].append((w, a))
    seen = [False] * n
    heap = [(0, 0)]
    total = 0
    count = 0
    while heap:
        w, v = heapq.heappop(heap)
        if seen[v]:
            continue
        seen[v] = True
        total += w
        count += 1
        for item in adj[v]:
            if not seen[item[1]]:
                heapq.heappush(heap, item)
    return total if count == n else -1

edges = [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]]
assert prim(4, edges) == 7
assert prim(4, [[0, 1, 1], [2, 3, 1]]) == -1
assert prim(1, []) == 0
```

```cpp
long long prim(int n, const vector<vector<int>>& edges) {
    vector<vector<pair<int, int>>> adj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back({e[2], e[1]});
        adj[e[1]].push_back({e[2], e[0]});
    }
    vector<bool> seen(n, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    pq.push({0, 0});
    long long total = 0;
    int count = 0;
    while (!pq.empty()) {
        auto [w, v] = pq.top();
        pq.pop();
        if (seen[v]) continue;
        seen[v] = true;
        total += w;
        count++;
        for (auto [w2, u] : adj[v])
            if (!seen[u]) pq.push({w2, u});
    }
    return count == n ? total : -1;
}
```

With the heap, Prim runs in $O(m \log m)$ time, the same as Kruskal. As a rule of thumb, Kruskal is easier when the edges come as a list, and Prim is nicer when the graph is dense.

## 8.4 Why the greedy choice is safe

Why can we trust "always take the cheapest edge"? Here is the idea. Split the vertices into two non-empty groups, any way you like. At least one edge of the final tree must cross between the two groups, or the tree would not connect them. If you look at the cheapest edge crossing the split, there is always a minimum spanning tree that contains it: if some tree used a more expensive crossing edge instead, swapping it for the cheaper one keeps the tree connected and does not cost more. Kruskal and Prim are both just two ways of repeatedly picking such a safe edge.

## 8.5 Points on a plane

In _Min Cost to Connect All Points_ we get points on a plane, and connecting two points costs their **Manhattan distance**, $|x_1-x_2|+|y_1-y_2|$. Any two points can be connected, so the graph has an edge between every pair. With $n$ points that is about $n^2/2$ edges, so building and sorting them all for Kruskal costs $O(n^2 \log n)$.

For a graph with so many edges, Prim without a heap is nicer. We keep, for every point not yet in the tree, the cheapest distance to the tree so far. At each step we take the point with the smallest value and then update the others. This needs only $O(n^2)$ time and $O(n)$ space, because we never store the edges at all.

```python
def min_cost_connect(points):
    n = len(points)
    INF = float("inf")
    best = [INF] * n
    best[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        v = -1
        for i in range(n):
            if not used[i] and (v == -1 or best[i] < best[v]):
                v = i
        used[v] = True
        total += best[v]
        for u in range(n):
            if not used[u]:
                d = abs(points[v][0] - points[u][0]) + abs(points[v][1] - points[u][1])
                if d < best[u]:
                    best[u] = d
    return total

assert min_cost_connect([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
assert min_cost_connect([[3, 12], [-2, 5], [-4, 1]]) == 18
assert min_cost_connect([[0, 0]]) == 0
```

```cpp
int min_cost_connect(const vector<vector<int>>& points) {
    int n = points.size();
    vector<int> best(n, INT_MAX);
    vector<bool> used(n, false);
    best[0] = 0;
    int total = 0;
    for (int step = 0; step < n; step++) {
        int v = -1;
        for (int i = 0; i < n; i++)
            if (!used[i] && (v == -1 || best[i] < best[v])) v = i;
        used[v] = true;
        total += best[v];
        for (int u = 0; u < n; u++)
            if (!used[u]) {
                int d = abs(points[v][0] - points[u][0]) + abs(points[v][1] - points[u][1]);
                best[u] = min(best[u], d);
            }
    }
    return total;
}
```

## 8.6 Check yourself

1. How many edges does a spanning tree of a connected graph with 10 vertices have?
2. In Kruskal's algorithm, what does it mean when `union` returns `False`, and what do we do with the edge?
3. In the trace of Prim above, why was the edge (0,2) ignored once vertices 0 and 2 were both in the tree?
4. Why is Prim without a heap a good choice when every pair of points is connected?

# Chapter 9. Bridges, cut vertices and strongly connected components

## 9.1 Weak spots in a network

Picture towns joined by roads. A **bridge** is a road whose closure leaves some pair of towns with no route between them. A **cut vertex** (also called an **articulation point**) is a town whose disappearance, together with every road touching it, splits the remaining towns into more separate pieces than before. These are the weak spots of a network: a single cable or a single server that everything depends on. Both ideas are about undirected graphs.

The test is not obvious from a picture of a big graph, so we use depth-first search with the entry times of Chapter 3. DFS builds a **DFS tree**: the edges along which it walked into new vertices. Every other edge of an undirected graph is a **back edge** that joins a vertex to one of its ancestors in the tree. A back edge is a shortcut around part of the tree, and bridges are exactly the tree edges that no shortcut covers.

Take this graph with the edges 0-1, 1-2, 0-3, 3-4 and 1-4.

```
0 --- 1 --- 2
|     |
3 --- 4
```

Vertices 0, 1, 4, 3 form a cycle, so none of its edges is a bridge, while the road to vertex 2 is the only way in or out of it, so 1-2 is a bridge. Vertex 1 is a cut vertex, because removing it cuts 2 off from the rest, and no other vertex is. The rest of the chapter finds such things automatically.

## 9.2 Entry times and low-link values

During DFS we number every vertex with its entry time `tin[v]`. For every vertex we also compute `low[v]`: **the smallest entry time that can be reached from `v`'s subtree by walking down tree edges and then using at most one back edge.** Think of it as "how high up the tree can this subtree climb by shortcut". It starts as `tin[v]` itself, and then it is lowered by two kinds of events. If `v` has a back edge to an already visited vertex `u` (other than its parent), then `low[v]` becomes at most `tin[u]`. And when we come back from a child `c`, then `low[v]` becomes at most `low[c]`, because whatever the child's subtree can reach, so can `v`'s.

Now the tests are short. A tree edge from `v` to its child `c` is a **bridge** exactly when $low[c] > tin[v]$, meaning the subtree of `c` cannot reach `v` or anything above it except through this very edge. A non-root vertex `v` is a **cut vertex** when some child `c` has $low[c] \ge tin[v]$, meaning that subtree cannot get above `v` without passing through `v` itself (it may touch `v` by a back edge, which is still not enough to escape). The root of the DFS tree is special, because it has no "above". It is a cut vertex exactly when it has two or more children in the DFS tree.

Let us trace the graph above, starting at 0, and visiting neighbours in the order they were listed. Vertex 0 gets `tin = low = 0`. We go to 1 (`tin = low = 1`), then to 2 (`tin = low = 2`). Vertex 2 has no other edges, so we return to 1 with `low[2] = 2`, which is greater than `tin[1] = 1`: the edge 1-2 is a bridge, and since $low[2] \ge tin[1]$ and 1 is not the root, vertex 1 is a cut vertex. Next 1 goes to 4 (`tin = low = 3`), and 4 goes to 3 (`tin = low = 4`). Vertex 3 sees its neighbour 0, which is already visited and is not its parent, so `low[3] = 0`. Returning, `low[4]` becomes 0, then `low[1]` becomes 0. For the child 4 of vertex 1, $low[4] = 0 < tin[1]$, so it does not make 1 a cut vertex, and the edge 1-4 is not a bridge. Finally the edge 0-1 is not a bridge since $low[1] = 0 \not> tin[0] = 0$, and the root 0 has only one child. The bridges are just 1-2 and the cut vertices just 1.

All of this takes one DFS, so the time is $O(n+m)$. (In Python, a very deep graph can overflow the recursion limit. Then use the explicit-stack DFS of Section 3.5. The logic is identical.)

## 9.3 Critical connections

A **critical connection** is simply a bridge. The code below computes `tin` and `low` as described and collects each tree edge `(v, to)` with $low[to] > tin[v]$. We skip the edge back to the parent, since it is the same road we arrived by (the problem guarantees that there are no repeated roads). Each bridge is reported as a pair `[a, b]` with `a < b`, in sorted order. This is exactly the problem _Critical Connections (Bridges)_.

```python
def critical_connections(n, connections):
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
    tin = [-1] * n
    low = [0] * n
    timer = [0]
    bridges = []

    def dfs(v, parent):
        tin[v] = low[v] = timer[0]
        timer[0] += 1
        for to in adj[v]:
            if to == parent:
                continue
            if tin[to] != -1:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append([min(v, to), max(v, to)])

    for s in range(n):
        if tin[s] == -1:
            dfs(s, -1)
    return sorted(bridges)

assert critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]) == [[1, 3]]
assert critical_connections(5, [[0, 1], [1, 2], [0, 3], [3, 4], [1, 4]]) == [[1, 2]]
assert critical_connections(2, [[0, 1]]) == [[0, 1]]
```

```cpp
vector<vector<int>> critical_connections(int n, const vector<vector<int>>& connections) {
    vector<vector<int>> adj(n);
    for (auto& e : connections) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<int> tin(n, -1), low(n, 0);
    int timer = 0;
    vector<vector<int>> bridges;
    function<void(int,int)> dfs = [&](int v, int parent) {
        tin[v] = low[v] = timer++;
        for (int to : adj[v]) {
            if (to == parent) continue;
            if (tin[to] != -1) {
                low[v] = min(low[v], tin[to]);
            } else {
                dfs(to, v);
                low[v] = min(low[v], low[to]);
                if (low[to] > tin[v]) bridges.push_back({min(v, to), max(v, to)});
            }
        }
    };
    for (int s = 0; s < n; ++s)
        if (tin[s] == -1) dfs(s, -1);
    sort(bridges.begin(), bridges.end());
    return bridges;
}
```

The time is $O(n + m + b \log b)$ for $b$ bridges (the last term is the final sort), and the space is $O(n+m)$.

## 9.4 Articulation points

The same DFS finds the cut vertices. For a non-root vertex `v`, we mark it as soon as one child has $low[child] \ge tin[v]$. For the root we only count its DFS children, and mark it if there are at least two. Notice that the root test is different because the root has no ancestors to escape to: with a single child, the whole graph hangs below the root and removing it just removes one end. This is exactly the problem _Articulation Points_.

```python
def articulation_points(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    tin = [-1] * n
    low = [0] * n
    timer = [0]
    is_cut = [False] * n

    def dfs(v, parent):
        tin[v] = low[v] = timer[0]
        timer[0] += 1
        children = 0
        for to in adj[v]:
            if to == parent:
                continue
            if tin[to] != -1:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                children += 1
                if parent != -1 and low[to] >= tin[v]:
                    is_cut[v] = True
        if parent == -1 and children >= 2:
            is_cut[v] = True

    for s in range(n):
        if tin[s] == -1:
            dfs(s, -1)
    return [v for v in range(n) if is_cut[v]]

assert articulation_points(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == [1, 3]
assert articulation_points(3, [[0, 1], [1, 2], [2, 0]]) == []
assert articulation_points(5, [[0, 1], [1, 2], [0, 3], [3, 4], [1, 4]]) == [1]
assert articulation_points(3, [[1, 0], [1, 2]]) == [1]
```

```cpp
vector<int> articulation_points(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<int> tin(n, -1), low(n, 0);
    vector<bool> is_cut(n, false);
    int timer = 0;
    function<void(int,int)> dfs = [&](int v, int parent) {
        tin[v] = low[v] = timer++;
        int children = 0;
        for (int to : adj[v]) {
            if (to == parent) continue;
            if (tin[to] != -1) {
                low[v] = min(low[v], tin[to]);
            } else {
                dfs(to, v);
                low[v] = min(low[v], low[to]);
                ++children;
                if (parent != -1 && low[to] >= tin[v]) is_cut[v] = true;
            }
        }
        if (parent == -1 && children >= 2) is_cut[v] = true;
    };
    for (int s = 0; s < n; ++s)
        if (tin[s] == -1) dfs(s, -1);
    vector<int> result;
    for (int v = 0; v < n; ++v)
        if (is_cut[v]) result.push_back(v);
    return result;
}
```

The time is $O(n+m)$ and the space is $O(n+m)$. The last assertion shows the root rule at work: with the edges 1-0 and 1-2 the search starts at 0, so 1 is not the root and is a cut vertex through its child 2. Starting at the middle vertex would have given the root two children and the same answer.

## 9.5 Strongly connected components

Now switch to directed graphs, where reachability can be one-way. A **strongly connected component**, or **SCC**, is a largest possible group of vertices in which every vertex can reach every other one by following arrows. Every vertex lies in exactly one SCC (a vertex alone is a component by itself). If we squeeze each SCC into a single dot, the result has no cycles, because a cycle would have merged its dots into one component.

**Kosaraju's algorithm** finds all SCCs with two DFS passes. In the first pass we run DFS over the whole graph and write each vertex in a list `order` at the moment it finishes. The vertex that finishes last belongs to a component with no arrows entering it from other components (a "source" component), because otherwise DFS would have visited it earlier from somewhere else and finished it earlier. In the second pass we **reverse every arrow** and go through `order` from the end. Reversing makes the source component a dead end: a DFS in the reversed graph starting inside it cannot leave it, so it collects exactly that component. We then remove it from consideration (by keeping the vertices marked) and the next vertex in the list lies in a source component of what remains.

Trace it on the arrows 0→1, 1→2, 2→0, 2→3, 3→4, 4→3. The vertices 0, 1, 2 form one loop and 3, 4 form another, with a single arrow 2→3 from the first into the second. In the first pass, DFS from 0 goes 0, 1, 2, then 3, then 4. Vertex 4 finishes first, then 3, 2, 1, 0, so `order = [4, 3, 2, 1, 0]`. In the second pass the arrows are reversed (now 0→2, 1→0, 2→1, 3→2, 3→4, 4→3). We read `order` backwards: 0 first. DFS from 0 reaches 2 and then 1, and cannot reach 3 or 4, because the arrow that connected them now points the other way. So {0, 1, 2} is a component. The next unvisited vertex in the backwards order is 3, whose DFS reaches 4: the component {3, 4}.

The answer to "how many SCCs?" is the number of components found. This is exactly the problem _Strongly Connected Components_.

```python
def strongly_connected_components(n, edges):
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        radj[b].append(a)
    visited = [False] * n
    order = []

    def dfs1(v):
        visited[v] = True
        for to in adj[v]:
            if not visited[to]:
                dfs1(to)
        order.append(v)

    for v in range(n):
        if not visited[v]:
            dfs1(v)

    visited = [False] * n
    components = []

    def dfs2(v, comp):
        visited[v] = True
        comp.append(v)
        for to in radj[v]:
            if not visited[to]:
                dfs2(to, comp)

    for v in reversed(order):
        if not visited[v]:
            comp = []
            dfs2(v, comp)
            components.append(comp)
    return components

def count_scc(n, edges):
    return len(strongly_connected_components(n, edges))

chain = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 3]]
comps = strongly_connected_components(5, chain)
assert [sorted(c) for c in comps] == [[0, 1, 2], [3, 4]]
assert count_scc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]) == 3
assert count_scc(3, []) == 3
```

```cpp
vector<vector<int>> strongly_connected_components(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n), radj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        radj[e[1]].push_back(e[0]);
    }
    vector<bool> visited(n, false);
    vector<int> order;
    function<void(int)> dfs1 = [&](int v) {
        visited[v] = true;
        for (int to : adj[v])
            if (!visited[to]) dfs1(to);
        order.push_back(v);
    };
    for (int v = 0; v < n; ++v)
        if (!visited[v]) dfs1(v);

    visited.assign(n, false);
    vector<vector<int>> components;
    vector<int> comp;
    function<void(int)> dfs2 = [&](int v) {
        visited[v] = true;
        comp.push_back(v);
        for (int to : radj[v])
            if (!visited[to]) dfs2(to);
    };
    for (int i = n - 1; i >= 0; --i) {
        int v = order[i];
        if (!visited[v]) {
            comp.clear();
            dfs2(v);
            components.push_back(comp);
        }
    }
    return components;
}

int count_scc(int n, const vector<vector<int>>& edges) {
    return strongly_connected_components(n, edges).size();
}
```

Both passes visit every vertex and edge once, so the time is $O(n+m)$ and the space is $O(n+m)$ for the two adjacency lists.

## 9.6 Minimum height trees

A **tree** is a connected undirected graph without cycles. If we pick one vertex as the **root** and hang the tree from it, the **height** is the number of edges on the longest downward path. Different roots give different heights: in a path of five vertices, rooting at an end gives height 4, while rooting in the middle gives height 2. The question is which roots give the smallest height.

The best roots are the "middle" of the tree. A way to find the middle is to peel the tree like an onion: all the **leaves** (vertices with only one neighbour) are the furthest from the middle, so remove them all at once. This creates new leaves. Repeat, layer by layer, until at most two vertices remain. Those are the answers: one vertex when the longest path has an odd number of vertices, two when it has an even number.

Take the tree with the edges 0-1, 1-2, 1-3, 3-4, 4-5 (six vertices). The leaves are 0, 2 and 5. Remove them, and 1 and 4 become leaves (3 vertices remain: 1, 3, 4). Remove those two as well, and 3 is the only vertex left. The answer is `[3]`; indeed the longest path 0-1-3-4-5 has 3 in the middle. This is exactly the problem _Minimum Height Trees_.

```python
from collections import deque

def min_height_trees(n, edges):
    if n == 1:
        return [0]
    adj = [[] for _ in range(n)]
    degree = [0] * n
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        degree[a] += 1
        degree[b] += 1
    leaves = deque(v for v in range(n) if degree[v] == 1)
    remaining = n
    while remaining > 2:
        layer = len(leaves)
        remaining -= layer
        for _ in range(layer):
            leaf = leaves.popleft()
            for nb in adj[leaf]:
                degree[nb] -= 1
                if degree[nb] == 1:
                    leaves.append(nb)
    return sorted(leaves)

assert min_height_trees(6, [[0, 1], [1, 2], [1, 3], [3, 4], [4, 5]]) == [3]
assert min_height_trees(4, [[1, 0], [1, 2], [1, 3]]) == [1]
assert min_height_trees(4, [[0, 1], [1, 2], [2, 3]]) == [1, 2]
assert min_height_trees(1, []) == [0]
```

```cpp
vector<int> min_height_trees(int n, const vector<vector<int>>& edges) {
    if (n == 1) return {0};
    vector<vector<int>> adj(n);
    vector<int> degree(n, 0);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
        degree[e[0]]++;
        degree[e[1]]++;
    }
    queue<int> leaves;
    for (int v = 0; v < n; ++v)
        if (degree[v] == 1) leaves.push(v);
    int remaining = n;
    while (remaining > 2) {
        int layer = leaves.size();
        remaining -= layer;
        for (int i = 0; i < layer; ++i) {
            int leaf = leaves.front();
            leaves.pop();
            for (int nb : adj[leaf]) {
                if (--degree[nb] == 1) leaves.push(nb);
            }
        }
    }
    vector<int> result;
    while (!leaves.empty()) {
        result.push_back(leaves.front());
        leaves.pop();
    }
    sort(result.begin(), result.end());
    return result;
}
```

Every vertex is removed once, so the time is $O(n)$ and the space is $O(n)$. This is Kahn's idea from Chapter 5 again: peeling vertices of degree one instead of degree zero.

## 9.7 Check yourself

1. In the bridge test $low[c] > tin[v]$, what does it say about the subtree of the child `c`?
2. Why is the root of the DFS tree a cut vertex only when it has at least two children?
3. In Kosaraju's algorithm, why do we reverse the arrows in the second pass?
4. A tree is a path of 6 vertices, 0-1-2-3-4-5. Which vertices does the leaf-peeling method return?

# Chapter 10. DP on directed acyclic graphs

## 10.1 Answers that build on answers

**Dynamic programming** (DP) means solving a big question by first answering smaller versions of it and then combining those answers, never solving the same small question twice. On a directed graph with no cycles (a **DAG**, from Chapter 5), the small questions are very natural: the answer for a vertex is built from the answers of the vertices its arrows point to. Because there are no cycles, those vertices never depend back on the first one, so the recursion always ends.

Here is the classic example. For each vertex `v`, find the length (number of edges) of the longest path that **starts at `v`**. A longest path from `v` either stops right there (length 0) or takes one arrow `v→u` and continues with a longest path from `u`. So

$$\text{len}(v) = \max\bigl(0,\ \max_{v \to u}(1 + \text{len}(u))\bigr).$$

Take six vertices with the arrows 0→1, 0→2, 1→3, 2→3, 3→4 and 2→5. Vertices 4 and 5 have no arrows out, so their answer is 0. Vertex 3 has the single arrow to 4, so its answer is $1 + 0 = 1$. Vertex 1 goes to 3, giving $1 + 1 = 2$. Vertex 2 goes to 3 or 5, so it is $\max(1 + 1, 1 + 0) = 2$. Vertex 0 goes to 1 or 2, so it is $1 + 2 = 3$. The answers for vertices 0 to 5 are 3, 2, 2, 1, 0, 0.

To avoid recomputing, we remember each answer after computing it. This trick is called **memoisation**. Each vertex is computed once and each arrow is looked at once, so the time is $O(n+m)$.

```python
def longest_from(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    best = [-1] * n  # -1 means "not computed yet"

    def go(v):
        if best[v] == -1:
            best[v] = 0
            for u in adj[v]:
                best[v] = max(best[v], 1 + go(u))
        return best[v]

    return [go(v) for v in range(n)]

edges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [2, 5]]
assert longest_from(6, edges) == [3, 2, 2, 1, 0, 0]
```

```cpp
vector<int> longest_from(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back(e[1]);
    vector<int> best(n, -1);  // -1 means "not computed yet"
    function<int(int)> go = [&](int v) {
        if (best[v] == -1) {
            best[v] = 0;
            for (int u : adj[v]) best[v] = max(best[v], 1 + go(u));
        }
        return best[v];
    };
    vector<int> result(n);
    for (int v = 0; v < n; ++v) result[v] = go(v);
    return result;
}
```

The guarantee that the recursion ends depends entirely on the absence of cycles. On a graph with a cycle, `go` could call itself forever. Chapter 11 shows how to deal with that.

## 10.2 Bottom-up with a topological order

The recursive version can run out of stack on a long chain, and sometimes we simply prefer a loop. A **topological order** (Chapter 5) lists the vertices so that every arrow points forward. If we walk through that list **backwards**, then by the time we reach a vertex, all vertices it points to have already been finished. So the DP becomes a plain loop with no recursion.

```python
from collections import deque

def topological_order(n, adj):
    indeg = [0] * n
    for v in range(n):
        for u in adj[v]:
            indeg[u] += 1
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in adj[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    return order

def longest_path_lengths(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    best = [0] * n
    for v in reversed(topological_order(n, adj)):
        for u in adj[v]:
            best[v] = max(best[v], 1 + best[u])
    return best

edges = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [2, 5]]
assert longest_path_lengths(6, edges) == [3, 2, 2, 1, 0, 0]
assert max(longest_path_lengths(6, edges)) == 3
```

```cpp
vector<int> topological_order(int n, const vector<vector<int>>& adj) {
    vector<int> indeg(n, 0), order;
    for (int v = 0; v < n; ++v)
        for (int u : adj[v]) indeg[u]++;
    queue<int> q;
    for (int v = 0; v < n; ++v)
        if (indeg[v] == 0) q.push(v);
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        order.push_back(v);
        for (int u : adj[v])
            if (--indeg[u] == 0) q.push(u);
    }
    return order;
}

vector<int> longest_path_lengths(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back(e[1]);
    vector<int> best(n, 0);
    vector<int> order = topological_order(n, adj);
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int v = order[i];
        for (int u : adj[v]) best[v] = max(best[v], 1 + best[u]);
    }
    return best;
}
```

The answer to "what is the longest path anywhere in the DAG?" is the largest entry. The time is $O(n+m)$ and the space is $O(n+m)$. If the topological order has fewer than $n$ vertices, the graph has a cycle and this DP does not apply.

## 10.3 Counting paths

The same skeleton works for any way of combining the answers of the successors. To **count** the paths from `v` to a target `t`, there is one path of length zero if `v` is the target, and otherwise every path starts with some arrow `v→u` followed by a path from `u` to `t`. So we add up the counts of the successors:

$$\text{ways}(v) = \begin{cases} 1 & v = t, \\ \sum_{v \to u} \text{ways}(u) & \text{otherwise.} \end{cases}$$

Take the arrows 0→1, 0→2, 1→2, 1→3 and 2→3, and count the paths from 0 to 3. Going backwards: `ways(3) = 1`; `ways(2) = ways(3) = 1`; `ways(1) = ways(2) + ways(3) = 2`; `ways(0) = ways(1) + ways(2) = 3`. The three paths are 0-1-3, 0-1-2-3 and 0-2-3. Counts grow fast, so problems usually ask for the answer modulo a big number such as $10^9 + 7$.

```python
def count_paths(n, edges, s, t):
    MOD = 10**9 + 7
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    ways = [0] * n
    ways[t] = 1
    for v in reversed(topological_order(n, adj)):
        if v != t:
            for u in adj[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[s]

assert count_paths(4, [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]], 0, 3) == 3
assert count_paths(3, [[0, 1]], 0, 2) == 0
```

```cpp
int count_paths(int n, const vector<vector<int>>& edges, int s, int t) {
    const int MOD = 1'000'000'007;
    vector<vector<int>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back(e[1]);
    vector<int> ways(n, 0);
    ways[t] = 1;
    vector<int> order = topological_order(n, adj);
    for (int i = (int)order.size() - 1; i >= 0; --i) {
        int v = order[i];
        if (v == t) continue;
        for (int u : adj[v]) ways[v] = (ways[v] + ways[u]) % MOD;
    }
    return ways[s];
}
```

Replace the sum by a minimum of (edge cost plus the successor's answer) and you get the cheapest path; replace it by "or" and you learn whether some path exists. If the path must satisfy an extra rule, such as "pass through exactly two special vertices", add that fact to the state, so that the state is the pair (vertex, special vertices passed so far). We will use this idea of a richer state in Chapter 11. And to print the best path rather than only its value, remember for each vertex which successor gave the best value and follow those choices.

## 10.4 Shortest paths on a DAG

On a DAG, shortest paths need no priority queue and no repeated scans. If we handle the vertices in topological order, then when we reach a vertex its distance is already final, because every arrow into it comes from an earlier vertex that has already been processed. So a single pass in which each vertex relaxes its outgoing arrows (Chapter 6) is enough. This works even with **negative** costs, since nothing can ever come back to improve a finished vertex.

Take the arrows 0→1 (cost 4), 0→2 (cost 5), 2→1 (cost $-3$) and 1→3 (cost 2), from vertex 0. A topological order is 0, 2, 1, 3. Vertex 0 sets `dist[1] = 4` and `dist[2] = 5`. Vertex 2 improves `dist[1]` to $5 - 3 = 2$. Vertex 1 sets `dist[3] = 4`. The distances are 0, 2, 5, 4.

```python
def dag_shortest(n, edges, source):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    INF = 10**18
    dist = [INF] * n
    dist[source] = 0
    plain = [[b for b, w in row] for row in adj]
    for v in topological_order(n, plain):
        if dist[v] == INF:
            continue
        for u, w in adj[v]:
            dist[u] = min(dist[u], dist[v] + w)
    return [None if d == INF else d for d in dist]

edges = [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]]
assert dag_shortest(4, edges, 0) == [0, 2, 5, 4]
assert dag_shortest(3, [[1, 2, 7]], 0) == [0, None, None]
```

```cpp
vector<optional<long long>> dag_shortest(int n, const vector<vector<int>>& edges, int source) {
    vector<vector<pair<int,int>>> adj(n);
    vector<vector<int>> plain(n);
    for (auto& e : edges) {
        adj[e[0]].push_back({e[1], e[2]});
        plain[e[0]].push_back(e[1]);
    }
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    dist[source] = 0;
    for (int v : topological_order(n, plain)) {
        if (dist[v] == INF) continue;
        for (auto [u, w] : adj[v]) dist[u] = min(dist[u], dist[v] + w);
    }
    vector<optional<long long>> result(n);
    for (int v = 0; v < n; ++v)
        if (dist[v] != INF) result[v] = dist[v];
    return result;
}
```

The time is $O(n+m)$, faster than Dijkstra's $O((n+m)\log n)$, which is why recognising a DAG pays off.

There is a second, less obvious DAG hiding in Chapter 6. In _Cheapest Flights Within K Stops_ the states are pairs (city, number of flights used). An arrow goes from (city $a$, $i$ flights) to (city $b$, $i+1$ flights) for every flight $a \to b$. Every arrow raises the second number, so there are no cycles: it is a DAG of layers, and the Bellman-Ford rounds of Section 6.7 are exactly the DP over its layers. Whenever you can add a counter that always grows, a graph with cycles becomes a DAG of states.

## 10.5 The shortest-path graph

Compute the shortest distances $d$ from a source with Dijkstra, assuming every edge cost is **positive**. Now keep only the edges $(u, v, w)$ with $d(u) + w = d(v)$: exactly the edges that lie on some shortest path. Along every kept edge the distance strictly grows, so the kept graph has no cycles even if the original graph had. It is a DAG, and handling the vertices in order of increasing distance is a valid topological order of it.

On this DAG all the counting and best-of questions from Section 10.3 apply. Counting shortest paths is the sum over kept edges: $\text{ways}(v) = \sum \text{ways}(u)$ over the kept edges $u \to v$, with $\text{ways}(\text{source}) = 1$. This is the same answer as the single-pass Dijkstra trick of Section 6.5, but seen as two clean steps: first distances, then DP.

Take the roads 0-1, 0-2, 1-3, 2-3, 3-4 (each of time 1) and one long road 0-4 of time 10. The distances from 0 are 0, 1, 1, 2, 3. The kept edges are all of them except the road 0-4 (since $0 + 10 \ne 3$). Going in increasing distance: `ways(0) = 1`, `ways(1) = ways(2) = 1`, `ways(3) = ways(1) + ways(2) = 2`, `ways(4) = ways(3) = 2`.

```python
import heapq

def dijkstra(n, adj, source):
    INF = 10**18
    dist = [INF] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist

def count_shortest_by_dp(n, roads, source, target):
    MOD = 10**9 + 7
    adj = [[] for _ in range(n)]
    for a, b, w in roads:
        adj[a].append((b, w))
        adj[b].append((a, w))
    dist = dijkstra(n, adj, source)
    ways = [0] * n
    ways[source] = 1
    for v in sorted(range(n), key=lambda x: dist[x]):
        for u, w in adj[v]:
            if dist[v] + w == dist[u]:
                ways[u] = (ways[u] + ways[v]) % MOD
    return ways[target]

roads = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1], [3, 4, 1], [0, 4, 10]]
assert count_shortest_by_dp(5, roads, 0, 4) == 2
assert count_shortest_by_dp(5, roads, 0, 3) == 2
```

```cpp
vector<long long> dijkstra(int n, const vector<vector<pair<int,int>>>& adj, int source) {
    const long long INF = (long long)1e18;
    vector<long long> dist(n, INF);
    dist[source] = 0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> heap;
    heap.push({0, source});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                heap.push({dist[v], v});
            }
        }
    }
    return dist;
}

int count_shortest_by_dp(int n, const vector<vector<int>>& roads, int source, int target) {
    const int MOD = 1'000'000'007;
    vector<vector<pair<int,int>>> adj(n);
    for (auto& r : roads) {
        adj[r[0]].push_back({r[1], r[2]});
        adj[r[1]].push_back({r[0], r[2]});
    }
    vector<long long> dist = dijkstra(n, adj, source);
    vector<int> ways(n, 0);
    ways[source] = 1;
    vector<int> order(n);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int a, int b) { return dist[a] < dist[b]; });
    for (int v : order)
        for (auto [u, w] : adj[v])
            if (dist[v] + w == dist[u]) ways[u] = (ways[u] + ways[v]) % MOD;
    return ways[target];
}
```

The time is $O((n+m)\log n)$ for Dijkstra plus the sort, and the space is $O(n+m)$. The positive costs are essential. With a zero-cost edge, two vertices at the same distance could point at each other, the kept graph would have a cycle, and sorting by distance would no longer be a valid order.

## 10.6 Check yourself

1. Why does the recursion `go(v)` of Section 10.1 always terminate on a DAG?
2. In the bottom-up version, why do we walk the topological order backwards?
3. In the path-counting example 0→1, 0→2, 1→2, 1→3, 2→3, why is `ways(0)` equal to `ways(1) + ways(2)`?
4. Why are negative edge costs harmless for shortest paths on a DAG, but dangerous for Dijkstra?

# Chapter 11. DP on graphs with cycles

## 11.1 When the arrows go round in circles

The DP of Chapter 10 needs an order in which every vertex is handled after the vertices it depends on. If the graph has a cycle, say $A \to B \to C \to A$, then the answer for $A$ depends on $B$, which depends on $C$, which depends on $A$, and no such order exists. A naive recursive solution would call itself forever.

There are three standard ways out, and this chapter teaches them in turn. The first is to **squeeze each cycle into a single point**, which is allowed when the question does not care what happens inside the cycle. The second is to **let Dijkstra supply the order**, since it finishes vertices in increasing order of distance. The third is to **add a counter or a flag to the state** so that the extended state graph no longer has cycles, or becomes a good fit for Dijkstra. At the end we look at two special tools for counting walks that repeat many times: matrix powers and binary lifting.

## 11.2 Squeezing cycles into points

Recall the strongly connected components (SCCs) of Chapter 9: groups of vertices in which every vertex can reach every other. If we squeeze every SCC into a single point and keep the arrows between different components, the result is called the **condensation**, and it never has a cycle (a cycle between components would have merged them). So we can run the DAG DP on the condensation.

This is the right tool when revisiting vertices is allowed and useless. Here is a classic puzzle. Each room holds some coins. You walk through one-way corridors, you may pass through rooms again, and the coins in a room can be taken only once. Inside an SCC you can reach every room from every other, so you can pick up all the coins in it. The value of a component is therefore the sum of its coins, and the question becomes "which path through the condensation collects the most?", which is the longest-path DP of Chapter 10 with sums instead of lengths.

Take four rooms with coins `[1, 1, 10, 3]` and the corridors 0→1, 1→0, 0→2 and 0→3. Rooms 0 and 1 form a loop, worth 2 coins together. From that component we may continue to room 2 (10 coins) or room 3 (3 coins). The best route collects $2 + 10 = 12$.

The Kosaraju steps of Section 9.5 give component numbers if we number the components in the order we find them: the first component found is a source of the condensation, so every arrow between components goes from a smaller number to a larger one. Then the DP is a loop over the component numbers from the largest to the smallest.

```python
def scc_numbers(n, edges):
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        radj[b].append(a)
    visited = [False] * n
    order = []

    def dfs1(v):
        visited[v] = True
        for u in adj[v]:
            if not visited[u]:
                dfs1(u)
        order.append(v)

    for v in range(n):
        if not visited[v]:
            dfs1(v)
    comp = [-1] * n
    count = 0

    def dfs2(v, c):
        comp[v] = c
        for u in radj[v]:
            if comp[u] == -1:
                dfs2(u, c)

    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, count)
            count += 1
    return comp, count

def max_coins(n, coins, edges):
    comp, count = scc_numbers(n, edges)
    value = [0] * count
    for v in range(n):
        value[comp[v]] += coins[v]
    next_components = [set() for _ in range(count)]
    for a, b in edges:
        if comp[a] != comp[b]:
            next_components[comp[a]].add(comp[b])
    best = [0] * count
    for c in range(count - 1, -1, -1):
        best[c] = value[c] + max((best[d] for d in next_components[c]), default=0)
    return max(best, default=0)

assert max_coins(4, [1, 1, 10, 3], [[0, 1], [1, 0], [0, 2], [0, 3]]) == 12
assert max_coins(5, [1, 2, 3, 4, 5], [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 3]]) == 15
assert max_coins(0, [], []) == 0
```

```cpp
pair<vector<int>, int> scc_numbers(int n, const vector<vector<int>>& edges) {
    vector<vector<int>> adj(n), radj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        radj[e[1]].push_back(e[0]);
    }
    vector<bool> visited(n, false);
    vector<int> order;
    function<void(int)> dfs1 = [&](int v) {
        visited[v] = true;
        for (int u : adj[v])
            if (!visited[u]) dfs1(u);
        order.push_back(v);
    };
    for (int v = 0; v < n; ++v)
        if (!visited[v]) dfs1(v);
    vector<int> comp(n, -1);
    int count = 0;
    function<void(int,int)> dfs2 = [&](int v, int c) {
        comp[v] = c;
        for (int u : radj[v])
            if (comp[u] == -1) dfs2(u, c);
    };
    for (int i = n - 1; i >= 0; --i) {
        int v = order[i];
        if (comp[v] == -1) dfs2(v, count++);
    }
    return {comp, count};
}

long long max_coins(int n, const vector<int>& coins, const vector<vector<int>>& edges) {
    auto [comp, count] = scc_numbers(n, edges);
    vector<long long> value(count, 0);
    for (int v = 0; v < n; ++v) value[comp[v]] += coins[v];
    vector<set<int>> next_components(count);
    for (auto& e : edges)
        if (comp[e[0]] != comp[e[1]]) next_components[comp[e[0]]].insert(comp[e[1]]);
    vector<long long> best(count, 0);
    long long answer = 0;
    for (int c = count - 1; c >= 0; --c) {
        long long follow = 0;
        for (int d : next_components[c]) follow = max(follow, best[d]);
        best[c] = value[c] + follow;
        answer = max(answer, best[c]);
    }
    return answer;
}
```

Both parts are linear: the time is $O(n+m)$ and the space is $O(n+m)$ (the sets add a logarithmic factor in the code above, which does not matter in practice). The same condensation trick answers "can $a$ reach $b$?" questions and is the first step of 2-SAT solvers.

## 11.3 Dijkstra supplies the order

In Chapter 6 we counted shortest paths while Dijkstra ran, and in Section 10.5 we saw why that is legitimate: Dijkstra finishes vertices in increasing order of distance, which on a graph with positive costs is a valid order for a DP. So we can attach **any extra DP value** to a shortest-path search, as long as it combines in a way that respects the order.

A neat example is the pair "(cost, number of edges)". Among all the cheapest routes, which one uses the fewest edges? Python compares pairs lexicographically (first entries first), so we can treat the pair as a single cost: adding an edge of cost $w$ adds the pair $(w, 1)$. This keeps the property that Dijkstra needs, that extending a route never makes it smaller. Take the roads 0→1 (cost 1), 1→2 (cost 1), 2→3 (cost 2) and 0→3 (cost 4). Both routes to vertex 3 cost 4, one with three roads and one with a single road, and the pair comparison picks $(4, 1)$.

```python
import heapq

def cheapest_then_fewest(n, edges, source):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    best = [None] * n
    best[source] = (0, 0)
    heap = [(0, 0, source)]
    while heap:
        cost, steps, u = heapq.heappop(heap)
        if best[u] != (cost, steps):
            continue
        for v, w in adj[u]:
            candidate = (cost + w, steps + 1)
            if best[v] is None or candidate < best[v]:
                best[v] = candidate
                heapq.heappush(heap, (candidate[0], candidate[1], v))
    return best

edges = [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 4]]
assert cheapest_then_fewest(4, edges, 0) == [(0, 0), (1, 1), (2, 2), (4, 1)]
assert cheapest_then_fewest(3, [[0, 1, 5]], 0) == [(0, 0), (5, 1), None]
```

```cpp
vector<optional<pair<long long,int>>> cheapest_then_fewest(int n, const vector<vector<int>>& edges, int source) {
    vector<vector<pair<int,int>>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back({e[1], e[2]});
    vector<optional<pair<long long,int>>> best(n);
    best[source] = make_pair(0LL, 0);
    using State = tuple<long long,int,int>;  // cost, steps, vertex
    priority_queue<State, vector<State>, greater<>> heap;
    heap.push({0, 0, source});
    while (!heap.empty()) {
        auto [cost, steps, u] = heap.top();
        heap.pop();
        if (!best[u] || *best[u] != make_pair(cost, steps)) continue;
        for (auto [v, w] : adj[u]) {
            pair<long long,int> candidate = {cost + w, steps + 1};
            if (!best[v] || candidate < *best[v]) {
                best[v] = candidate;
                heap.push({candidate.first, candidate.second, v});
            }
        }
    }
    return best;
}
```

The time is $O((n+m)\log n)$ as for ordinary Dijkstra. The same idea gives "cheapest route, and among those the one with the largest sum of a second quantity", or the lexicographically smallest route in a more complicated setting.

## 11.4 Adding facts to the state

The most flexible idea is to make the **state** richer, so that the position in the new, bigger graph carries everything the future needs. A vertex of the new graph is a pair like (city, coupon used?) or (city, flights taken). Arrows between such pairs follow the original roads and also update the extra fact. If the extra fact only ever increases (a counter) the new graph is a DAG, and when costs are non-negative, Dijkstra works on it directly. This is often called a **layered graph** or product graph.

First example: you travel from a start city to a destination, and you have one coupon that halves the cost of a single road (rounding down). The state is (city, coupon used?). From (city $v$, not used) along a road of cost $w$ you may go to (city $u$, not used) paying $w$, or to (city $u$, used) paying $\lfloor w/2 \rfloor$. From (city $v$, used) you only go to (city $u$, used) paying $w$. The answer is the distance to (destination, used). With the roads 0→1 (10), 1→2 (10), 0→2 (30) the cheapest trip without a coupon is 20, and with the coupon on one of the first two roads it is $10 + 5 = 15$.

```python
import heapq

def cheapest_with_coupon(n, edges, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    INF = 10**18
    dist = [[INF, INF] for _ in range(n)]  # dist[v][used]
    dist[src][0] = 0
    heap = [(0, src, 0)]
    while heap:
        d, v, used = heapq.heappop(heap)
        if d != dist[v][used]:
            continue
        for u, w in adj[v]:
            if d + w < dist[u][used]:
                dist[u][used] = d + w
                heapq.heappush(heap, (d + w, u, used))
            if used == 0 and d + w // 2 < dist[u][1]:
                dist[u][1] = d + w // 2
                heapq.heappush(heap, (d + w // 2, u, 1))
    return -1 if dist[dst][1] == INF else dist[dst][1]

assert cheapest_with_coupon(3, [[0, 1, 10], [1, 2, 10], [0, 2, 30]], 0, 2) == 15
assert cheapest_with_coupon(2, [[0, 1, 8]], 0, 1) == 4
assert cheapest_with_coupon(2, [], 0, 1) == -1
```

```cpp
long long cheapest_with_coupon(int n, const vector<vector<int>>& edges, int src, int dst) {
    vector<vector<pair<int,int>>> adj(n);
    for (auto& e : edges) adj[e[0]].push_back({e[1], e[2]});
    const long long INF = (long long)1e18;
    vector<array<long long,2>> dist(n, {INF, INF});  // dist[v][used]
    dist[src][0] = 0;
    using State = tuple<long long,int,int>;
    priority_queue<State, vector<State>, greater<>> heap;
    heap.push({0, src, 0});
    while (!heap.empty()) {
        auto [d, v, used] = heap.top();
        heap.pop();
        if (d != dist[v][used]) continue;
        for (auto [u, w] : adj[v]) {
            if (d + w < dist[u][used]) {
                dist[u][used] = d + w;
                heap.push({d + w, u, used});
            }
            if (used == 0 && d + w / 2 < dist[u][1]) {
                dist[u][1] = d + w / 2;
                heap.push({d + w / 2, u, 1});
            }
        }
    }
    return dist[dst][1] == INF ? -1 : dist[dst][1];
}
```

The second example is the one from Section 6.7, _Cheapest Flights Within K Stops_, done the Dijkstra way. The state is (city, flights used so far), with at most $k+1$ flights allowed. A flight moves from (city $a$, $i$) to (city $b$, $i+1$) at its price, and we may not go beyond $k+1$ flights. Because prices are non-negative, the first time the destination is taken from the heap (in any layer) its cost is the answer.

```python
def cheapest_price_by_state(n, flights, src, dst, k):
    adj = [[] for _ in range(n)]
    for a, b, price in flights:
        adj[a].append((b, price))
    INF = 10**18
    best = [[INF] * (k + 2) for _ in range(n)]  # best[city][flights used]
    best[src][0] = 0
    heap = [(0, src, 0)]
    while heap:
        cost, city, used = heapq.heappop(heap)
        if cost != best[city][used]:
            continue
        if city == dst:
            return cost
        if used == k + 1:
            continue
        for nxt, price in adj[city]:
            if cost + price < best[nxt][used + 1]:
                best[nxt][used + 1] = cost + price
                heapq.heappush(heap, (cost + price, nxt, used + 1))
    return -1

flights = [[0, 1, 10], [1, 2, 10], [2, 3, 10], [0, 3, 100]]
assert cheapest_price_by_state(4, flights, 0, 3, 1) == 100
assert cheapest_price_by_state(4, flights, 0, 3, 2) == 30
assert cheapest_price_by_state(4, flights, 3, 0, 3) == -1
```

```cpp
int cheapest_price_by_state(int n, const vector<vector<int>>& flights, int src, int dst, int k) {
    vector<vector<pair<int,int>>> adj(n);
    for (auto& f : flights) adj[f[0]].push_back({f[1], f[2]});
    const long long INF = (long long)1e18;
    vector<vector<long long>> best(n, vector<long long>(k + 2, INF));  // best[city][flights used]
    best[src][0] = 0;
    using State = tuple<long long,int,int>;
    priority_queue<State, vector<State>, greater<>> heap;
    heap.push({0, src, 0});
    while (!heap.empty()) {
        auto [cost, city, used] = heap.top();
        heap.pop();
        if (cost != best[city][used]) continue;
        if (city == dst) return (int)cost;
        if (used == k + 1) continue;
        for (auto [nxt, price] : adj[city]) {
            if (cost + price < best[nxt][used + 1]) {
                best[nxt][used + 1] = cost + price;
                heap.push({cost + price, nxt, used + 1});
            }
        }
    }
    return -1;
}
```

There are $n(k+2)$ states and each flight is tried once per layer, so the time is $O(k \cdot m \log(k \cdot m))$ and the space is $O(nk + m)$, comparable to Bellman-Ford's $O(k \cdot m)$. Which to use is a matter of taste; the state view generalises better. The same recipe handles (city, fuel left), (city, tickets left), (cell, number of walls broken) and (position, parity of steps). The price is the size of the state space, so keep the extra information as small as possible.

## 11.5 Counting walks with matrix powers

A **walk** may repeat vertices and edges. Let $A$ be the adjacency matrix of a graph, where $A_{ij}$ is the number of edges from $i$ to $j$. The number of walks of length 2 from $i$ to $j$ is $\sum_k A_{ik}A_{kj}$, which is exactly the entry $(A^2)_{ij}$ of the matrix product, and by induction the number of walks of length $k$ is $(A^k)_{ij}$. When $k$ is huge, say $10^{18}$, but $n$ is small, we compute $A^k$ by **repeated squaring**: to get $A^{13}$, multiply $A^8 \cdot A^4 \cdot A^1$ (13 is 1101 in binary), using only about $\log_2 k$ squarings. Each product takes $O(n^3)$ time, so the total is $O(n^3 \log k)$. Answers are usually asked modulo $10^9+7$.

For a triangle (three vertices, all joined), the walks of length 3 from vertex 0 back to itself are 0-1-2-0 and 0-2-1-0, so there are 2, and the matrix code agrees. A famous special case is the Fibonacci numbers: each step moves the pair $(F_{k+1}, F_k)$ to $(F_{k+1} + F_k, F_{k+1})$, which is multiplication by the matrix with rows $(1, 1)$ and $(1, 0)$, so $F_n$ is read off its $n$-th power.

```python
MOD = 10**9 + 7

def mat_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                for j in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
    return C

def mat_pow(A, k):
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while k:
        if k & 1:
            result = mat_mul(result, A)
        A = mat_mul(A, A)
        k >>= 1
    return result

def count_walks(A, i, j, k):
    return mat_pow(A, k)[i][j]

def fib(n):
    return mat_pow([[1, 1], [1, 0]], n)[0][1]

triangle = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
assert count_walks(triangle, 0, 0, 3) == 2
assert count_walks(triangle, 0, 1, 1) == 1
assert fib(10) == 55
assert fib(0) == 0
```

```cpp
const long long MOD = 1'000'000'007;
using Matrix = vector<vector<long long>>;

Matrix mat_mul(const Matrix& A, const Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; ++i)
        for (int k = 0; k < n; ++k)
            if (A[i][k])
                for (int j = 0; j < n; ++j)
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
    return C;
}

Matrix mat_pow(Matrix A, long long k) {
    int n = A.size();
    Matrix result(n, vector<long long>(n, 0));
    for (int i = 0; i < n; ++i) result[i][i] = 1;
    while (k > 0) {
        if (k & 1) result = mat_mul(result, A);
        A = mat_mul(A, A);
        k >>= 1;
    }
    return result;
}

long long count_walks(const Matrix& A, int i, int j, long long k) {
    return mat_pow(A, k)[i][j];
}

long long fib(long long n) {
    return mat_pow({{1, 1}, {1, 0}}, n)[0][1];
}
```

Any recurrence in which each new value is a fixed linear combination of the last few values can be turned into a matrix power in the same way, which turns a slow loop over $10^{18}$ steps into about 60 squarings.

## 11.6 Functional graphs and binary lifting

A **functional graph** is a graph in which every vertex has exactly one outgoing arrow, in other words the graph of a function $f$ that maps each vertex to the next. Following the arrows from any vertex, you eventually walk onto a cycle and stay on it forever. A common question is "where am I after $k$ steps?", with $k$ as large as $10^{18}$.

Stepping one at a time is far too slow, so we use **binary lifting**: precompute, for every power of two, where every vertex lands after that many steps. Let `up[j][v]` be the vertex reached from `v` after $2^j$ steps. Then `up[0]` is $f$ itself, and since $2^j$ steps are two batches of $2^{j-1}$ steps, `up[j][v] = up[j-1][ up[j-1][v] ]`. To take $k$ steps, look at the binary digits of $k$: for every digit that is 1 at position $j$, jump with `up[j]`. Take $f = [1, 2, 3, 1]$ (vertex 0 goes to 1, 1 to 2, 2 to 3, 3 back to 1). From 0 the walk is 0, 1, 2, 3, 1, 2, so after 5 steps we are at 2. The cycle 1, 2, 3 has length 3 and $10^{18}$ leaves remainder 1 when divided by 3, so after $10^{18}$ steps from vertex 1 we are at vertex 2.

```python
def kth_after(f, start, k):
    n = len(f)
    levels = max(1, k.bit_length())
    up = [f[:]]
    for j in range(1, levels):
        prev = up[-1]
        up.append([prev[prev[v]] for v in range(n)])
    v = start
    for j in range(levels):
        if (k >> j) & 1:
            v = up[j][v]
    return v

f = [1, 2, 3, 1]
assert kth_after(f, 0, 0) == 0
assert kth_after(f, 0, 5) == 2
assert kth_after(f, 1, 10**18) == 2
```

```cpp
int kth_after(const vector<int>& f, int start, long long k) {
    int n = f.size();
    int levels = 1;
    while ((1LL << levels) <= k) ++levels;
    vector<vector<int>> up(levels, vector<int>(n));
    up[0] = f;
    for (int j = 1; j < levels; ++j)
        for (int v = 0; v < n; ++v)
            up[j][v] = up[j - 1][up[j - 1][v]];
    int v = start;
    for (int j = 0; j < levels; ++j)
        if ((k >> j) & 1) v = up[j][v];
    return v;
}
```

The table has $n \log k$ entries, so preprocessing takes $O(n \log k)$ time and memory, and every query then takes $O(\log k)$. The same doubling table, applied to a tree with `f` equal to the parent, answers "the $k$-th ancestor of a vertex" and is the base of lowest-common-ancestor algorithms.

## 11.7 Check yourself

1. Why does squeezing every strongly connected component into one point remove all the cycles?
2. In the coin puzzle, why is the value of a component the sum of all its coins?
3. In the state (city, coupon used?), what happens to the number of states compared with the original graph, and why is Dijkstra still valid?
4. After how many squarings do we obtain $A^{13}$ by repeated squaring, roughly?
5. For $f = [1, 2, 0]$, where is vertex 0 after 100 steps?

# Sources and credit

Chapters 1 to 9 adapt ideas from the graph articles at [cp-algorithms.com](https://cp-algorithms.com) (breadth-first search, depth-first search, 0-1 BFS, connected components, bipartite check, finding cycles, topological sorting, Dijkstra, Bellman-Ford, Floyd-Warshall, disjoint set union, Kruskal, Prim, bridges, cut points and strongly connected components). The text here is rewritten for beginners. Like the original, it is shared under the Creative Commons Attribution-ShareAlike 4.0 licence.
