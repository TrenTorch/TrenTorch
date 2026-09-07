import { getStaticValue } from '@eslint-community/eslint-utils';
import { getScope } from '../utils/ast-utils.js';
import { createRule } from '../utils/index.js';
export default createRule('no-bind-value-on-checkable-inputs', {
    meta: {
        hasSuggestions: true,
        docs: {
            description: 'disallow useless `bind:value` on `<input type="checkbox">` and `<input type="radio">`',
            category: 'Possible Errors',
            recommended: false
        },
        schema: [],
        type: 'problem',
        messages: {
            checkboxValueBinding: '`bind:value` does not work on checkbox inputs. Did you mean `bind:checked` or `bind:group`?',
            radioValueBinding: '`bind:value` does not work on radio inputs. Did you mean `bind:group`?', // svelte compiler disallows `bind:checked` on radios
            checkedSuggestion: 'Change `bind:value` to `bind:checked`.',
            groupSuggestion: 'Change `bind:value` to `bind:group`.'
        }
    },
    create(context) {
        return {
            "SvelteElement[name.name='input']"(node) {
                function getType() {
                    const typeAttr = node.startTag?.attributes.find((attr) => attr.type === 'SvelteAttribute' && attr.key.name.toLowerCase() === 'type');
                    if (!typeAttr)
                        return null;
                    if (typeAttr.value.length !== 1)
                        return null;
                    const typeValue = typeAttr.value[0];
                    if (typeValue.type === 'SvelteLiteral') {
                        // <input type="checkbox" />
                        return typeValue.value.toLowerCase();
                    }
                    if (typeValue.type === 'SvelteMustacheTag') {
                        const staticValue = getStaticValue(typeValue.expression, getScope(context, typeValue.expression));
                        if (typeof staticValue?.value !== 'string')
                            return null;
                        // <input type={"checkbox"} />
                        return staticValue.value.toLowerCase();
                    }
                    return null;
                }
                const type = getType();
                if (!type || (type !== 'checkbox' && type !== 'radio'))
                    return;
                const bindValue = node.startTag?.attributes.find((attr) => attr.type === 'SvelteDirective' &&
                    attr.kind === 'Binding' &&
                    attr.key.name.name === 'value');
                if (!bindValue)
                    return;
                function suggestion(suggestionType, bindValue // make typescript happy
                ) {
                    return {
                        messageId: `${suggestionType}Suggestion`,
                        fix(fixer) {
                            if (bindValue.shorthand)
                                return fixer.replaceText(bindValue, `bind:${suggestionType}={value}`);
                            return fixer.replaceText(bindValue.key, `bind:${suggestionType}`);
                        }
                    };
                }
                context.report({
                    node: bindValue,
                    messageId: `${type}ValueBinding`,
                    suggest: type === 'checkbox'
                        ? [suggestion('checked', bindValue), suggestion('group', bindValue)]
                        : [suggestion('group', bindValue)]
                });
            }
        };
    }
});
