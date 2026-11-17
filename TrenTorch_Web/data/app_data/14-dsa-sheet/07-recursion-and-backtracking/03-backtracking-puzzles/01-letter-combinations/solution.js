// O(4^n * n) time, O(4^n * n) space
function letterCombinations(digits) {
  const keys = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
  };

  if (!digits) {
    return [];
  }

  const out = [];

  function go(i, prefix) {
    if (i === digits.length) {
      out.push(prefix);
      return;
    }
    for (const letter of keys[digits[i]]) {
      go(i + 1, prefix + letter);
    }
  }

  go(0, "");
  return out;
}

console.log(letterCombinations("23"));
