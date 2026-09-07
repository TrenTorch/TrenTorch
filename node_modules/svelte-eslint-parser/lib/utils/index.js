/**
 * Add element to a sorted array
 */
export function addElementToSortedArray(array, element, compare) {
    const index = sortedLastIndex(array, (target) => compare(target, element));
    array.splice(index, 0, element);
}
/**
 * Add element to a sorted array
 */
export function addElementsToSortedArray(array, elements, compare) {
    if (!elements.length) {
        return;
    }
    let last = elements[0];
    let index = sortedLastIndex(array, (target) => compare(target, last));
    for (const element of elements) {
        if (compare(last, element) > 0) {
            index = sortedLastIndex(array, (target) => compare(target, element));
        }
        let e = array[index];
        while (e && compare(e, element) <= 0) {
            e = array[++index];
        }
        array.splice(index, 0, element);
        last = element;
    }
}
/**
 * Uses a binary search to determine the highest index at which value should be inserted into array in order to maintain its sort order.
 */
export function sortedLastIndex(array, compare) {
    let lower = 0;
    let upper = array.length;
    while (lower < upper) {
        const mid = Math.floor(lower + (upper - lower) / 2);
        const target = compare(array[mid]);
        if (target < 0) {
            lower = mid + 1;
        }
        else if (target > 0) {
            upper = mid;
        }
        else {
            return mid + 1;
        }
    }
    return upper;
}
/**
 * Checks if the given element has type information.
 *
 * Note: This function is not exhaustive and does not cover all possible cases.
 * However, it works sufficiently well for this parser.
 * @param element The element to check.
 * @returns True if the element has type information, false otherwise.
 */
export function hasTypeInfo(element) {
    return isTypeInfoInternal(element);
    function isTypeInfoInternal(node) {
        // Handle expressions
        if (node.type.startsWith("TS") ||
            node.type === "Literal" ||
            node.type === "TemplateLiteral") {
            return true;
        }
        if (node.type === "ArrowFunctionExpression" ||
            node.type === "FunctionExpression") {
            if (node.params.some((param) => !isTypeInfoInternal(param)))
                return false;
            if (node.returnType)
                return true;
            if (node.body.type !== "BlockStatement") {
                // Check for type assertions in concise return expressions, e.g., `() => value as Type`
                return isTypeInfoInternal(node.body);
            }
            return false;
        }
        if (node.type === "ObjectExpression") {
            return node.properties.every((prop) => isTypeInfoInternal(prop));
        }
        if (node.type === "ArrayExpression") {
            return node.elements.every((element) => element == null || isTypeInfoInternal(element));
        }
        if (node.type === "UnaryExpression") {
            // All UnaryExpression operators always produce a value of a specific type regardless of the argument's type annotation:
            //   - '!'      : always boolean
            //   - '+'/'-'/~: always number
            //   - 'typeof' : always string (type name)
            //   - 'void'   : always undefined
            //   - 'delete' : always boolean
            // Therefore, we always consider UnaryExpression as having type information.
            return true;
        }
        if (node.type === "UpdateExpression") {
            // All UpdateExpression operators ('++', '--') always produce a number value regardless of the argument's type annotation.
            // Therefore, we always consider UpdateExpression as having type information.
            return true;
        }
        if (node.type === "ConditionalExpression") {
            // ConditionalExpression (ternary) only has type information if both branches have type information.
            //   e.g., a ? 1 : 2  → true (both are literals)
            //         a ? 1 : b  → false (alternate has no type info)
            //         a ? b : c  → false (neither has type info)
            return (isTypeInfoInternal(node.consequent) &&
                isTypeInfoInternal(node.alternate));
        }
        if (node.type === "AssignmentExpression") {
            // AssignmentExpression only has type information if the right-hand side has type information.
            //   e.g., a = 1  → true (right is literal)
            //         a = b  → false (right has no type info)
            return isTypeInfoInternal(node.right);
        }
        if (node.type === "SequenceExpression") {
            // SequenceExpression only has type information if the last expression has type information.
            //   e.g., (a, b, 1)  → true (last is literal)
            //         (a, b, c)  → false (last has no type info)
            if (node.expressions.length === 0)
                return false;
            return isTypeInfoInternal(node.expressions[node.expressions.length - 1]);
        }
        // Handle destructuring and identifier patterns
        if (node.type === "Identifier" ||
            node.type === "ObjectPattern" ||
            node.type === "ArrayPattern" ||
            node.type === "AssignmentPattern" ||
            node.type === "RestElement") {
            return Boolean(node.typeAnnotation);
        }
        // Handle special nodes
        if (node.type === "SpreadElement") {
            return isTypeInfoInternal(node.argument);
        }
        if (node.type === "Property") {
            return isTypeInfoInternal(node.value);
        }
        return false;
    }
}
