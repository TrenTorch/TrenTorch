import katex from 'katex';
import type { KatexOptions } from 'katex';
import type { MarkedExtension, TokenizerExtension, RendererExtension, Tokens } from 'marked';

export interface MarkedKatexOptions extends KatexOptions {
  nonStandard?: boolean
}

interface KatexToken extends Tokens.Generic {
  type: 'inlineKatex' | 'blockKatex';
  text: string;
  displayMode: boolean;
}

const inlineRule = /^(\${1,2})(?!\$)((?:\\.|[^\\\n])*?(?:\\.|[^\\\n\$]))\1(?=[\s?!\.,:？！。，：]|$)/;
const inlineRuleNonStandard = /^(\${1,2})(?!\$)((?:\\.|[^\\\n])*?(?:\\.|[^\\\n\$]))\1/; // Non-standard, even if there are no spaces before and after $ or $$, try to parse

const blockRule = /^(\${1,2})\n((?:\\[^]|[^\\])+?)\n\1(?:\n|$)/;

export default function markedKatex(options: MarkedKatexOptions = {}): MarkedExtension {
  return {
    extensions: [
      inlineKatex(options, createRenderer(options, false)),
      blockKatex(options, createRenderer(options, true)),
    ],
  };
}

function createRenderer(options: MarkedKatexOptions, newlineAfter: boolean) {
  return (token: KatexToken) => katex.renderToString(token.text, { ...options, displayMode: token.displayMode }) + (newlineAfter ? '\n' : '');
}

function inlineKatex(options: MarkedKatexOptions, renderer: (token: KatexToken) => string): TokenizerExtension & RendererExtension {
  const nonStandard = options && options.nonStandard;
  const ruleReg = nonStandard ? inlineRuleNonStandard : inlineRule;
  return {
    name: 'inlineKatex',
    level: 'inline',
    start(src: string) {
      let index;
      let indexSrc = src;

      while (indexSrc) {
        index = indexSrc.indexOf('$');
        if (index === -1) {
          return;
        }
        const f = nonStandard ? index > -1 : index === 0 || indexSrc.charAt(index - 1) === ' ';
        if (f) {
          const possibleKatex = indexSrc.substring(index);

          if (possibleKatex.match(ruleReg)) {
            return index;
          }
        }

        indexSrc = indexSrc.substring(index + 1).replace(/^\$+/, '');
      }
    },
    tokenizer(src: string, _tokens: Tokens.Generic[]) {
      const match = src.match(ruleReg);
      if (match) {
        return {
          type: 'inlineKatex',
          raw: match[0],
          text: match[2].trim(),
          displayMode: match[1].length === 2,
        };
      }
    },
    renderer: renderer as (token: Tokens.Generic) => string,
  };
}

function blockKatex(options: MarkedKatexOptions, renderer: (token: KatexToken) => string): TokenizerExtension & RendererExtension {
  return {
    name: 'blockKatex',
    level: 'block',
    tokenizer(src: string, _tokens: Tokens.Generic[]) {
      const match = src.match(blockRule);
      if (match) {
        return {
          type: 'blockKatex',
          raw: match[0],
          text: match[2].trim(),
          displayMode: match[1].length === 2,
        };
      }
    },
    renderer: renderer as (token: Tokens.Generic) => string,
  };
}
