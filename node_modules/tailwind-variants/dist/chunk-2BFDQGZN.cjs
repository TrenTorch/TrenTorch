'use strict';

// src/internal/join-class-value.ts
var isArray = Array.isArray;
var joinClassValue = (value) => {
  if (!value && value !== 0 && value !== 0n) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number") {
    if (value !== value) return "";
    return "" + value;
  }
  if (typeof value === "bigint") return "" + value;
  let result = "";
  if (isArray(value)) {
    const length = value.length;
    for (let index = 0; index < length; index++) {
      const item = value[index];
      if (!item && item !== 0 && item !== 0n) continue;
      const resolved = typeof item === "string" ? item : joinClassValue(item);
      if (resolved) {
        if (result) result += " ";
        result += resolved;
      }
    }
    return result;
  }
  if (typeof value === "object") {
    for (const key in value) {
      if (value[key]) {
        if (result) result += " ";
        result += key;
      }
    }
  }
  return result;
};

// src/utils.ts
var SPACE_REGEX = /\s+/g;
var isArray2 = Array.isArray;
var removeExtraSpaces = (str) => {
  if (typeof str !== "string" || !str) return str;
  return str.replace(SPACE_REGEX, " ").trim();
};
var stringNeedsNormalize = (str) => {
  const len = str.length;
  if (len === 0) return false;
  const first = str.charCodeAt(0);
  const last = str.charCodeAt(len - 1);
  if (first === 32 || last === 32 || first >= 9 && first <= 13 || first === 160 || last >= 9 && last <= 13 || last === 160) {
    return true;
  }
  for (let i = 0; i < len; i++) {
    const code = str.charCodeAt(i);
    if (code >= 9 && code <= 13 || code === 160) return true;
    if (code === 32 && i + 1 < len && str.charCodeAt(i + 1) === 32) return true;
  }
  return false;
};
var cx = (...classnames) => {
  const result = joinClassValue(classnames);
  if (!result) return void 0;
  return stringNeedsNormalize(result) ? removeExtraSpaces(result) : result;
};
var falsyToString = (value) => value === false ? "false" : value === true ? "true" : value === 0 ? "0" : value;
var isEmptyObject = (obj) => {
  if (!obj || typeof obj !== "object") return true;
  for (const _ in obj) return false;
  return true;
};
var isEqual = (obj1, obj2) => {
  if (obj1 === obj2) return true;
  if (!obj1 || !obj2) return false;
  const record1 = obj1;
  const record2 = obj2;
  const keys1 = Object.keys(record1);
  const keys2 = Object.keys(record2);
  if (keys1.length !== keys2.length) return false;
  for (let i = 0; i < keys1.length; i++) {
    const key = keys1[i];
    if (!keys2.includes(key)) return false;
    if (record1[key] !== record2[key]) return false;
  }
  return true;
};
var isBoolean = (value) => value === true || value === false;
var joinObjects = (obj1, obj2) => {
  const target = obj1;
  for (const key in obj2) {
    if (Object.hasOwn(obj2, key)) {
      const val2 = obj2[key];
      if (key in target) {
        target[key] = cx(target[key], val2);
      } else {
        target[key] = val2;
      }
    }
  }
  return obj1;
};
var flat = (arr, target) => {
  for (let i = 0; i < arr.length; i++) {
    const el = arr[i];
    if (isArray2(el)) flat(el, target);
    else if (el) target.push(el);
  }
};
function flatArray(arr) {
  const flattened = [];
  flat(arr, flattened);
  return flattened;
}
var flatMergeArrays = (...arrays) => {
  const result = [];
  flat(arrays, result);
  const filtered = [];
  for (let i = 0; i < result.length; i++) {
    if (result[i]) filtered.push(result[i]);
  }
  return filtered;
};
var mergeObjects = (obj1, obj2) => {
  const record1 = obj1;
  const record2 = obj2;
  const result = {};
  for (const key in record1) {
    const val1 = record1[key];
    if (key in record2) {
      const val2 = record2[key];
      if (isArray2(val1) || isArray2(val2)) {
        result[key] = flatMergeArrays(val2, val1);
      } else if (typeof val1 === "object" && typeof val2 === "object" && val1 && val2) {
        result[key] = mergeObjects(val1, val2);
      } else {
        result[key] = val2 + " " + val1;
      }
    } else {
      result[key] = val1;
    }
  }
  for (const key in record2) {
    if (!(key in record1)) {
      result[key] = record2[key];
    }
  }
  return result;
};

exports.cx = cx;
exports.falsyToString = falsyToString;
exports.flat = flat;
exports.flatArray = flatArray;
exports.flatMergeArrays = flatMergeArrays;
exports.isBoolean = isBoolean;
exports.isEmptyObject = isEmptyObject;
exports.isEqual = isEqual;
exports.joinClassValue = joinClassValue;
exports.joinObjects = joinObjects;
exports.mergeObjects = mergeObjects;
exports.removeExtraSpaces = removeExtraSpaces;
