// O(n) time, O(n) space
function simplifyPath(path) {
  const stack = [];
  for (const name of path.split("/")) {
    if (name === "..") {
      if (stack.length) stack.pop();
    } else if (name && name !== ".") {
      stack.push(name);
    }
  }
  return "/" + stack.join("/");
}

console.log(simplifyPath("/home/"));
