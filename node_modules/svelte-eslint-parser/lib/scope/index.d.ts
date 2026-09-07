import type * as ESTree from "estree";
import type { TSESTree } from "@typescript-eslint/types";
import type * as eslint from "eslint";
/** Remove all scope, variable, and reference */
export declare function removeAllScopeAndVariableAndReference(target: ESTree.Node | TSESTree.Node, info: {
    visitorKeys?: {
        [type: string]: string[];
    } | {
        readonly [type: string]: readonly string[] | undefined;
    };
    scopeManager: eslint.Scope.ScopeManager;
}): void;
/**
 * Gets the scope for the current node
 */
export declare function getScopeFromNode(scopeManager: eslint.Scope.ScopeManager, currentNode: ESTree.Node): eslint.Scope.Scope;
/**
 * Find the variable of a given identifier.
 */
export declare function findVariable(scopeManager: eslint.Scope.ScopeManager, node: ESTree.Identifier): eslint.Scope.Variable | null;
/**
 * Gets the scope for the Program node
 */
export declare function getProgramScope(scopeManager: eslint.Scope.ScopeManager): eslint.Scope.Scope;
/** Remove variable */
export declare function removeIdentifierVariable(node: ESTree.Pattern | TSESTree.BindingName | TSESTree.RestElement | TSESTree.DestructuringPattern, scope: eslint.Scope.Scope): void;
/** Get all references */
export declare function getAllReferences(node: ESTree.Pattern | TSESTree.BindingName | TSESTree.RestElement | TSESTree.DestructuringPattern, scope: eslint.Scope.Scope): Iterable<eslint.Scope.Reference>;
/** Remove reference */
export declare function removeIdentifierReference(node: ESTree.Identifier, scope: eslint.Scope.Scope): boolean;
/** Remove reference */
export declare function removeReference(reference: eslint.Scope.Reference, baseScope: eslint.Scope.Scope): void;
/** Remove scope */
export declare function removeScope(scopeManager: eslint.Scope.ScopeManager, scope: eslint.Scope.Scope): void;
/** Replace scope */
export declare function replaceScope(scopeManager: eslint.Scope.ScopeManager, scope: eslint.Scope.Scope, newChildScopes?: eslint.Scope.Scope[]): void;
/**
 * Add variable to array
 */
export declare function addVariable(list: eslint.Scope.Variable[], variable: eslint.Scope.Variable): void;
/**
 * Add reference to array
 */
export declare function addReference(list: eslint.Scope.Reference[], reference: eslint.Scope.Reference): void;
/**
 * Add all references to array
 */
export declare function addAllReferences(list: eslint.Scope.Reference[], elements: eslint.Scope.Reference[]): void;
/**
 * Simplify scope data.
 * @deprecated For Debug
 */
export declare function simplifyScope(scope: eslint.Scope.Scope): unknown;
