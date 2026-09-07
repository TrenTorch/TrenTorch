/** Class value accepted by the callable merger (`createMerger()`). */
type ClassNameValue = ClassNameArray | string | null | undefined | 0 | 0n | false;
type ClassNameArray = readonly ClassNameValue[];
/** Built-in merger configuration shape. */
type Config<ClassGroupIds extends string, ThemeGroupIds extends string> = ConfigGroupsPart<ClassGroupIds, ThemeGroupIds>;
/**
 * Dynamic merger config groups. When merging configs, use `override` or `extend`.
 */
interface ConfigGroupsPart<ClassGroupIds extends string, ThemeGroupIds extends string> {
    /**
     * Theme scales used in classGroups.
     *
     * The keys are the same as in the Tailwind config but the values are sometimes defined more broadly.
     */
    theme: NoInfer<ThemeObject<ThemeGroupIds>>;
    /**
     * Object with groups of classes.
     *
     * @example
     * {
     *     // Creates group of classes `group`, `of` and `classes`
     *     'group-id': ['group', 'of', 'classes'],
     *     // Creates group of classes `look-at-me-other` and `look-at-me-group`.
     *     'other-group': [{ 'look-at-me': ['other', 'group']}]
     * }
     */
    classGroups: NoInfer<Record<ClassGroupIds, ClassGroup<ThemeGroupIds>>>;
    /**
     * Conflicting classes across groups.
     *
     * The key is the ID of a class group which creates a conflict, values are IDs of class groups which receive a conflict. That means if a class from from the key ID is present, all preceding classes from the values are removed.
     *
     * A class group ID is the key of a class group in the classGroups object.
     *
     * @example { gap: ['gap-x', 'gap-y'] }
     */
    conflictingClassGroups: NoInfer<Partial<Record<ClassGroupIds, readonly ClassGroupIds[]>>>;
    /**
     * Postfix modifiers conflicting with other class groups.
     *
     * A class group ID is the key of a class group in classGroups object.
     *
     * @example { 'font-size': ['leading'] }
     */
    conflictingClassGroupModifiers: NoInfer<Partial<Record<ClassGroupIds, readonly ClassGroupIds[]>>>;
    /**
     * Class group IDs which should be resolved again with their postfix modifier attached.
     *
     * This is needed when a slash can make the full class name belong to a different class group than the part before the slash.
     *
     * @example ['container-type'] // `@container-size/sidebar` should resolve differently from `@container-size`
     */
    postfixLookupClassGroups?: readonly NoInferString<ClassGroupIds>[];
    /**
     * Modifiers whose order among multiple modifiers should be preserved because their order changes which element gets targeted.
     *
     * Classes with these modifiers are not overwritten by peers that only differ in order-sensitive modifier position.
     */
    orderSensitiveModifiers: string[];
}
type ThemeObject<ThemeGroupIds extends string> = Record<ThemeGroupIds, ClassGroup<ThemeGroupIds>>;
type ClassGroup<ThemeGroupIds extends string> = readonly ClassDefinition<ThemeGroupIds>[];
type ClassDefinition<ThemeGroupIds extends string> = string | ClassValidator | ThemeGetter | ClassObject<ThemeGroupIds>;
type ClassValidator = (classPart: string) => boolean;
interface ThemeGetter {
    (theme: ThemeObject<AnyThemeGroupIds>): ClassGroup<AnyClassGroupIds>;
    isThemeGetter: true;
}
type ClassObject<ThemeGroupIds extends string> = Record<string, readonly ClassDefinition<ThemeGroupIds>[]>;
/**
 * Hack from https://stackoverflow.com/questions/56687668/a-way-to-disable-type-argument-inference-in-generics/56688073#56688073
 *
 * Could be replaced with NoInfer utility type from TypeScript (https://www.typescriptlang.org/docs/handbook/utility-types.html#noinfertype), but that is only supported in TypeScript 5.4 or higher, so I should wait some time before using it.
 */
type NoInfer<T> = [T][T extends unknown ? 0 : never];
/**
 * Special-purpose NoInfer variant for string unions used in array item positions.
 *
 * The NoInfer helper above doesn't prevent inference from array items in all cases, so this keeps
 * config arrays like `postfixLookupClassGroups` from defining or narrowing class group IDs.
 * Prefer TypeScript's built-in `NoInfer` when the minimum supported version is 5.4+.
 */
type NoInferString<T extends string> = T extends infer S ? S & string : never;
type AnyClassGroupIds = string;
type AnyThemeGroupIds = string;
/** Merger config with unrestricted class-group and theme-group IDs. */
type AnyConfig = Config<AnyClassGroupIds, AnyThemeGroupIds>;
/** Merger config: `override` replaces class groups, `extend` appends to them. */
interface ConfigExtension {
    override?: Partial<AnyConfig>;
    extend?: Partial<AnyConfig>;
}

/** Merger config for the built-in Tailwind conflict resolver. */
type TWMergeConfig = ConfigExtension & Partial<AnyConfig> & {
    extend?: Partial<AnyConfig>;
    override?: Partial<AnyConfig>;
};
type TWMConfig = {
    /**
     * Whether to merge conflicting Tailwind classes.
     * @default true
     */
    twMerge?: boolean;
    /**
     * Custom merger config (`extend` / `override`, or legacy flat fields).
     */
    twMergeConfig?: TWMergeConfig;
};
type TVConfig = TWMConfig;

export type { ClassNameValue as C, TWMConfig as T, TVConfig as a, TWMergeConfig as b };
