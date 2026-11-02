import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// The cross-device sync is tested elsewhere; here it is only watched, so the storage rules show: which
// languages sync, and what a reset tells the server.
const sync = vi.hoisted(() => ({
	stampLocalDraft: vi.fn(() => 'stamp-1'),
	queueDraftPush: vi.fn(),
	forgetLocalDraftStamp: vi.fn(),
	removeRemoteDraft: vi.fn()
}));
vi.mock('./draft-sync.svelte', () => sync);

import { CODE_KEY_PREFIX, codeStorageKey } from './code-storage-key';
import { loadUserCode } from './load-user-code';
import { saveUserCode } from './save-user-code';
import { resetUserCode } from './reset-user-code';
import { loadDsaLanguage, saveDsaLanguage } from './dsa-language-preference';
import { DSA_LANGUAGES, detectLanguage, isLanguageSelectable } from './detect-language';
import { questionsById } from '$processes/ide-content/curriculum-index';
import type { QuestionContent } from '$data/curriculum/types';

const LANGUAGES = ['python', 'javascript', 'cpp', 'java', 'go', 'rust'];

// A localStorage that lives in a Map, and can be told to fail like a full or disabled one.
function memoryStorage() {
	const items = new Map<string, string>();
	let broken = false;
	const guard = () => {
		if (broken) throw new Error('storage unavailable');
	};
	return {
		items,
		breakIt: () => (broken = true),
		getItem: (k: string) => (guard(), items.get(k) ?? null),
		setItem: (k: string, v: string) => (guard(), void items.set(k, v)),
		removeItem: (k: string) => (guard(), void items.delete(k))
	};
}

let storage: ReturnType<typeof memoryStorage>;
beforeEach(() => {
	storage = memoryStorage();
	vi.stubGlobal('window', {});
	vi.stubGlobal('localStorage', storage);
	for (const fn of Object.values(sync)) fn.mockClear();
});
afterEach(() => {
	vi.unstubAllGlobals();
	vi.restoreAllMocks();
});

describe('codeStorageKey', () => {
	it('keeps Python on the original key, so existing drafts are still found', () => {
		expect(codeStorageKey('sheet-count-pairs')).toBe(`${CODE_KEY_PREFIX}sheet-count-pairs`);
		expect(codeStorageKey('sheet-count-pairs', 'python')).toBe(
			`${CODE_KEY_PREFIX}sheet-count-pairs`
		);
	});

	it('gives every other language its own key, and no two languages share one', () => {
		const keys = LANGUAGES.map((l) => codeStorageKey('q', l));
		expect(new Set(keys).size).toBe(LANGUAGES.length);
		expect(codeStorageKey('q', 'java')).toBe(`${CODE_KEY_PREFIX}q__java`);
	});

	// "<id>__<language>" is only unambiguous while no question id contains "__". Ids are kebab-case today;
	// this fails the day one is not, instead of letting two questions share a draft.
	it('cannot be confused with another question, because no question id contains "__"', () => {
		const ids = [...questionsById.keys()];
		expect(ids.length).toBeGreaterThan(1000);
		expect(ids.filter((id) => id.includes('__'))).toEqual([]);
	});
});

describe('saving and loading a draft', () => {
	it('returns the starter when nothing was saved', () => {
		expect(loadUserCode('q', 'STARTER', 'go')).toBe('STARTER');
	});

	it('round-trips a draft in each language, independently', () => {
		for (const lang of LANGUAGES) saveUserCode('q', `code in ${lang}`, lang);
		for (const lang of LANGUAGES)
			expect(loadUserCode('q', 'STARTER', lang)).toBe(`code in ${lang}`);
	});

	it('keeps a draft per question', () => {
		saveUserCode('one', 'A', 'cpp');
		saveUserCode('two', 'B', 'cpp');
		expect(loadUserCode('one', '', 'cpp')).toBe('A');
		expect(loadUserCode('two', '', 'cpp')).toBe('B');
	});

	it('keeps an empty draft as empty, not as the starter', () => {
		saveUserCode('q', '', 'rust');
		expect(loadUserCode('q', 'STARTER', 'rust')).toBe('');
	});

	it('syncs a Python draft across devices, and no other language', () => {
		saveUserCode('q', 'py', 'python');
		expect(sync.queueDraftPush).toHaveBeenCalledWith('q', 'py', 'stamp-1');
		sync.queueDraftPush.mockClear();
		for (const lang of LANGUAGES.filter((l) => l !== 'python')) saveUserCode('q', 'x', lang);
		expect(sync.queueDraftPush).not.toHaveBeenCalled();
	});

	it('falls back to the starter, and says so, when storage cannot be read', () => {
		const error = vi.spyOn(console, 'error').mockImplementation(() => {});
		storage.breakIt();
		expect(loadUserCode('q', 'STARTER', 'java')).toBe('STARTER');
		expect(error).toHaveBeenCalled();
	});

	it('does not throw when storage cannot be written', () => {
		vi.spyOn(console, 'error').mockImplementation(() => {});
		storage.breakIt();
		expect(() => saveUserCode('q', 'x', 'java')).not.toThrow();
	});

	it('does nothing on the server, where there is no window', () => {
		vi.unstubAllGlobals();
		expect(loadUserCode('q', 'STARTER', 'go')).toBe('STARTER');
		expect(() => saveUserCode('q', 'x', 'go')).not.toThrow();
		expect(() => resetUserCode('q')).not.toThrow();
		expect(sync.queueDraftPush).not.toHaveBeenCalled();
	});
});

