// O(3^n) time, O(1) extra space (excluding output)
function restoreIpAddresses(s) {
  const out = [];

  function valid(part) {
    return (part === "0" || !part.startsWith("0")) && Number(part) <= 255;
  }

  function go(start, parts) {
    if (parts.length === 4) {
      if (start === s.length) {
        out.push(parts.join('.'));
      }
      return;
    }
    for (let len = 1; len <= 3; len++) {
      const part = s.slice(start, start + len);
      if (part.length === len && valid(part)) {
        go(start + len, parts.concat(part));
      }
    }
  }

  go(0, []);
  return out.sort();
}

console.log(restoreIpAddresses("25525511135"));
