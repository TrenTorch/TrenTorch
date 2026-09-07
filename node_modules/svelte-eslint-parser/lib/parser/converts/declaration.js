/** Convert for DeclarationTag */
export function convertDeclarationTag(node, parent, ctx) {
    const declarationTag = {
        type: "SvelteDeclarationTag",
        declaration: null,
        parent,
        ...ctx.getConvertLocation(node),
    };
    ctx.scriptLet.addDeclaration(node.declaration, declarationTag, (declaration) => {
        declarationTag.declaration = declaration;
    });
    return declarationTag;
}
