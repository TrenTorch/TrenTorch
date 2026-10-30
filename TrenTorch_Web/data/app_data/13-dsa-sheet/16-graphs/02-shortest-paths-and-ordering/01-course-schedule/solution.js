function canFinish(numCourses, prerequisites) {
  // O(V + E) time, O(V + E) space
  const adj = Array.from({ length: numCourses }, () => []);
  const inDegree = new Array(numCourses).fill(0);
  for (const [course, pre] of prerequisites) {
    adj[pre].push(course);
    inDegree[course]++;
  }
  const queue = [];
  for (let i = 0; i < numCourses; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }
  let taken = 0;
  let head = 0;
  while (head < queue.length) {
    const node = queue[head++];
    taken++;
    for (const nxt of adj[node]) {
      inDegree[nxt]--;
      if (inDegree[nxt] === 0) queue.push(nxt);
    }
  }
  return taken === numCourses;
}

console.log(canFinish(2, [[1, 0]]));
