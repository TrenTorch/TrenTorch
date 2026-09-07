// Reserved characters that force PostgREST-style quoting: `[,()]` (which the
// server reads as condition/list delimiters) plus `"`/`\` (escaped inside quotes).
const PostgrestReservedCharsRegexp = /[,()"\\]/;
const needsQuoting = (value) => PostgrestReservedCharsRegexp.test(value) || value !== value.trim();
const quote = (value) => `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
const serializeScalar = (value) => {
    const serialized = value === null ? 'null' : String(value);
    return needsQuoting(serialized) ? quote(serialized) : serialized;
};
const serializeIsValue = (value) => value === null ? 'null' : String(value);
// Builds the `operator.value` portion of a filter (everything after `column=`).
const serialize = (operator, value) => {
    if (operator === 'in') {
        const values = Array.isArray(value) ? value : [value];
        if (values.length === 0) {
            throw new Error('Realtime `in` filter requires at least one value.');
        }
        const items = Array.from(new Set(values))
            .map((v) => serializeScalar(v))
            .join(',');
        return `in.(${items})`;
    }
    if (operator === 'is') {
        return `is.${serializeIsValue(value)}`;
    }
    return `${operator}.${serializeScalar(value)}`;
};
/**
 * Fluent builder for Postgres Changes `filter` strings.
 *
 * Each method appends a single `column=operator.value` condition. Multiple
 * conditions are combined with commas, which the Realtime server applies as an
 * `AND`. Pass an instance straight to `channel.on('postgres_changes', …)` — the
 * SDK serializes it to a string automatically — or call {@link build} to obtain
 * the string yourself.
 *
 * The builder mirrors the `postgrest-js` filter API (`eq`, `neq`, `in`, `like`,
 * `not`, …) for the operators that Realtime supports. Values containing reserved
 * characters (`,`, `(`, `)`, `"`, `\`) — or surrounding whitespace — are
 * automatically double-quoted and escaped the same way PostgREST does, so they
 * survive the server's filter parser; all other values are sent verbatim.
 *
 * The filter is snapshotted when passed to `channel.on(...)`; mutating the
 * builder afterwards does not affect an existing subscription. An empty builder
 * serializes to `''`, which the server treats as "no filter".
 *
 * @example
 * channel.on('postgres_changes', {
 *   event: '*',
 *   schema: 'public',
 *   table: 'users',
 *   filter: postgresChangesFilter().eq('id', 1).lt('age', 30), // → 'id=eq.1,age=lt.30'
 * }, (payload) => { ... })
 */
export class RealtimePostgresFilterBuilder {
    constructor() {
        this.filters = [];
    }
    add(column, operator, value, negate = false) {
        const prefix = negate ? 'not.' : '';
        this.filters.push(`${column}=${prefix}${serialize(operator, value)}`);
        return this;
    }
    /** Match rows where `column` equals `value` (`column=eq.value`). */
    eq(column, value) {
        return this.add(column, 'eq', value);
    }
    /** Match rows where `column` does not equal `value` (`column=neq.value`). */
    neq(column, value) {
        return this.add(column, 'neq', value);
    }
    /** Match rows where `column` is greater than `value` (`column=gt.value`). */
    gt(column, value) {
        return this.add(column, 'gt', value);
    }
    /** Match rows where `column` is greater than or equal to `value` (`column=gte.value`). */
    gte(column, value) {
        return this.add(column, 'gte', value);
    }
    /** Match rows where `column` is less than `value` (`column=lt.value`). */
    lt(column, value) {
        return this.add(column, 'lt', value);
    }
    /** Match rows where `column` is less than or equal to `value` (`column=lte.value`). */
    lte(column, value) {
        return this.add(column, 'lte', value);
    }
    /**
     * Match rows where `column` is one of `values` (`column=in.(a,b,c)`).
     * Requires at least one value; duplicates are removed. An element containing a
     * reserved character is double-quoted (`in.("a,b",c)`), so commas inside an
     * element are preserved. `null` is intentionally not accepted (`IN (null)`
     * never matches in SQL) — use `is`/`not('col','is',null)` for null checks.
     */
    in(column, values) {
        return this.add(column, 'in', values);
    }
    /** Match rows where `column` matches the case-sensitive `pattern` (`column=like.pattern`). */
    like(column, pattern) {
        return this.add(column, 'like', pattern);
    }
    /** Match rows where `column` matches the case-insensitive `pattern` (`column=ilike.pattern`). */
    ilike(column, pattern) {
        return this.add(column, 'ilike', pattern);
    }
    /** Match rows where `column` matches the POSIX regex `pattern` (`column=match.pattern`). */
    match(column, pattern) {
        return this.add(column, 'match', pattern);
    }
    /** Match rows where `column` matches the case-insensitive POSIX regex `pattern` (`column=imatch.pattern`). */
    imatch(column, pattern) {
        return this.add(column, 'imatch', pattern);
    }
    /**
     * Match rows where `column` `IS` the given value (`column=is.null`).
     * Accepts `null`, a boolean, or the keywords `'null' | 'true' | 'false' | 'unknown'`.
     */
    is(column, value) {
        return this.add(column, 'is', value);
    }
    /** Match rows where `column` is distinct from `value` (`column=isdistinct.value`). NULL-safe inequality. */
    isDistinct(column, value) {
        return this.add(column, 'isdistinct', value);
    }
    not(column, operator, value) {
        return this.add(column, operator, value, true);
    }
    /**
     * Serialize all conditions into the comma-separated (AND) filter string.
     *
     * Conditions are joined by commas, which the server applies as `AND`. A scalar
     * value (or single `in` element) that contains a reserved character — `,`,
     * `(`, `)`, `"`, `\` — or surrounding whitespace is double-quoted and escaped
     * the way PostgREST does, so commas inside a value are preserved rather than
     * read as a condition boundary.
     */
    build() {
        return this.filters.join(',');
    }
    /** Alias for {@link build}; lets the builder be used wherever a string is expected. */
    toString() {
        return this.build();
    }
}
/**
 * Create a {@link RealtimePostgresFilterBuilder} for composing a Postgres
 * Changes `filter`. Conditions are combined with `AND`.
 *
 * @example
 * import { postgresChangesFilter } from '@supabase/realtime-js'
 *
 * channel.on('postgres_changes', {
 *   event: 'UPDATE',
 *   schema: 'public',
 *   table: 'orders',
 *   filter: postgresChangesFilter().gt('amount', 100).eq('status', 'open'),
 * }, (payload) => { ... })
 */
export const postgresChangesFilter = () => new RealtimePostgresFilterBuilder();
//# sourceMappingURL=RealtimePostgresFilterBuilder.js.map