describe('resetting a draft', () => {
	const fill = () => LANGUAGES.forEach((l) => saveUserCode('q', `code ${l}`, l));

	it('resets only the language you are in when it is not Python', () => {
		fill();
		resetUserCode('q', 'java');
		expect(loadUserCode('q', 'STARTER', 'java')).toBe('STARTER');
		for (const lang of LANGUAGES.filter((l) => l !== 'java'))
			expect(loadUserCode('q', 'STARTER', lang)).toBe(`code ${lang}`);
		expect(sync.removeRemoteDraft).not.toHaveBeenCalled();
		expect(sync.forgetLocalDraftStamp).not.toHaveBeenCalled();
	});

	it('resets Python, and tells the server, without touching the other languages', () => {
		fill();
		resetUserCode('q', 'python');
		expect(loadUserCode('q', 'STARTER', 'python')).toBe('STARTER');
		expect(loadUserCode('q', 'STARTER', 'rust')).toBe('code rust');
		expect(sync.forgetLocalDraftStamp).toHaveBeenCalledWith('q');
		expect(sync.removeRemoteDraft).toHaveBeenCalledWith('q');
	});

	it('resets every language at once when none is named (Re-attempt)', () => {
		fill();
		resetUserCode('q');
		for (const lang of LANGUAGES) expect(loadUserCode('q', 'STARTER', lang)).toBe('STARTER');
		expect(sync.removeRemoteDraft).toHaveBeenCalledWith('q');
	});

	it('leaves other questions alone', () => {
		saveUserCode('q', 'mine', 'go');
		saveUserCode('other', 'theirs', 'go');
		resetUserCode('q');
		expect(loadUserCode('other', 'STARTER', 'go')).toBe('theirs');
	});

	it('does not throw when storage cannot be written', () => {
		vi.spyOn(console, 'error').mockImplementation(() => {});
		storage.breakIt();
		expect(() => resetUserCode('q', 'java')).not.toThrow();
		expect(() => resetUserCode('q')).not.toThrow();
	});
});

describe('the remembered language', () => {
	it('round-trips each DSA language', () => {
		for (const lang of DSA_LANGUAGES) {
			saveDsaLanguage(lang);
			expect(loadDsaLanguage()).toBe(lang);
		}
	});

	it('is null before anything was chosen', () => {
		expect(loadDsaLanguage()).toBeNull();
	});

	it('ignores a stored value that is not a language, so a bad value cannot select a missing runtime', () => {
		storage.setItem('trentorch_dsa_language', 'cobol');
		expect(loadDsaLanguage()).toBeNull();
		storage.setItem('trentorch_dsa_language', 'sql');
		expect(loadDsaLanguage()).toBeNull();
	});

	it('does not throw when storage is unavailable, either way', () => {
		storage.breakIt();
		expect(loadDsaLanguage()).toBeNull();
		expect(() => saveDsaLanguage('go')).not.toThrow();
	});

	it('does nothing on the server', () => {
		vi.unstubAllGlobals();
		expect(loadDsaLanguage()).toBeNull();
		expect(() => saveDsaLanguage('go')).not.toThrow();
	});
});

describe('detect-language', () => {
	const content = (kind: string | undefined, id = 'q', tags: string[] = []) =>
		({ id, metadata: { kind, tags } }) as unknown as QuestionContent;

	it('lets the student pick a language only on DSA questions', () => {
		expect(isLanguageSelectable(content('dsa'))).toBe(true);
		expect(isLanguageSelectable(content('problemset'))).toBe(false);
		expect(isLanguageSelectable(content(undefined))).toBe(false);
	});

	it('offers exactly the six DSA languages, Python first', () => {
		expect(DSA_LANGUAGES).toEqual(['python', 'javascript', 'cpp', 'java', 'go', 'rust']);
	});

	it('detects Python for an ordinary question and SQL for a SQL one', () => {
		expect(detectLanguage(content(undefined, 'linear-regression'))).toBe('python');
		expect(detectLanguage(content(undefined, 'db-sql-group-by', ['sql']))).toBe('sql');
	});
});
