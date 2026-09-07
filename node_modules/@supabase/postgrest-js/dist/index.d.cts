//#region src/PostgrestError.d.ts
/**
 * Error format
 *
 * Returned by every PostgREST request that fails. When something fails, the
 * single most useful field is usually `hint` — Postgres often returns the
 * actionable fix there, not in `message`. Always log the full object (e.g.
 * `console.error(error)`); logging only `error.message` hides the hint.
 *
 * Read the fields in roughly this order of usefulness:
 *
 * - `hint` — actionable guidance from the database when available. For
 *   permission-denied errors (`42501`), this is the literal SQL to fix the
 *   problem, e.g.
 *   `"Grant the required privileges to the current role with: GRANT SELECT ON public.users TO anon;"`.
 *   Missing column? `hint` suggests the column you probably meant. Whenever
 *   Postgres knows the fix, it puts it in `hint`.
 * - `code` — stable error code from PostgREST (e.g. `PGRST301`) or Postgres
 *   (e.g. `42501`). Branch on this rather than on `message` text.
 * - `details` — extra context, often the offending value, key, or row.
 * - `message` — human-readable summary. Useful in UI strings; less useful
 *   for debugging.
 *
 * {@link https://postgrest.org/en/stable/api.html?highlight=options#errors-and-http-status-codes}
 */
declare class PostgrestError extends Error {
  details: string;
  hint: string;
  code: string;
  /**
   * @example
   * ```ts
   * import PostgrestError from '@supabase/postgrest-js'
   *
   * throw new PostgrestError({
   *   message: 'Row level security prevented the request',
   *   details: 'RLS denied the insert',
   *   hint: 'Check your policies',
   *   code: 'PGRST301',
   * })
   * ```
   */
  constructor(context: {
    message: string;
    details: string;
    hint: string;
    code: string;
  });
  toJSON(): {
    name: string;
    message: string;
    details: string;
    hint: string;
    code: string;
  };
}
//#endregion
//#region src/types/common/common.d.ts
type Fetch = typeof fetch;
type GenericRelationship = {
  foreignKeyName: string;
  columns: string[];
  isOneToOne?: boolean;
  referencedRelation: string;
  referencedColumns: string[];
};
type GenericTable = {
  Row: Record<string, unknown>;
  Insert: Record<string, unknown>;
  Update: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericUpdatableView = {
  Row: Record<string, unknown>;
  Insert: Record<string, unknown>;
  Update: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericNonUpdatableView = {
  Row: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericView = GenericUpdatableView | GenericNonUpdatableView;
type GenericSetofOption = {
  isSetofReturn?: boolean | undefined;
  isOneToOne?: boolean | undefined;
  isNotNullable?: boolean | undefined;
  to: string;
  from: string;
};
type GenericFunction = {
  Args: Record<string, unknown> | never;
  Returns: unknown;
  SetofOptions?: GenericSetofOption;
};
type GenericSchema = {
  Tables: Record<string, GenericTable>;
  Views: Record<string, GenericView>;
  Functions: Record<string, GenericFunction>;
};
type ClientServerOptions = {
  PostgrestVersion?: string;
};
//#endregion
//#region src/select-query-parser/types.d.ts
type AggregateWithoutColumnFunctions = 'count';
type AggregateWithColumnFunctions = 'sum' | 'avg' | 'min' | 'max' | AggregateWithoutColumnFunctions;
type AggregateFunctions = AggregateWithColumnFunctions;
type Json = string | number | boolean | null | {
  [key: string]: Json | undefined;
} | Json[];
type PostgresSQLNumberTypes = 'int2' | 'int4' | 'int8' | 'float4' | 'float8' | 'numeric';
type PostgresSQLStringTypes = 'bytea' | 'bpchar' | 'varchar' | 'date' | 'text' | 'citext' | 'time' | 'timetz' | 'timestamp' | 'timestamptz' | 'uuid' | 'vector';
type SingleValuePostgreSQLTypes = PostgresSQLNumberTypes | PostgresSQLStringTypes | 'bool' | 'json' | 'jsonb' | 'void' | 'record' | string;
type ArrayPostgreSQLTypes = `_${SingleValuePostgreSQLTypes}`;
type TypeScriptSingleValueTypes<T extends SingleValuePostgreSQLTypes> = T extends 'bool' ? boolean : T extends PostgresSQLNumberTypes ? number : T extends PostgresSQLStringTypes ? string : T extends 'json' | 'jsonb' ? Json : T extends 'void' ? undefined : T extends 'record' ? Record<string, unknown> : unknown;
type StripUnderscore<T extends string> = T extends `_${infer U}` ? U : T;
type PostgreSQLTypes = SingleValuePostgreSQLTypes | ArrayPostgreSQLTypes;
type TypeScriptTypes<T extends PostgreSQLTypes> = T extends ArrayPostgreSQLTypes ? TypeScriptSingleValueTypes<StripUnderscore<Extract<T, SingleValuePostgreSQLTypes>>>[] : TypeScriptSingleValueTypes<T>;
type UnionToIntersection$1<U> = (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;
type LastOf$1<T> = UnionToIntersection$1<T extends any ? () => T : never> extends (() => infer R) ? R : never;
type Push<T extends any[], V> = [...T, V];
type UnionToTuple<T, L$1 = LastOf$1<T>, N = ([T] extends [never] ? true : false)> = N extends true ? [] : Push<UnionToTuple<Exclude<T, L$1>>, L$1>;
type UnionToArray<T> = UnionToTuple<T>;
type ExtractFirstProperty<T> = T extends { [K in keyof T]: infer U } ? U : never;
type ContainsNull<T> = null extends T ? true : false;
type IsNonEmptyArray<T> = Exclude<T, undefined> extends readonly [unknown, ...unknown[]] ? true : false;
type TablesAndViews$2<Schema extends GenericSchema> = Schema['Tables'] & Exclude<Schema['Views'], ''>;
//#endregion
//#region src/select-query-parser/parser.d.ts
/**
 * Parses a query.
 * A query is a sequence of nodes, separated by `,`, ensuring that there is
 * no remaining input after all nodes have been parsed.
 *
 * Returns an array of parsed nodes, or an error.
 */
type ParseQuery<Query extends string> = string extends Query ? GenericStringError : ParseNodes<EatWhitespace<Query>> extends [infer Nodes, `${infer Remainder}`] ? Nodes extends Ast.Node[] ? EatWhitespace<Remainder> extends '' ? SimplifyDeep<Nodes> : ParserError<`Unexpected input: ${Remainder}`> : ParserError<'Invalid nodes array structure'> : ParseNodes<EatWhitespace<Query>>;
/**
 * Notes: all `Parse*` types assume that their input strings have their whitespace
 * removed. They return tuples of ["Return Value", "Remainder of text"] or
 * a `ParserError`.
 */
/**
 * Parses a sequence of nodes, separated by `,`.
 *
 * Returns a tuple of ["Parsed fields", "Remainder of text"] or an error.
 */
type ParseNodes<Input extends string> = string extends Input ? GenericStringError : ParseNodesHelper<Input, []>;
type ParseNodesHelper<Input extends string, Nodes$1 extends Ast.Node[]> = ParseNode<Input> extends [infer Node, `${infer Remainder}`] ? Node extends Ast.Node ? EatWhitespace<Remainder> extends `,${infer Remainder}` ? ParseNodesHelper<EatWhitespace<Remainder>, [...Nodes$1, Node]> : [[...Nodes$1, Node], EatWhitespace<Remainder>] : ParserError<'Invalid node type in nodes helper'> : ParseNode<Input>;
/**
 * Parses a node.
 * A node is one of the following:
 * - `*`
 * - a field, as defined above
 * - a renamed field, `renamed_field:field`
 * - a spread field, `...field`
 */
type ParseNode<Input extends string> = Input extends '' ? ParserError<'Empty string'> : Input extends `*${infer Remainder}` ? [Ast.StarNode, EatWhitespace<Remainder>] : Input extends `...${infer Remainder}` ? ParseField<EatWhitespace<Remainder>> extends [infer TargetField, `${infer Remainder}`] ? TargetField extends Ast.FieldNode ? [{
  type: 'spread';
  target: TargetField;
}, EatWhitespace<Remainder>] : ParserError<'Invalid target field type in spread'> : ParserError<`Unable to parse spread resource at \`${Input}\``> : ParseIdentifier<Input> extends [infer NameOrAlias, `${infer Remainder}`] ? EatWhitespace<Remainder> extends `::${infer _}` ? ParseField<Input> : EatWhitespace<Remainder> extends `:${infer Remainder}` ? ParseField<EatWhitespace<Remainder>> extends [infer Field, `${infer Remainder}`] ? Field extends Ast.FieldNode ? [Omit<Field, 'alias'> & {
  alias: NameOrAlias;
}, EatWhitespace<Remainder>] : ParserError<'Invalid field type in alias parsing'> : ParserError<`Unable to parse renamed field at \`${Input}\``> : ParseField<Input> : ParserError<`Expected identifier at \`${Input}\``>;
/**
 * Parses a field without preceding alias.
 * A field is one of the following:
 * - a top-level `count` field: https://docs.postgrest.org/en/v12/references/api/aggregate_functions.html#the-case-of-count
 * - a field with an embedded resource
 *   - `field(nodes)`
 *   - `field!hint(nodes)`
 *   - `field!inner(nodes)`
 *   - `field!left(nodes)`
 *   - `field!hint!inner(nodes)`
 *   - `field!hint!left(nodes)`
 * - a field without an embedded resource (see {@link ParseNonEmbeddedResourceField})
 */
type ParseField<Input extends string> = Input extends '' ? ParserError<'Empty string'> : ParseIdentifier<Input> extends [infer Name, `${infer Remainder}`] ? Name extends 'count' ? ParseCountField<Input> : Remainder extends `!inner${infer Remainder}` ? ParseEmbeddedResource<EatWhitespace<Remainder>> extends [infer Children, `${infer Remainder}`] ? Children extends Ast.Node[] ? [{
  type: 'field';
  name: Name;
  innerJoin: true;
  children: Children;
}, Remainder] : ParserError<'Invalid children array in inner join'> : CreateParserErrorIfRequired<ParseEmbeddedResource<EatWhitespace<Remainder>>, `Expected embedded resource after "!inner" at \`${Remainder}\``> : EatWhitespace<Remainder> extends `!left${infer Remainder}` ? ParseEmbeddedResource<EatWhitespace<Remainder>> extends [infer Children, `${infer Remainder}`] ? Children extends Ast.Node[] ? [{
  type: 'field';
  name: Name;
  children: Children;
}, EatWhitespace<Remainder>] : ParserError<'Invalid children array in left join'> : CreateParserErrorIfRequired<ParseEmbeddedResource<EatWhitespace<Remainder>>, `Expected embedded resource after "!left" at \`${EatWhitespace<Remainder>}\``> : EatWhitespace<Remainder> extends `!${infer Remainder}` ? ParseIdentifier<EatWhitespace<Remainder>> extends [infer Hint, `${infer Remainder}`] ? EatWhitespace<Remainder> extends `!inner${infer Remainder}` ? ParseEmbeddedResource<EatWhitespace<Remainder>> extends [infer Children, `${infer Remainder}`] ? Children extends Ast.Node[] ? [{
  type: 'field';
  name: Name;
  hint: Hint;
  innerJoin: true;
  children: Children;
}, EatWhitespace<Remainder>] : ParserError<'Invalid children array in hint inner join'> : ParseEmbeddedResource<EatWhitespace<Remainder>> : ParseEmbeddedResource<EatWhitespace<Remainder>> extends [infer Children, `${infer Remainder}`] ? Children extends Ast.Node[] ? [{
  type: 'field';
  name: Name;
  hint: Hint;
  children: Children;
}, EatWhitespace<Remainder>] : ParserError<'Invalid children array in hint'> : ParseEmbeddedResource<EatWhitespace<Remainder>> : ParserError<`Expected identifier after "!" at \`${EatWhitespace<Remainder>}\``> : EatWhitespace<Remainder> extends `(${infer _}` ? ParseEmbeddedResource<EatWhitespace<Remainder>> extends [infer Children, `${infer Remainder}`] ? Children extends Ast.Node[] ? [{
  type: 'field';
  name: Name;
  children: Children;
}, EatWhitespace<Remainder>] : ParserError<'Invalid children array in field'> : ParseEmbeddedResource<EatWhitespace<Remainder>> : ParseNonEmbeddedResourceField<Input> : ParserError<`Expected identifier at \`${Input}\``>;
type ParseCountField<Input extends string> = ParseIdentifier<Input> extends ['count', `${infer Remainder}`] ? (EatWhitespace<Remainder> extends `()${infer Remainder_}` ? EatWhitespace<Remainder_> : EatWhitespace<Remainder>) extends `${infer Remainder}` ? Remainder extends `::${infer _}` ? ParseFieldTypeCast<Remainder> extends [infer CastType, `${infer Remainder}`] ? [{
  type: 'field';
  name: 'count';
  aggregateFunction: 'count';
  castType: CastType;
}, Remainder] : ParseFieldTypeCast<Remainder> : [{
  type: 'field';
  name: 'count';
  aggregateFunction: 'count';
}, Remainder] : never : ParserError<`Expected "count" at \`${Input}\``>;
/**
 * Parses an embedded resource, which is an opening `(`, followed by a sequence of
 * 0 or more nodes separated by `,`, then a closing `)`.
 *
 * Returns a tuple of ["Parsed fields", "Remainder of text"], an error,
 * or the original string input indicating that no opening `(` was found.
 */
type ParseEmbeddedResource<Input extends string> = Input extends `(${infer Remainder}` ? EatWhitespace<Remainder> extends `)${infer Remainder}` ? [[], EatWhitespace<Remainder>] : ParseNodes<EatWhitespace<Remainder>> extends [infer Nodes, `${infer Remainder}`] ? Nodes extends Ast.Node[] ? EatWhitespace<Remainder> extends `)${infer Remainder}` ? [Nodes, EatWhitespace<Remainder>] : ParserError<`Expected ")" at \`${EatWhitespace<Remainder>}\``> : ParserError<'Invalid nodes array in embedded resource'> : ParseNodes<EatWhitespace<Remainder>> : ParserError<`Expected "(" at \`${Input}\``>;
/**
 * Parses a field excluding embedded resources, without preceding field renaming.
 * This is one of the following:
 * - `field`
 * - `field.aggregate()`
 * - `field.aggregate()::type`
 * - `field::type`
 * - `field::type.aggregate()`
 * - `field::type.aggregate()::type`
 * - `field->json...`
 * - `field->json.aggregate()`
 * - `field->json.aggregate()::type`
 * - `field->json::type`
 * - `field->json::type.aggregate()`
 * - `field->json::type.aggregate()::type`
 */
type ParseNonEmbeddedResourceField<Input extends string> = ParseIdentifier<Input> extends [infer Name, `${infer Remainder}`] ? (Remainder extends `->${infer PathAndRest}` ? ParseJsonAccessor<Remainder> extends [infer PropertyName, infer PropertyType, `${infer Remainder}`] ? [{
  type: 'field';
  name: Name;
  alias: PropertyName;
  castType: PropertyType;
  jsonPath: JsonPathToAccessor<PathAndRest extends `${infer Path},${string}` ? Path : PathAndRest>;
}, Remainder] : ParseJsonAccessor<Remainder> : [{
  type: 'field';
  name: Name;
}, Remainder]) extends infer Parsed ? Parsed extends [infer Field, `${infer Remainder}`] ? (Remainder extends `::${infer _}` ? ParseFieldTypeCast<Remainder> extends [infer CastType, `${infer Remainder}`] ? [Omit<Field, 'castType'> & {
  castType: CastType;
}, Remainder] : ParseFieldTypeCast<Remainder> : [Field, Remainder]) extends infer Parsed ? Parsed extends [infer Field, `${infer Remainder}`] ? Remainder extends `.${infer _}` ? ParseFieldAggregation<Remainder> extends [infer AggregateFunction, `${infer Remainder}`] ? Remainder extends `::${infer _}` ? ParseFieldTypeCast<Remainder> extends [infer CastType, `${infer Remainder}`] ? [Omit<Field, 'castType'> & {
  aggregateFunction: AggregateFunction;
  castType: CastType;
}, Remainder] : ParseFieldTypeCast<Remainder> : [Field & {
  aggregateFunction: AggregateFunction;
}, Remainder] : ParseFieldAggregation<Remainder> : [Field, Remainder] : Parsed : never : Parsed : never : ParserError<`Expected identifier at \`${Input}\``>;
/**
 * Parses a JSON property accessor of the shape `->a->b->c`. The last accessor in
 * the series may convert to text by using the ->> operator instead of ->.
 *
 * Returns a tuple of ["Last property name", "Last property type", "Remainder of text"]
 */
type ParseJsonAccessor<Input extends string> = Input extends `->${infer Remainder}` ? Remainder extends `>${infer Remainder}` ? ParseIdentifier<Remainder> extends [infer Name, `${infer Remainder}`] ? [Name, 'text', EatWhitespace<Remainder>] : ParserError<'Expected property name after `->>`'> : ParseIdentifier<Remainder> extends [infer Name, `${infer Remainder}`] ? ParseJsonAccessor<Remainder> extends [infer PropertyName, infer PropertyType, `${infer Remainder}`] ? [PropertyName, PropertyType, EatWhitespace<Remainder>] : [Name, 'json', EatWhitespace<Remainder>] : ParserError<'Expected property name after `->`'> : ParserError<'Expected ->'>;
/**
 * Parses a field typecast (`::type`), returning a tuple of ["Type", "Remainder of text"].
 */
type ParseFieldTypeCast<Input extends string> = EatWhitespace<Input> extends `::${infer Remainder}` ? ParseIdentifier<EatWhitespace<Remainder>> extends [`${infer CastType}`, `${infer Remainder}`] ? [CastType, EatWhitespace<Remainder>] : ParserError<`Invalid type for \`::\` operator at \`${Remainder}\``> : ParserError<'Expected ::'>;
/**
 * Parses a field aggregation (`.max()`), returning a tuple of ["Aggregate function", "Remainder of text"]
 */
type ParseFieldAggregation<Input extends string> = EatWhitespace<Input> extends `.${infer Remainder}` ? ParseIdentifier<EatWhitespace<Remainder>> extends [`${infer FunctionName}`, `${infer Remainder}`] ? FunctionName extends Token.AggregateFunction ? EatWhitespace<Remainder> extends `()${infer Remainder}` ? [FunctionName, EatWhitespace<Remainder>] : ParserError<`Expected \`()\` after \`.\` operator \`${FunctionName}\``> : ParserError<`Invalid type for \`.\` operator \`${FunctionName}\``> : ParserError<`Invalid type for \`.\` operator at \`${Remainder}\``> : ParserError<'Expected .'>;
/**
 * Parses a (possibly double-quoted) identifier.
 * Identifiers are sequences of 1 or more letters.
 */
type ParseIdentifier<Input extends string> = ParseLetters<Input> extends [infer Name, `${infer Remainder}`] ? [Name, EatWhitespace<Remainder>] : ParseQuotedLetters<Input> extends [infer Name, `${infer Remainder}`] ? [Name, EatWhitespace<Remainder>] : ParserError<`No (possibly double-quoted) identifier at \`${Input}\``>;
/**
 * Parse a consecutive sequence of 1 or more letter, where letters are `[0-9a-zA-Z_]`.
 */
type ParseLetters<Input extends string> = string extends Input ? GenericStringError : ParseLettersHelper<Input, ''> extends [`${infer Letters}`, `${infer Remainder}`] ? Letters extends '' ? ParserError<`Expected letter at \`${Input}\``> : [Letters, Remainder] : ParseLettersHelper<Input, ''>;
type ParseLettersHelper<Input extends string, Acc extends string> = string extends Input ? GenericStringError : Input extends `${infer L}${infer Remainder}` ? L extends Token.Letter ? ParseLettersHelper<Remainder, `${Acc}${L}`> : [Acc, Input] : [Acc, ''];
/**
 * Parse a consecutive sequence of 1 or more double-quoted letters,
 * where letters are `[^"]`.
 */
type ParseQuotedLetters<Input extends string> = string extends Input ? GenericStringError : Input extends `"${infer Remainder}` ? ParseQuotedLettersHelper<Remainder, ''> extends [`${infer Letters}`, `${infer Remainder}`] ? Letters extends '' ? ParserError<`Expected string at \`${Remainder}\``> : [Letters, Remainder] : ParseQuotedLettersHelper<Remainder, ''> : ParserError<`Not a double-quoted string at \`${Input}\``>;
type ParseQuotedLettersHelper<Input extends string, Acc extends string> = string extends Input ? GenericStringError : Input extends `${infer L}${infer Remainder}` ? L extends '"' ? [Acc, Remainder] : ParseQuotedLettersHelper<Remainder, `${Acc}${L}`> : ParserError<`Missing closing double-quote in \`"${Acc}${Input}\``>;
/**
 * Trims whitespace from the left of the input.
 */
type EatWhitespace<Input extends string> = string extends Input ? GenericStringError : Input extends `${Token.Whitespace}${infer Remainder}` ? EatWhitespace<Remainder> : Input;
/**
 * Creates a new {@link ParserError} if the given input is not already a parser error.
 */
type CreateParserErrorIfRequired<Input, Message extends string> = Input extends ParserError<string> ? Input : ParserError<Message>;
/**
 * Parser errors.
 */
type ParserError<Message extends string> = {
  error: true;
} & Message;
type GenericStringError = ParserError<'Received a generic string'>;
declare namespace Ast {
  type Node = FieldNode | StarNode | SpreadNode;
  type FieldNode = {
    type: 'field';
    name: string;
    alias?: string;
    hint?: string;
    innerJoin?: true;
    castType?: string;
    jsonPath?: string;
    aggregateFunction?: Token.AggregateFunction;
    children?: Node[];
  };
  type StarNode = {
    type: 'star';
  };
  type SpreadNode = {
    type: 'spread';
    target: FieldNode & {
      children: Node[];
    };
  };
}
declare namespace Token {
  export type Whitespace = ' ' | '\n' | '\t';
  type LowerAlphabet = 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z';
  type Alphabet = LowerAlphabet | Uppercase<LowerAlphabet>;
  type Digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0';
  export type Letter = Alphabet | Digit | '_';
  export type AggregateFunction = 'count' | 'sum' | 'avg' | 'min' | 'max';
  export {};
}
//#endregion
//#region src/select-query-parser/utils.d.ts
type IsAny$1<T> = 0 extends 1 & T ? true : false;
type SelectQueryError<Message extends string> = {
  error: true;
} & Message;
type DeduplicateRelationships<T extends readonly unknown[]> = T extends readonly [infer First, ...infer Rest] ? First extends Rest[number] ? DeduplicateRelationships<Rest extends readonly unknown[] ? Rest : []> : [First, ...DeduplicateRelationships<Rest extends readonly unknown[] ? Rest : []>] : T;
type GetFieldNodeResultName<Field$1 extends Ast.FieldNode> = Field$1['alias'] extends string ? Field$1['alias'] : Field$1['aggregateFunction'] extends AggregateFunctions ? Field$1['aggregateFunction'] : Field$1['name'];
type FilterRelationNodes<Nodes$1 extends Ast.Node[]> = UnionToArray<{ [K in keyof Nodes$1]: Nodes$1[K] extends Ast.SpreadNode ? Nodes$1[K]['target'] : Nodes$1[K] extends Ast.FieldNode ? IsNonEmptyArray<Nodes$1[K]['children']> extends true ? Nodes$1[K] : never : never }[number]>;
type ResolveRelationships<Schema extends GenericSchema, RelationName extends string, Relationships extends GenericRelationship[], Nodes$1 extends Ast.FieldNode[]> = UnionToArray<{ [K in keyof Nodes$1]: Nodes$1[K] extends Ast.FieldNode ? ResolveRelationship<Schema, Relationships, Nodes$1[K], RelationName> extends infer Relation ? Relation extends {
  relation: {
    referencedRelation: string;
    foreignKeyName: string;
    match: string;
  };
  from: string;
} ? {
  referencedTable: Relation['relation']['referencedRelation'];
  fkName: Relation['relation']['foreignKeyName'];
  from: Relation['from'];
  match: Relation['relation']['match'];
  fieldName: GetFieldNodeResultName<Nodes$1[K]>;
} : Relation : never : never }>[0];
/**
 * Checks if a relation is implicitly referenced twice, requiring disambiguation
 */
type IsDoubleReference<T, U> = T extends {
  referencedTable: infer RT;
  fieldName: infer FN;
  match: infer M;
} ? M extends 'col' | 'refrel' ? U extends {
  referencedTable: RT;
  fieldName: FN;
  match: M;
} ? true : false : false : false;
/**
 * Compares one element with all other elements in the array to find duplicates
 */
type CheckDuplicates<Arr extends any[], Current> = Arr extends [infer Head, ...infer Tail] ? IsDoubleReference<Current, Head> extends true ? Head | CheckDuplicates<Tail, Current> : CheckDuplicates<Tail, Current> : never;
/**
 * Iterates over the elements of the array to find duplicates
 */
type FindDuplicatesWithinDeduplicated<Arr extends any[]> = Arr extends [infer Head, ...infer Tail] ? CheckDuplicates<Tail, Head> | FindDuplicatesWithinDeduplicated<Tail> : never;
type FindDuplicates<Arr extends any[]> = FindDuplicatesWithinDeduplicated<DeduplicateRelationships<Arr>>;
type CheckDuplicateEmbededReference<Schema extends GenericSchema, RelationName extends string, Relationships extends GenericRelationship[], Nodes$1 extends Ast.Node[]> = FilterRelationNodes<Nodes$1> extends infer RelationsNodes ? RelationsNodes extends Ast.FieldNode[] ? ResolveRelationships<Schema, RelationName, Relationships, RelationsNodes> extends infer ResolvedRels ? ResolvedRels extends unknown[] ? FindDuplicates<ResolvedRels> extends infer Duplicates ? Duplicates extends never ? false : Duplicates extends {
  fieldName: infer FieldName;
} ? FieldName extends string ? { [K in FieldName]: SelectQueryError<`table "${RelationName}" specified more than once use hinting for desambiguation`> } : false : false : false : false : false : false : false;
/**
 * Returns a boolean representing whether there is a foreign key referencing
 * a given relation.
 */
type HasFKeyToFRel<FRelName, Relationships> = Relationships extends [infer R] ? R extends {
  referencedRelation: FRelName;
} ? true : false : Relationships extends [infer R, ...infer Rest] ? HasFKeyToFRel<FRelName, [R]> extends true ? true : HasFKeyToFRel<FRelName, Rest> : false;
/**
 * Checks if there is more than one relation to a given foreign relation name in the Relationships.
 */
type HasMultipleFKeysToFRelDeduplicated<FRelName, Relationships> = Relationships extends [infer R, ...infer Rest] ? R extends {
  referencedRelation: FRelName;
} ? HasFKeyToFRel<FRelName, Rest> extends true ? true : HasMultipleFKeysToFRelDeduplicated<FRelName, Rest> : HasMultipleFKeysToFRelDeduplicated<FRelName, Rest> : false;
type HasMultipleFKeysToFRel<FRelName, Relationships extends unknown[]> = HasMultipleFKeysToFRelDeduplicated<FRelName, DeduplicateRelationships<Relationships>>;
type CheckRelationshipError<Schema extends GenericSchema, Relationships extends GenericRelationship[], CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string, FoundRelation$1> = FoundRelation$1 extends SelectQueryError<string> ? FoundRelation$1 : FoundRelation$1 extends {
  relation: {
    referencedRelation: infer RelatedRelationName;
    name: string;
  };
  direction: 'reverse';
} ? RelatedRelationName extends string ? HasMultipleFKeysToFRel<RelatedRelationName, Relationships> extends true ? FoundRelation$1 extends {
  relation: {
    match: 'col';
  };
} ? FoundRelation$1 : SelectQueryError<`Could not embed because more than one relationship was found for '${RelatedRelationName}' and '${CurrentTableOrView}' you need to hint the column with ${RelatedRelationName}!<columnName> ?`> : FoundRelation$1 : never : FoundRelation$1 extends {
  relation: {
    referencedRelation: infer RelatedRelationName;
    name: string;
  };
  direction: 'forward';
  from: infer From;
} ? RelatedRelationName extends string ? From extends keyof TablesAndViews$2<Schema> & string ? HasMultipleFKeysToFRel<RelatedRelationName, TablesAndViews$2<Schema>[From]['Relationships']> extends true ? SelectQueryError<`Could not embed because more than one relationship was found for '${From}' and '${RelatedRelationName}' you need to hint the column with ${From}!<columnName> ?`> : FoundRelation$1 : never : never : FoundRelation$1;
/**
 * Resolves relationships for embedded resources and retrieves the referenced Table
 */
type ResolveRelationship<Schema extends GenericSchema, Relationships extends GenericRelationship[], Field$1 extends Ast.FieldNode, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string> = ResolveReverseRelationship<Schema, Relationships, Field$1, CurrentTableOrView> extends infer ReverseRelationship ? ReverseRelationship extends false ? CheckRelationshipError<Schema, Relationships, CurrentTableOrView, ResolveForwardRelationship<Schema, Field$1, CurrentTableOrView>> : CheckRelationshipError<Schema, Relationships, CurrentTableOrView, ReverseRelationship> : never;
/**
 * Resolves reverse relationships (from children to parent)
 */
type ResolveReverseRelationship<Schema extends GenericSchema, Relationships extends GenericRelationship[], Field$1 extends Ast.FieldNode, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string> = FindFieldMatchingRelationships<Schema, Relationships, Field$1> extends infer FoundRelation ? FoundRelation extends never ? false : FoundRelation extends {
  referencedRelation: infer RelatedRelationName;
} ? RelatedRelationName extends string ? RelatedRelationName extends keyof TablesAndViews$2<Schema> ? FoundRelation extends {
  hint: string;
} | {
  match: 'col';
} ? {
  referencedTable: TablesAndViews$2<Schema>[RelatedRelationName];
  relation: FoundRelation;
  direction: 'reverse';
  from: CurrentTableOrView;
} : HasMultipleFKeysToFRel<RelatedRelationName, Relationships> extends true ? SelectQueryError<`Could not embed because more than one relationship was found for '${RelatedRelationName}' and '${CurrentTableOrView}' you need to hint the column with ${RelatedRelationName}!<columnName> ?`> : {
  referencedTable: TablesAndViews$2<Schema>[RelatedRelationName];
  relation: FoundRelation;
  direction: 'reverse';
  from: CurrentTableOrView;
} : SelectQueryError<`Relation '${RelatedRelationName}' not found in schema.`> : false : false : false;
type FindMatchingTableRelationships<Schema extends GenericSchema, Relationships extends GenericRelationship[], value extends string> = Relationships extends [infer R, ...infer Rest] ? Rest extends GenericRelationship[] ? R extends {
  referencedRelation: infer ReferencedRelation;
} ? ReferencedRelation extends keyof Schema['Tables'] ? R extends {
  foreignKeyName: value;
} ? R & {
  match: 'fkname';
} : R extends {
  referencedRelation: value;
} ? R & {
  match: 'refrel';
} : R extends {
  columns: [value];
} ? R & {
  match: 'col';
} : FindMatchingTableRelationships<Schema, Rest, value> : FindMatchingTableRelationships<Schema, Rest, value> : false : false : false;
type FindMatchingViewRelationships<Schema extends GenericSchema, Relationships extends GenericRelationship[], value extends string> = Relationships extends [infer R, ...infer Rest] ? Rest extends GenericRelationship[] ? R extends {
  referencedRelation: infer ReferencedRelation;
} ? ReferencedRelation extends keyof Schema['Views'] ? R extends {
  foreignKeyName: value;
} ? R & {
  match: 'fkname';
} : R extends {
  referencedRelation: value;
} ? R & {
  match: 'refrel';
} : R extends {
  columns: [value];
} ? R & {
  match: 'col';
} : FindMatchingViewRelationships<Schema, Rest, value> : FindMatchingViewRelationships<Schema, Rest, value> : false : false : false;
type FindMatchingHintTableRelationships<Schema extends GenericSchema, Relationships extends GenericRelationship[], hint extends string, name extends string> = Relationships extends [infer R, ...infer Rest] ? Rest extends GenericRelationship[] ? R extends {
  referencedRelation: infer ReferencedRelation;
} ? ReferencedRelation extends name ? R extends {
  foreignKeyName: hint;
} ? R & {
  match: 'fkname';
} : R extends {
  referencedRelation: hint;
} ? R & {
  match: 'refrel';
} : R extends {
  columns: [hint];
} ? R & {
  match: 'col';
} : FindMatchingHintTableRelationships<Schema, Rest, hint, name> : FindMatchingHintTableRelationships<Schema, Rest, hint, name> : false : false : false;
type FindMatchingHintViewRelationships<Schema extends GenericSchema, Relationships extends GenericRelationship[], hint extends string, name extends string> = Relationships extends [infer R, ...infer Rest] ? Rest extends GenericRelationship[] ? R extends {
  referencedRelation: infer ReferencedRelation;
} ? ReferencedRelation extends name ? R extends {
  foreignKeyName: hint;
} ? R & {
  match: 'fkname';
} : R extends {
  referencedRelation: hint;
} ? R & {
  match: 'refrel';
} : R extends {
  columns: [hint];
} ? R & {
  match: 'col';
} : FindMatchingHintViewRelationships<Schema, Rest, hint, name> : FindMatchingHintViewRelationships<Schema, Rest, hint, name> : false : false : false;
type IsColumnsNullable<Table extends Pick<GenericTable, 'Row'>, Columns extends (keyof Table['Row'])[]> = Columns extends [infer Column, ...infer Rest] ? Column extends keyof Table['Row'] ? ContainsNull<Table['Row'][Column]> extends true ? true : IsColumnsNullable<Table, Rest extends (keyof Table['Row'])[] ? Rest : []> : false : false;
type IsRelationNullable<Table extends GenericTable, Relation$1 extends GenericRelationship> = IsColumnsNullable<Table, Relation$1['columns']>;
type TableForwardRelationships<Schema extends GenericSchema, TName> = TName extends keyof TablesAndViews$2<Schema> ? UnionToArray<RecursivelyFindRelationships<Schema, TName, keyof TablesAndViews$2<Schema>>> extends infer R ? R extends (GenericRelationship & {
  from: keyof TablesAndViews$2<Schema>;
})[] ? R : [] : [] : [];
type RecursivelyFindRelationships<Schema extends GenericSchema, TName, Keys extends keyof TablesAndViews$2<Schema>> = Keys extends infer K ? K extends keyof TablesAndViews$2<Schema> ? FilterRelationships<TablesAndViews$2<Schema>[K]['Relationships'], TName, K> extends never ? RecursivelyFindRelationships<Schema, TName, Exclude<Keys, K>> : FilterRelationships<TablesAndViews$2<Schema>[K]['Relationships'], TName, K> | RecursivelyFindRelationships<Schema, TName, Exclude<Keys, K>> : false : false;
type FilterRelationships<R$1, TName, From$1> = R$1 extends readonly (infer Rel)[] ? Rel extends {
  referencedRelation: TName;
} ? Rel & {
  from: From$1;
} : never : never;
type ResolveForwardRelationship<Schema extends GenericSchema, Field$1 extends Ast.FieldNode, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string> = FindFieldMatchingRelationships<Schema, TablesAndViews$2<Schema>[Field$1['name']]['Relationships'], Ast.FieldNode & {
  name: CurrentTableOrView;
  hint: Field$1['hint'];
}> extends infer FoundByName ? FoundByName extends GenericRelationship ? {
  referencedTable: TablesAndViews$2<Schema>[Field$1['name']];
  relation: FoundByName;
  direction: 'forward';
  from: Field$1['name'];
  type: 'found-by-name';
} : FindFieldMatchingRelationships<Schema, TableForwardRelationships<Schema, CurrentTableOrView>, Field$1> extends infer FoundByMatch ? FoundByMatch extends GenericRelationship & {
  from: keyof TablesAndViews$2<Schema>;
} ? {
  referencedTable: TablesAndViews$2<Schema>[FoundByMatch['from']];
  relation: FoundByMatch;
  direction: 'forward';
  from: CurrentTableOrView;
  type: 'found-by-match';
} : FindJoinTableRelationship<Schema, CurrentTableOrView, Field$1['name']> extends infer FoundByJoinTable ? FoundByJoinTable extends GenericRelationship ? {
  referencedTable: TablesAndViews$2<Schema>[FoundByJoinTable['referencedRelation']];
  relation: FoundByJoinTable & {
    match: 'refrel';
  };
  direction: 'forward';
  from: CurrentTableOrView;
  type: 'found-by-join-table';
} : ResolveEmbededFunctionJoinTableRelationship<Schema, CurrentTableOrView, Field$1['name']> extends infer FoundEmbededFunctionJoinTableRelation ? FoundEmbededFunctionJoinTableRelation extends GenericFunction ? FoundEmbededFunctionJoinTableRelation['SetofOptions'] extends GenericSetofOption ? FoundEmbededFunctionJoinTableRelation['SetofOptions']['to'] extends '' ? {
  referencedTable: {
    Row: Record<string, never>;
    Relationships: [];
  };
  relation: {
    foreignKeyName: `${Field$1['name']}_${CurrentTableOrView}_scalar_forward`;
    columns: [];
    isOneToOne: false;
    referencedColumns: [];
    referencedRelation: '';
  } & {
    match: 'func';
    isNotNullable: FoundEmbededFunctionJoinTableRelation['SetofOptions']['isNotNullable'] extends true ? true : FoundEmbededFunctionJoinTableRelation['SetofOptions']['isSetofReturn'] extends true ? false : true;
    isSetofReturn: FoundEmbededFunctionJoinTableRelation['SetofOptions']['isSetofReturn'];
  };
  scalarType: FoundEmbededFunctionJoinTableRelation['Returns'];
  direction: 'forward';
  from: CurrentTableOrView;
  type: 'found-by-embeded-scalar-function';
} : {
  referencedTable: TablesAndViews$2<Schema>[FoundEmbededFunctionJoinTableRelation['SetofOptions']['to']];
  relation: {
    foreignKeyName: `${Field$1['name']}_${CurrentTableOrView}_${FoundEmbededFunctionJoinTableRelation['SetofOptions']['to']}_forward`;
    columns: [];
    isOneToOne: FoundEmbededFunctionJoinTableRelation['SetofOptions']['isOneToOne'] extends true ? true : false;
    referencedColumns: [];
    referencedRelation: FoundEmbededFunctionJoinTableRelation['SetofOptions']['to'];
  } & {
    match: 'func';
    isNotNullable: FoundEmbededFunctionJoinTableRelation['SetofOptions']['isNotNullable'] extends true ? true : FoundEmbededFunctionJoinTableRelation['SetofOptions']['isSetofReturn'] extends true ? false : true;
    isSetofReturn: FoundEmbededFunctionJoinTableRelation['SetofOptions']['isSetofReturn'];
  };
  direction: 'forward';
  from: CurrentTableOrView;
  type: 'found-by-embeded-function';
} : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`> : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`> : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`> : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`> : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`> : SelectQueryError<`could not find the relation between ${CurrentTableOrView} and ${Field$1['name']}`>;
/**
 * Given a CurrentTableOrView, finds all join tables to this relation.
 * For example, if products and categories are linked via product_categories table:
 *
 * @example Find join table relationship
 * Given:
 * - CurrentTableView = 'products'
 * - FieldName = "categories"
 *
 * It should return this relationship from product_categories:
 * {
 *   foreignKeyName: "product_categories_category_id_fkey",
 *   columns: ["category_id"],
 *   isOneToOne: false,
 *   referencedRelation: "categories",
 *   referencedColumns: ["id"]
 * }
 */
type ResolveJoinTableRelationship<Schema extends GenericSchema, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string, FieldName$1 extends string> = { [TableName in keyof TablesAndViews$2<Schema>]: DeduplicateRelationships<TablesAndViews$2<Schema>[TableName]['Relationships']> extends readonly (infer Rel)[] ? Rel extends {
  referencedRelation: CurrentTableOrView;
} ? DeduplicateRelationships<TablesAndViews$2<Schema>[TableName]['Relationships']> extends readonly (infer OtherRel)[] ? OtherRel extends {
  referencedRelation: FieldName$1;
} ? OtherRel : never : never : never : never }[keyof TablesAndViews$2<Schema>];
type ResolveEmbededFunctionJoinTableRelationship<Schema extends GenericSchema, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string, FieldName$1 extends string> = FindMatchingFunctionBySetofFrom<Schema['Functions'][FieldName$1], CurrentTableOrView> extends infer Fn ? Fn extends GenericFunction ? Fn : false : false;
type FindJoinTableRelationship<Schema extends GenericSchema, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string, FieldName$1 extends string> = ResolveJoinTableRelationship<Schema, CurrentTableOrView, FieldName$1> extends infer Result ? [Result] extends [never] ? false : Result : never;
/**
 * Finds a matching relationship based on the FieldNode's name and optional hint.
 */
type FindFieldMatchingRelationships<Schema extends GenericSchema, Relationships extends GenericRelationship[], Field$1 extends Ast.FieldNode> = Field$1 extends {
  hint: string;
} ? FindMatchingHintTableRelationships<Schema, Relationships, Field$1['hint'], Field$1['name']> extends GenericRelationship ? FindMatchingHintTableRelationships<Schema, Relationships, Field$1['hint'], Field$1['name']> & {
  branch: 'found-in-table-via-hint';
  hint: Field$1['hint'];
} : FindMatchingHintViewRelationships<Schema, Relationships, Field$1['hint'], Field$1['name']> extends GenericRelationship ? FindMatchingHintViewRelationships<Schema, Relationships, Field$1['hint'], Field$1['name']> & {
  branch: 'found-in-view-via-hint';
  hint: Field$1['hint'];
} : SelectQueryError<'Failed to find matching relation via hint'> : FindMatchingTableRelationships<Schema, Relationships, Field$1['name']> extends GenericRelationship ? FindMatchingTableRelationships<Schema, Relationships, Field$1['name']> & {
  branch: 'found-in-table-via-name';
  name: Field$1['name'];
} : FindMatchingViewRelationships<Schema, Relationships, Field$1['name']> extends GenericRelationship ? FindMatchingViewRelationships<Schema, Relationships, Field$1['name']> & {
  branch: 'found-in-view-via-name';
  name: Field$1['name'];
} : SelectQueryError<'Failed to find matching relation via name'>;
type JsonPathToAccessor<Path extends string> = Path extends `${infer P1}->${infer P2}` ? P2 extends `>${infer Rest}` ? JsonPathToAccessor<`${P1}.${Rest}`> : P2 extends string ? JsonPathToAccessor<`${P1}.${P2}`> : Path : Path extends `>${infer Rest}` ? JsonPathToAccessor<Rest> : Path extends `${infer P1}::${infer _}` ? JsonPathToAccessor<P1> : Path extends `${infer P1}${')' | ','}${infer _}` ? P1 : Path;
type JsonPathToType<T, Path extends string> = Path extends '' ? T : ContainsNull<T> extends true ? JsonPathToType<Exclude<T, null>, Path> : Path extends `${infer Key}.${infer Rest}` ? Key extends keyof T ? JsonPathToType<T[Key], Rest> : never : Path extends keyof T ? T[Path] : never;
type IsStringUnion<T> = string extends T ? false : T extends string ? [T] extends [never] ? false : true : false;
type MatchingFunctionBySetofFrom<Fn$1 extends GenericFunction, TableName$1 extends string> = Fn$1['SetofOptions'] extends GenericSetofOption ? TableName$1 extends Fn$1['SetofOptions']['from'] ? Fn$1 : never : false;
type FindMatchingFunctionBySetofFrom<FnUnion, TableName$1 extends string> = FnUnion extends infer Fn extends GenericFunction ? MatchingFunctionBySetofFrom<Fn, TableName$1> : false;
type ComputedField<Schema extends GenericSchema, RelationName extends keyof TablesAndViews$2<Schema>, FieldName$1 extends keyof TablesAndViews$2<Schema>[RelationName]['Row']> = FieldName$1 extends keyof Schema['Functions'] ? [Schema['Functions'][FieldName$1]['Args']] extends [never] ? never : Schema['Functions'][FieldName$1] extends {
  Args: {
    '': TablesAndViews$2<Schema>[RelationName]['Row'];
  };
  Returns: any;
} ? FieldName$1 : never : never;
type GetComputedFields<Schema extends GenericSchema, RelationName extends keyof TablesAndViews$2<Schema>> = { [K in keyof TablesAndViews$2<Schema>[RelationName]['Row']]: ComputedField<Schema, RelationName, K> }[keyof TablesAndViews$2<Schema>[RelationName]['Row']];
//#endregion
//#region src/types/types.d.ts
/**
 * Response format
 *
 * {@link https://github.com/supabase/supabase-js/issues/32}
 */
interface PostgrestResponseBase {
  /** HTTP status code of the response. */
  status: number;
  /**
   * HTTP reason phrase of the response, e.g. `"OK"`.
   *
   * May be an empty string: HTTP/2 and HTTP/3 don't carry reason phrases, so
   * responses over those protocols (e.g. browser requests to Supabase) have no
   * `statusText`. Rely on `status` instead of this value.
   */
  statusText: string;
}
interface PostgrestResponseSuccess<T> extends PostgrestResponseBase {
  success: true;
  error: null;
  data: T;
  count: number | null;
}
interface PostgrestResponseFailure extends PostgrestResponseBase {
  success: false;
  error: PostgrestError;
  data: null;
  count: null;
}
type PostgrestSingleResponse<T> = PostgrestResponseSuccess<T> | PostgrestResponseFailure;
type PostgrestMaybeSingleResponse<T> = PostgrestSingleResponse<T | null>;
type PostgrestResponse<T> = PostgrestSingleResponse<T[]>;
/**
 * OpenAPI description served by PostgREST at the REST root (`GET /`).
 *
 * PostgREST emits OpenAPI 2.0 (Swagger), so the version lives in `swagger`.
 * OpenAPI 2.0 requires only `swagger`, `info` and `paths`; a PostgREST
 * `db-root-spec` override may leave out any other field. Only the top level
 * is typed here; the contents of `paths`, `definitions` and `parameters`
 * follow the OpenAPI 2.0 specification and vary with the PostgREST version.
 *
 * {@link https://docs.postgrest.org/en/stable/references/api/openapi.html}
 */
interface PostgrestOpenApiSpec {
  swagger: string;
  info: Record<string, unknown>;
  host?: string;
  basePath?: string;
  paths: Record<string, Record<string, unknown>>;
  definitions?: Record<string, Record<string, unknown>>;
  parameters?: Record<string, Record<string, unknown>>;
  [key: string]: unknown;
}
type Prettify<T> = { [K in keyof T]: T[K] } & {};
type RejectExcessProperties<Base, Row> = Row & { [K in Exclude<keyof Row, keyof Base>]: never };
type SimplifyDeep<Type, ExcludeType = never> = ConditionalSimplifyDeep<Type, ExcludeType | NonRecursiveType | Set<unknown> | Map<unknown, unknown>, object>;
type ConditionalSimplifyDeep<Type, ExcludeType = never, IncludeType = unknown> = Type extends ExcludeType ? Type : Type extends IncludeType ? { [TypeKey in keyof Type]: ConditionalSimplifyDeep<Type[TypeKey], ExcludeType, IncludeType> } : Type;
type NonRecursiveType = BuiltIns | Function | (new (...arguments_: any[]) => unknown);
type BuiltIns = Primitive | void | Date | RegExp;
type Primitive = null | undefined | string | number | boolean | symbol | bigint;
type IsValidResultOverride<Result$1, NewResult, ErrorResult, ErrorNewResult> = Result$1 extends any[] ? NewResult extends any[] ? true : ErrorResult : NewResult extends any[] ? ErrorNewResult : true;
/**
 * Utility type to check if array types match between Result and NewResult.
 * Returns either the valid NewResult type or an error message type.
 */
type CheckMatchingArrayTypes<Result$1, NewResult> = Result$1 extends SelectQueryError<string> ? NewResult : IsValidResultOverride<Result$1, NewResult, {
  Error: 'Type mismatch: Cannot cast array result to a single object. Use .overrideTypes<Array<YourType>> or .returns<Array<YourType>> (deprecated) for array results or .single() to convert the result to a single object';
}, {
  Error: 'Type mismatch: Cannot cast single object to array type. Remove Array wrapper from return type or make sure you are not using .single() up in the calling chain';
}> extends infer ValidationResult ? ValidationResult extends true ? ContainsNull<Result$1> extends true ? NewResult | null : NewResult : ValidationResult : never;
type Simplify<T> = T extends object ? { [K in keyof T]: T[K] } : T;
type ExplicitKeys<T> = { [K in keyof T]: string extends K ? never : K }[keyof T];
type MergeExplicit<New, Row> = { [K in ExplicitKeys<New> | ExplicitKeys<Row>]: K extends keyof New ? K extends keyof Row ? Row[K] extends SelectQueryError<string> ? New[K] : New[K] extends any[] ? Row[K] extends any[] ? Array<Simplify<MergeDeep<NonNullable<New[K][number]>, NonNullable<Row[K][number]>>>> : New[K] : IsPlainObject<NonNullable<New[K]>> extends true ? IsPlainObject<NonNullable<Row[K]>> extends true ? ContainsNull<New[K]> extends true ?
// If the override wants to preserve optionality
Simplify<MergeDeep<NonNullable<New[K]>, NonNullable<Row[K]>>> | null : Simplify<MergeDeep<New[K], NonNullable<Row[K]>>> : New[K] : New[K] : New[K] : K extends keyof Row ? Row[K] : never };
type MergeDeep<New, Row> = Simplify<MergeExplicit<New, Row> & (string extends keyof Row ? {
  [K: string]: Row[string];
} : {})>;
type IsPlainObject<T> = T extends any[] ? false : T extends object ? true : false;
type MergePartialResult<NewResult, Result$1, Options> = Options extends {
  merge: true;
} ? Result$1 extends any[] ? NewResult extends any[] ? Array<Simplify<MergeDeep<NewResult[number], Result$1[number]>>> : never : Simplify<MergeDeep<NewResult, Result$1>> : NewResult;
//#endregion
//#region src/PostgrestBuilder.d.ts
declare abstract class PostgrestBuilder<ClientOptions extends ClientServerOptions, Result$1, ThrowOnError extends boolean = false> implements PromiseLike<ThrowOnError extends true ? PostgrestResponseSuccess<Result$1> : PostgrestSingleResponse<Result$1>> {
  protected method: 'GET' | 'HEAD' | 'POST' | 'PATCH' | 'DELETE';
  protected url: URL;
  protected headers: Headers;
  protected schema?: string;
  protected body?: unknown;
  protected shouldThrowOnError: boolean;
  protected signal?: AbortSignal;
  protected fetch: Fetch;
  protected isMaybeSingle: boolean;
  protected shouldStripNulls: boolean;
  protected urlLengthLimit: number;
  protected retryEnabled: boolean;
  /**
   * Creates a builder configured for a specific PostgREST request.
   *
   * @example Using supabase-js (recommended)
   * ```ts
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const { data, error } = await supabase.from('users').select('*')
   * ```
   *
   * @category Database
   *
   * @example Standalone import for bundle-sensitive environments
   * ```ts
   * import { PostgrestQueryBuilder } from '@supabase/postgrest-js'
   *
   * const builder = new PostgrestQueryBuilder(
   *   new URL('https://xyzcompany.supabase.co/rest/v1/users'),
   *   { headers: new Headers({ apikey: 'your-publishable-key' }) }
   * )
   * ```
   */
  constructor(builder: {
    method: 'GET' | 'HEAD' | 'POST' | 'PATCH' | 'DELETE';
    url: URL;
    headers: HeadersInit;
    schema?: string;
    body?: unknown;
    shouldThrowOnError?: boolean;
    signal?: AbortSignal;
    fetch?: Fetch;
    isMaybeSingle?: boolean;
    shouldStripNulls?: boolean;
    urlLengthLimit?: number;
    retry?: boolean;
  });
  /**
   * If there's an error with the query, throwOnError will reject the promise by
   * throwing the error instead of returning it as part of a successful response.
   *
   * {@link https://github.com/supabase/supabase-js/issues/92}
   *
   * @category Database
   * @subcategory Using modifiers
   */
  throwOnError(): PostgrestBuilder<ClientOptions, Result$1, true>;
  /**
   * Strip null values from the response data. Properties with `null` values
   * will be omitted from the returned JSON objects.
   *
   * Requires PostgREST 11.2.0+.
   *
   * {@link https://docs.postgrest.org/en/stable/references/api/resource_representation.html#stripped-nulls}
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .stripNulls()
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text, bio text);
   *
   * insert into
   *   characters (id, name, bio)
   * values
   *   (1, 'Luke', null),
   *   (2, 'Leia', 'Princess of Alderaan');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     },
   *     {
   *       "id": 2,
   *       "name": "Leia",
   *       "bio": "Princess of Alderaan"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  stripNulls(): this;
  /**
   * Set an HTTP header on this single PostgREST request, overriding any header
   * with the same name set on the client.
   *
   * This is an advanced escape hatch for one-off needs (passing a custom
   * `Authorization` for a single query, attaching a tracing header, etc.).
   * Most callers do not need it: configure client-wide headers via the
   * `headers` option when constructing the client, and authentication via
   * Supabase Auth.
   *
   * @param name - HTTP header name
   * @param value - HTTP header value
   *
   * @category Database
   * @subcategory Using modifiers
   */
  setHeader(name: string, value: string): this;
  /**
   * @category Database
   * @subcategory Using modifiers
   *
   * Configure retry behavior for this request.
   *
   * By default, retries are enabled for idempotent requests (GET, HEAD, OPTIONS)
   * that fail with network errors or specific HTTP status codes (503, 520).
   * Retries use exponential backoff (1s, 2s, 4s) with a maximum of 3 attempts.
   *
   * @param enabled - Whether to enable retries for this request
   *
   * @example
   * ```ts
   * // Disable retries for a specific query
   * const { data, error } = await supabase
   *   .from('users')
   *   .select()
   *   .retry(false)
   * ```
   */
  retry(enabled: boolean): this;
  then<TResult1 = (ThrowOnError extends true ? PostgrestResponseSuccess<Result$1> : PostgrestSingleResponse<Result$1>), TResult2 = never>(onfulfilled?: ((value: ThrowOnError extends true ? PostgrestResponseSuccess<Result$1> : PostgrestSingleResponse<Result$1>) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): PromiseLike<TResult1 | TResult2>;
  /**
   * Process a fetch response and return the standardized postgrest response.
   */
  private processResponse;
  /**
   * Override the type of the returned `data`.
   *
   * @typeParam NewResult - The new result type to override with
   * @deprecated Use overrideTypes<yourType, { merge: false }>() method at the end of your call chain instead
   *
   * @category Database
   * @subcategory Using modifiers
   */
  returns<NewResult>(): PostgrestBuilder<ClientOptions, CheckMatchingArrayTypes<Result$1, NewResult>, ThrowOnError>;
  /**
   * Override the type of the returned `data` field in the response.
   *
   * @typeParam NewResult - The new type to cast the response data to
   * @typeParam Options - Optional type configuration (defaults to { merge: true })
   * @typeParam Options.merge - When true, merges the new type with existing return type. When false, replaces the existing types entirely (defaults to true)
   * @example
   * ```typescript
   * // Merge with existing types (default behavior)
   * const query = supabase
   *   .from('users')
   *   .select()
   *   .overrideTypes<{ custom_field: string }>()
   *
   * // Replace existing types completely
   * const replaceQuery = supabase
   *   .from('users')
   *   .select()
   *   .overrideTypes<{ id: number; name: string }, { merge: false }>()
   * ```
   * @returns A PostgrestBuilder instance with the new type
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example Complete Override type of successful response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .overrideTypes<Array<MyType>, { merge: false }>()
   * ```
   *
   * @exampleResponse Complete Override type of successful response
   * ```ts
   * let x: typeof data // MyType[]
   * ```
   *
   * @example Complete Override type of object response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .maybeSingle()
   *   .overrideTypes<MyType, { merge: false }>()
   * ```
   *
   * @exampleResponse Complete Override type of object response
   * ```ts
   * let x: typeof data // MyType | null
   * ```
   *
   * @example Partial Override type of successful response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .overrideTypes<Array<{ status: "A" | "B" }>>()
   * ```
   *
   * @exampleResponse Partial Override type of successful response
   * ```ts
   * let x: typeof data // Array<CountryRowProperties & { status: "A" | "B" }>
   * ```
   *
   * @example Partial Override type of object response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .maybeSingle()
   *   .overrideTypes<{ status: "A" | "B" }>()
   * ```
   *
   * @exampleResponse Partial Override type of object response
   * ```ts
   * let x: typeof data // CountryRowProperties & { status: "A" | "B" } | null
   * ```
   *
   * @example Merge vs replace existing types
   * ```typescript
   * // Merge with existing types (default behavior)
   * const query = supabase
   *   .from('users')
   *   .select()
   *   .overrideTypes<{ custom_field: string }>()
   *
   * // Replace existing types completely
   * const replaceQuery = supabase
   *   .from('users')
   *   .select()
   *   .overrideTypes<{ id: number; name: string }, { merge: false }>()
   * ```
   */
  overrideTypes<NewResult, Options extends {
    merge?: boolean;
  } = {
    merge: true;
  }>(): PostgrestBuilder<ClientOptions, IsValidResultOverride<Result$1, NewResult, false, false> extends true ? ContainsNull<Result$1> extends true ? MergePartialResult<NewResult, NonNullable<Result$1>, Options> | null : MergePartialResult<NewResult, Result$1, Options> : CheckMatchingArrayTypes<Result$1, NewResult>, ThrowOnError>;
}
//#endregion
//#region src/types/feature-flags.d.ts
type IsPostgrest13<PostgrestVersion extends string | undefined> = PostgrestVersion extends `13${string}` ? true : false;
type IsPostgrest14<PostgrestVersion extends string | undefined> = PostgrestVersion extends `14${string}` ? true : false;
type IsPostgrestVersionGreaterThan12<PostgrestVersion extends string | undefined> = IsPostgrest13<PostgrestVersion> extends true ? true : IsPostgrest14<PostgrestVersion> extends true ? true : false;
type MaxAffectedEnabled<PostgrestVersion extends string | undefined> = IsPostgrestVersionGreaterThan12<PostgrestVersion> extends true ? true : false;
type SpreadOnManyEnabled<PostgrestVersion extends string | undefined> = IsPostgrestVersionGreaterThan12<PostgrestVersion> extends true ? true : false;
//#endregion
//#region src/select-query-parser/result.d.ts
/**
 * Main entry point for constructing the result type of a PostgREST query.
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param Query - The select query string literal to parse.
 */
type GetResult<Schema extends GenericSchema, Row extends Record<string, unknown>, RelationName, Relationships, Query extends string, ClientOptions extends ClientServerOptions> = IsAny$1<Schema> extends true ? ParseQuery<Query> extends infer ParsedQuery ? ParsedQuery extends Ast.Node[] ? RelationName extends string ? ProcessNodesWithoutSchema<ParsedQuery> : any : ParsedQuery : any : Relationships extends null ? ParseQuery<Query> extends infer ParsedQuery ? ParsedQuery extends Ast.Node[] ? RPCCallNodes<ParsedQuery, RelationName extends string ? RelationName : 'rpc_call', Row> : ParsedQuery : Row : ParseQuery<Query> extends infer ParsedQuery ? ParsedQuery extends Ast.Node[] ? RelationName extends string ? Relationships extends GenericRelationship[] ? ProcessNodes<ClientOptions, Schema, Row, RelationName, Relationships, ParsedQuery> : SelectQueryError<'Invalid Relationships cannot infer result type'> : SelectQueryError<'Invalid RelationName cannot infer result type'> : ParsedQuery : never;
type ProcessSimpleFieldWithoutSchema<Field$1 extends Ast.FieldNode> = Field$1['aggregateFunction'] extends AggregateFunctions ? { [K in GetFieldNodeResultName<Field$1>]: Field$1['castType'] extends PostgreSQLTypes ? TypeScriptTypes<Field$1['castType']> : number } : { [K in GetFieldNodeResultName<Field$1>]: Field$1['castType'] extends PostgreSQLTypes ? TypeScriptTypes<Field$1['castType']> : any };
type ProcessFieldNodeWithoutSchema<Node$1 extends Ast.FieldNode> = IsNonEmptyArray<Node$1['children']> extends true ? { [K in GetFieldNodeResultName<Node$1>]: Node$1['children'] extends Ast.Node[] ? ProcessNodesWithoutSchema<Node$1['children']>[] : ProcessSimpleFieldWithoutSchema<Node$1> } : ProcessSimpleFieldWithoutSchema<Node$1>;
/**
 * Processes a single Node without schema and returns the resulting TypeScript type.
 */
type ProcessNodeWithoutSchema<Node$1 extends Ast.Node> = Node$1 extends Ast.StarNode ? any : Node$1 extends Ast.SpreadNode ? Node$1['target']['children'] extends Ast.StarNode[] ? any : Node$1['target']['children'] extends Ast.FieldNode[] ? { [P in Node$1['target']['children'][number] as GetFieldNodeResultName<P>]: P['castType'] extends PostgreSQLTypes ? TypeScriptTypes<P['castType']> : any } : any : Node$1 extends Ast.FieldNode ? ProcessFieldNodeWithoutSchema<Node$1> : any;
/**
 * Processes nodes when Schema is any, providing basic type inference
 */
type ProcessNodesWithoutSchema<Nodes$1 extends Ast.Node[], Acc extends Record<string, unknown> = {}> = Nodes$1 extends [infer FirstNode, ...infer RestNodes] ? FirstNode extends Ast.Node ? RestNodes extends Ast.Node[] ? ProcessNodeWithoutSchema<FirstNode> extends infer FieldResult ? FieldResult extends Record<string, unknown> ? ProcessNodesWithoutSchema<RestNodes, Acc & FieldResult> : FieldResult : any : any : any : Prettify<Acc>;
/**
 * Processes a single Node from a select chained after a rpc call
 *
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current rpc function
 * @param NodeType - The Node to process.
 */
type ProcessRPCNode<Row extends Record<string, unknown>, RelationName extends string, NodeType extends Ast.Node> = NodeType['type'] extends Ast.StarNode['type'] ? Row : NodeType['type'] extends Ast.FieldNode['type'] ? ProcessSimpleField<Row, RelationName, Extract<NodeType, Ast.FieldNode>> : SelectQueryError<'RPC Unsupported node type.'>;
/**
 * Process select call that can be chained after an rpc call
 */
type RPCCallNodes<Nodes$1 extends Ast.Node[], RelationName extends string, Row extends Record<string, unknown>, Acc extends Record<string, unknown> = {}> = Nodes$1 extends [infer FirstNode, ...infer RestNodes] ? FirstNode extends Ast.Node ? RestNodes extends Ast.Node[] ? ProcessRPCNode<Row, RelationName, FirstNode> extends infer FieldResult ? FieldResult extends Record<string, unknown> ? RPCCallNodes<RestNodes, RelationName, Row, Acc & FieldResult> : FieldResult extends SelectQueryError<infer E> ? SelectQueryError<E> : SelectQueryError<'Could not retrieve a valid record or error value'> : SelectQueryError<'Processing node failed.'> : SelectQueryError<'Invalid rest nodes array in RPC call'> : SelectQueryError<'Invalid first node in RPC call'> : Prettify<Acc>;
/**
 * Recursively processes an array of Nodes and accumulates the resulting TypeScript type.
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param Nodes - An array of AST nodes to process.
 * @param Acc - Accumulator for the constructed type.
 */
type ProcessNodes<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, RelationName extends string, Relationships extends GenericRelationship[], Nodes$1 extends Ast.Node[], Acc extends Record<string, unknown> = {}> = CheckDuplicateEmbededReference<Schema, RelationName, Relationships, Nodes$1> extends false ? Nodes$1 extends [infer FirstNode, ...infer RestNodes] ? FirstNode extends Ast.Node ? RestNodes extends Ast.Node[] ? ProcessNode<ClientOptions, Schema, Row, RelationName, Relationships, FirstNode> extends infer FieldResult ? FieldResult extends Record<string, unknown> ? ProcessNodes<ClientOptions, Schema, Row, RelationName, Relationships, RestNodes, Acc & FieldResult> : FieldResult extends SelectQueryError<infer E> ? SelectQueryError<E> : SelectQueryError<'Could not retrieve a valid record or error value'> : SelectQueryError<'Processing node failed.'> : SelectQueryError<'Invalid rest nodes array type in ProcessNodes'> : SelectQueryError<'Invalid first node type in ProcessNodes'> : Prettify<Acc> : Prettify<CheckDuplicateEmbededReference<Schema, RelationName, Relationships, Nodes$1>>;
/**
 * Processes a single Node and returns the resulting TypeScript type.
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param NodeType - The Node to process.
 */
type ProcessNode<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, RelationName extends string, Relationships extends GenericRelationship[], NodeType extends Ast.Node> = NodeType['type'] extends Ast.StarNode['type'] ? GetComputedFields<Schema, RelationName> extends never ? Row : Omit<Row, GetComputedFields<Schema, RelationName>> : NodeType['type'] extends Ast.SpreadNode['type'] ? ProcessSpreadNode<ClientOptions, Schema, Row, RelationName, Relationships, Extract<NodeType, Ast.SpreadNode>> : NodeType['type'] extends Ast.FieldNode['type'] ? ProcessFieldNode<ClientOptions, Schema, Row, RelationName, Relationships, Extract<NodeType, Ast.FieldNode>> : SelectQueryError<'Unsupported node type.'>;
/**
 * Processes a FieldNode and returns the resulting TypeScript type.
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param Field - The FieldNode to process.
 */
type ProcessFieldNode<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, RelationName extends string, Relationships extends GenericRelationship[], Field$1 extends Ast.FieldNode> = Field$1['children'] extends [] ? ProcessEmbeddedResource<ClientOptions, Schema, Relationships, Field$1, RelationName> : IsNonEmptyArray<Field$1['children']> extends true ? ProcessEmbeddedResource<ClientOptions, Schema, Relationships, Field$1, RelationName> : ProcessSimpleField<Row, RelationName, Field$1>;
type ResolveJsonPathType<Value, Path extends string | undefined, CastType$1 extends PostgreSQLTypes> = Path extends string ? JsonPathToType<Value, Path> extends never ? TypeScriptTypes<CastType$1> : JsonPathToType<Value, Path> extends infer PathResult ? PathResult extends string ? PathResult : IsStringUnion<PathResult> extends true ? PathResult : CastType$1 extends 'json' ? PathResult : TypeScriptTypes<CastType$1> : TypeScriptTypes<CastType$1> : TypeScriptTypes<CastType$1>;
/**
 * Processes a simple field (without embedded resources).
 *
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Field - The FieldNode to process.
 */
type ProcessSimpleField<Row extends Record<string, unknown>, RelationName extends string, Field$1 extends Ast.FieldNode> = Field$1['name'] extends keyof Row | 'count' ? Field$1['aggregateFunction'] extends AggregateFunctions ? { [K in GetFieldNodeResultName<Field$1>]: Field$1['castType'] extends PostgreSQLTypes ? TypeScriptTypes<Field$1['castType']> : number } : { [K in GetFieldNodeResultName<Field$1>]: Field$1['castType'] extends PostgreSQLTypes ? ResolveJsonPathType<Row[Field$1['name']], Field$1['jsonPath'], Field$1['castType']> : Row[Field$1['name']] } : SelectQueryError<`column '${Field$1['name']}' does not exist on '${RelationName}'.`>;
/**
 * Processes an embedded resource (relation).
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param Field - The FieldNode to process.
 */
type ProcessEmbeddedResource<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Relationships extends GenericRelationship[], Field$1 extends Ast.FieldNode, CurrentTableOrView extends keyof TablesAndViews$2<Schema> & string> = ResolveRelationship<Schema, Relationships, Field$1, CurrentTableOrView> extends infer Resolved ? Resolved extends {
  scalarType: infer ScalarType;
  relation: {
    isSetofReturn?: boolean;
    isNotNullable?: boolean;
  };
} ? { [K in GetFieldNodeResultName<Field$1>]: Resolved['relation']['isSetofReturn'] extends true ? ScalarType : Resolved['relation']['isNotNullable'] extends true ? ScalarType : ScalarType | null } : Resolved extends {
  referencedTable: Pick<GenericTable, 'Row' | 'Relationships'>;
  relation: GenericRelationship & {
    match: 'refrel' | 'col' | 'fkname' | 'func';
  };
  direction: string;
} ? Field$1['children'] extends [] ? {} : ProcessEmbeddedResourceResult<ClientOptions, Schema, Resolved, Field$1, CurrentTableOrView> : { [K in GetFieldNodeResultName<Field$1>]: Resolved } : { [K in GetFieldNodeResultName<Field$1>]: SelectQueryError<'Failed to resolve relationship.'> & string };
/**
 * Helper type to process the result of an embedded resource.
 */
type ProcessEmbeddedResourceResult<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Resolved$1 extends {
  referencedTable: Pick<GenericTable, 'Row' | 'Relationships'>;
  relation: GenericRelationship & {
    match: 'refrel' | 'col' | 'fkname' | 'func';
    isNotNullable?: boolean;
    referencedRelation: string;
    isSetofReturn?: boolean;
  };
  direction: string;
}, Field$1 extends Ast.FieldNode, CurrentTableOrView extends keyof TablesAndViews$2<Schema>> = ProcessNodes<ClientOptions, Schema, Resolved$1['referencedTable']['Row'], Resolved$1['relation']['match'] extends 'func' ? Resolved$1['relation']['referencedRelation'] : Field$1['name'], Resolved$1['referencedTable']['Relationships'], Field$1['children'] extends undefined ? [] : Exclude<Field$1['children'], undefined> extends Ast.Node[] ? Exclude<Field$1['children'], undefined> : []> extends infer ProcessedChildren ? { [K in GetFieldNodeResultName<Field$1>]: Resolved$1['direction'] extends 'forward' ? Field$1 extends {
  innerJoin: true;
} ? Resolved$1['relation']['isOneToOne'] extends true ? ProcessedChildren : ProcessedChildren[] : Resolved$1['relation']['isOneToOne'] extends true ? Resolved$1['relation']['match'] extends 'func' ? Resolved$1['relation']['isNotNullable'] extends true ? Resolved$1['relation']['isSetofReturn'] extends true ? ProcessedChildren : { [P in keyof ProcessedChildren]: ProcessedChildren[P] | null } : ProcessedChildren | null : ProcessedChildren | null : ProcessedChildren[] : Resolved$1['relation']['referencedRelation'] extends CurrentTableOrView ? Resolved$1['relation'] extends {
  hint: string;
} ? ProcessedChildren[] : Resolved$1['relation']['match'] extends 'col' ? IsRelationNullable<TablesAndViews$2<Schema>[CurrentTableOrView], Resolved$1['relation']> extends true ? ProcessedChildren | null : ProcessedChildren : ProcessedChildren[] : IsRelationNullable<TablesAndViews$2<Schema>[CurrentTableOrView], Resolved$1['relation']> extends true ? Field$1 extends {
  innerJoin: true;
} ? ProcessedChildren : ProcessedChildren | null : ProcessedChildren } : { [K in GetFieldNodeResultName<Field$1>]: SelectQueryError<'Failed to process embedded resource nodes.'> & string };
/**
 * Processes a SpreadNode by processing its target node.
 *
 * @param Schema - Database schema.
 * @param Row - The type of a row in the current table.
 * @param RelationName - The name of the current table or view.
 * @param Relationships - Relationships of the current table.
 * @param Spread - The SpreadNode to process.
 */
type ProcessSpreadNode<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, RelationName extends string, Relationships extends GenericRelationship[], Spread extends Ast.SpreadNode> = ProcessNode<ClientOptions, Schema, Row, RelationName, Relationships, Spread['target']> extends infer Result ? Result extends SelectQueryError<infer E> ? SelectQueryError<E> : ExtractFirstProperty<Result> extends unknown[] ? SpreadOnManyEnabled<ClientOptions['PostgrestVersion']> extends true ? ProcessManyToManySpreadNodeResult<Result> : { [K in Spread['target']['name']]: SelectQueryError<`"${RelationName}" and "${Spread['target']['name']}" do not form a many-to-one or one-to-one relationship spread not possible`> } : ProcessSpreadNodeResult<Result> : never;
/**
 * Helper type to process the result of a many-to-many spread node.
 * Converts all fields in the spread object into arrays.
 */
type ProcessManyToManySpreadNodeResult<Result$1> = Result$1 extends Record<string, SelectQueryError<string> | null> ? Result$1 : ExtractFirstProperty<Result$1> extends infer SpreadedObject ? SpreadedObject extends Array<Record<string, unknown>> ? { [K in keyof SpreadedObject[number]]: Array<SpreadedObject[number][K]> } : SelectQueryError<'An error occurred spreading the many-to-many object'> : SelectQueryError<'An error occurred spreading the many-to-many object'>;
/**
 * Helper type to process the result of a spread node.
 */
type ProcessSpreadNodeResult<Result$1> = Result$1 extends Record<string, SelectQueryError<string> | null> ? Result$1 : ExtractFirstProperty<Result$1> extends infer SpreadedObject ? ContainsNull<SpreadedObject> extends true ? Exclude<{ [K in keyof SpreadedObject]: SpreadedObject[K] | null }, null> : Exclude<{ [K in keyof SpreadedObject]: SpreadedObject[K] }, null> : SelectQueryError<'An error occurred spreading the object'>;
//#endregion
//#region src/PostgrestTransformBuilder.d.ts
declare class PostgrestTransformBuilder<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, Result$1, RelationName = unknown, Relationships = unknown, Method = unknown, ThrowOnError extends boolean = false> extends PostgrestBuilder<ClientOptions, Result$1, ThrowOnError> {
  throwOnError(): PostgrestTransformBuilder<ClientOptions, Schema, Row, Result$1, RelationName, Relationships, Method, true>;
  /**
   * Perform a SELECT on the query result.
   *
   * By default, `.insert()`, `.update()`, `.upsert()`, and `.delete()` do not
   * return modified rows. By calling this method, modified rows are returned in
   * `data`.
   *
   * @param columns - The columns to retrieve, separated by commas
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `upsert()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .upsert({ id: 1, name: 'Han Solo' })
   *   .select()
   * ```
   *
   * @exampleSql With `upsert()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Han');
   * ```
   *
   * @exampleResponse With `upsert()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Han Solo"
   *     }
   *   ],
   *   "status": 201,
   *   "statusText": ""
   * }
   * ```
   */
  select<Query extends string = '*', NewResultOne = GetResult<Schema, Row, RelationName, Relationships, Query, ClientOptions>>(columns?: Query): PostgrestFilterBuilder<ClientOptions, Schema, Row, Method extends 'RPC' ? Result$1 extends unknown[] ? NewResultOne[] : NewResultOne : NewResultOne[], RelationName, Relationships, Method, ThrowOnError>;
  /**
   * Order the query result by `column`.
   *
   * You can call this method multiple times to order by multiple columns.
   *
   * You can order referenced tables, but it only affects the ordering of the
   * parent table if you use `!inner` in the query.
   *
   * @param column - The column to order by
   * @param options - Named parameters
   * @param options.ascending - If `true`, the result will be in ascending order
   * @param options.nullsFirst - If `true`, `null`s appear first. If `false`,
   * `null`s appear last.
   * @param options.referencedTable - Set this to order a referenced table by
   * its columns
   *
   * @category Database
   * @subcategory Using modifiers
   */
  order<ColumnName extends string & keyof Row>(column: ColumnName, options?: {
    ascending?: boolean;
    nullsFirst?: boolean;
    referencedTable?: undefined;
  }): this;
  order(column: string, options?: {
    ascending?: boolean;
    nullsFirst?: boolean;
    referencedTable?: string;
  }): this;
  /**
   * @deprecated Use `options.referencedTable` instead of `options.foreignTable`
   */
  order<ColumnName extends string & keyof Row>(column: ColumnName, options?: {
    ascending?: boolean;
    nullsFirst?: boolean;
    foreignTable?: undefined;
  }): this;
  /**
   * @deprecated Use `options.referencedTable` instead of `options.foreignTable`
   */
  order(column: string, options?: {
    ascending?: boolean;
    nullsFirst?: boolean;
    foreignTable?: string;
  }): this;
  /**
   * Limit the query result by `rows`.
   *
   * @param rows - The maximum number of rows to return
   * @param options - Named parameters
   * @param options.referencedTable - Set this to limit rows of referenced
   * tables instead of the parent table
   * @param options.foreignTable - Deprecated, use `options.referencedTable`
   * instead
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .limit(1)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Luke"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example On a referenced table
   * ```ts
   * const { data, error } = await supabase
   *   .from('orchestral_sections')
   *   .select(`
   *     name,
   *     instruments (
   *       name
   *     )
   *   `)
   *   .limit(1, { referencedTable: 'instruments' })
   * ```
   *
   * @exampleSql On a referenced table
   * ```sql
   * create table
   *   orchestral_sections (id int8 primary key, name text);
   * create table
   *   instruments (
   *     id int8 primary key,
   *     section_id int8 not null references orchestral_sections,
   *     name text
   *   );
   *
   * insert into
   *   orchestral_sections (id, name)
   * values
   *   (1, 'strings');
   * insert into
   *   instruments (id, section_id, name)
   * values
   *   (1, 1, 'harp'),
   *   (2, 1, 'violin');
   * ```
   *
   * @exampleResponse On a referenced table
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "strings",
   *       "instruments": [
   *         {
   *           "name": "violin"
   *         }
   *       ]
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  limit(rows: number, {
    foreignTable,
    referencedTable
  }?: {
    foreignTable?: string;
    referencedTable?: string;
  }): this;
  /**
   * Limit the query result by starting at an offset `from` and ending at the offset `to`.
   * Only records within this range are returned.
   * This respects the query order and if there is no order clause the range could behave unexpectedly.
   * The `from` and `to` values are 0-based and inclusive: `range(1, 3)` will include the second, third
   * and fourth rows of the query.
   *
   * @param from - The starting index from which to limit the result
   * @param to - The last index to which to limit the result
   * @param options - Named parameters
   * @param options.referencedTable - Set this to limit rows of referenced
   * tables instead of the parent table
   * @param options.foreignTable - Deprecated, use `options.referencedTable`
   * instead
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .range(0, 1)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Luke"
   *     },
   *     {
   *       "name": "Leia"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  range(from: number, to: number, {
    foreignTable,
    referencedTable
  }?: {
    foreignTable?: string;
    referencedTable?: string;
  }): this;
  /**
   * Set the AbortSignal for the fetch request.
   *
   * @param signal - The AbortSignal to use for the fetch request
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @remarks
   * You can use this to set a timeout for the request.
   *
   * @exampleDescription Aborting requests in-flight
   * You can use an [`AbortController`](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) to abort requests.
   * Note that `status` and `statusText` don't mean anything for aborted requests as the request wasn't fulfilled.
   *
   * @example Aborting requests in-flight
   * ```ts
   * const ac = new AbortController()
   *
   * const { data, error } = await supabase
   *   .from('very_big_table')
   *   .select()
   *   .abortSignal(ac.signal)
   *
   * // Abort the request after 100 ms
   * setTimeout(() => ac.abort(), 100)
   * ```
   *
   * @exampleResponse Aborting requests in-flight
   * ```json
   *   {
   *     "error": {
   *       "message": "AbortError: The user aborted a request.",
   *       "details": "",
   *       "hint": "The request was aborted locally via the provided AbortSignal.",
   *       "code": ""
   *     },
   *     "status": 0,
   *     "statusText": ""
   *   }
   *
   * ```
   *
   * @example Set a timeout
   * ```ts
   * const { data, error } = await supabase
   *   .from('very_big_table')
   *   .select()
   *   .abortSignal(AbortSignal.timeout(1000 /* ms *\/))
   * ```
   *
   * @exampleResponse Set a timeout
   * ```json
   *   {
   *     "error": {
   *       "message": "FetchError: The user aborted a request.",
   *       "details": "",
   *       "hint": "",
   *       "code": ""
   *     },
   *     "status": 0,
   *     "statusText": ""
   *   }
   *
   * ```
   */
  abortSignal(signal: AbortSignal): this;
  /**
   * Return `data` as a single object instead of an array of objects.
   *
   * Query result must be one row (e.g. using `.limit(1)`), otherwise this
   * returns an error.
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .limit(1)
   *   .single()
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": {
   *     "name": "Luke"
   *   },
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  single<ResultOne = (Result$1 extends (infer ResultOne)[] ? ResultOne : never)>(): PostgrestBuilder<ClientOptions, ResultOne, ThrowOnError>;
  /**
   * Return `data` as a single object instead of an array of objects.
   *
   * Query result must be zero or one row (e.g. using `.limit(1)`), otherwise
   * this returns an error.
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .eq('name', 'Katniss')
   *   .maybeSingle()
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  maybeSingle<ResultOne = (Result$1 extends (infer ResultOne)[] ? ResultOne : never)>(): PostgrestBuilder<ClientOptions, ResultOne | null, ThrowOnError>;
  /**
   * Return `data` as a string in CSV format.
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @exampleDescription Return data as CSV
   * By default, the data is returned in JSON format, but can also be returned as Comma Separated Values.
   *
   * @example Return data as CSV
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .csv()
   * ```
   *
   * @exampleSql Return data as CSV
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse Return data as CSV
   * ```json
   * {
   *   "data": "id,name\n1,Luke\n2,Leia\n3,Han",
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  csv(): PostgrestBuilder<ClientOptions, string, ThrowOnError>;
  /**
   * Return `data` as an object in [GeoJSON](https://geojson.org) format.
   *
   * @category Database
   * @subcategory Using modifiers
   */
  geojson(): PostgrestBuilder<ClientOptions, Record<string, unknown>, ThrowOnError>;
  /**
   * Return `data` as the EXPLAIN plan for the query.
   *
   * You need to enable the
   * [db_plan_enabled](https://supabase.com/docs/guides/database/debugging-performance#enabling-explain)
   * setting before using this method.
   *
   * @param options - Named parameters
   *
   * @param options.analyze - If `true`, the query will be executed and the
   * actual run time will be returned
   *
   * @param options.verbose - If `true`, the query identifier will be returned
   * and `data` will include the output columns of the query
   *
   * @param options.settings - If `true`, include information on configuration
   * parameters that affect query planning
   *
   * @param options.buffers - If `true`, include information on buffer usage
   *
   * @param options.wal - If `true`, include information on WAL record generation
   *
   * @param options.format - The format of the output, can be `"text"` (default)
   * or `"json"`
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @exampleDescription Get the execution plan
   * By default, the data is returned in TEXT format, but can also be returned as JSON by using the `format` parameter.
   *
   * @example Get the execution plan
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .explain()
   * ```
   *
   * @exampleSql Get the execution plan
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse Get the execution plan
   * ```js
   * Aggregate  (cost=33.34..33.36 rows=1 width=112)
   *   ->  Limit  (cost=0.00..18.33 rows=1000 width=40)
   *         ->  Seq Scan on characters  (cost=0.00..22.00 rows=1200 width=40)
   * ```
   *
   * @exampleDescription Get the execution plan with analyze and verbose
   * By default, the data is returned in TEXT format, but can also be returned as JSON by using the `format` parameter.
   *
   * @example Get the execution plan with analyze and verbose
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .explain({analyze:true,verbose:true})
   * ```
   *
   * @exampleSql Get the execution plan with analyze and verbose
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse Get the execution plan with analyze and verbose
   * ```js
   * Aggregate  (cost=33.34..33.36 rows=1 width=112) (actual time=0.041..0.041 rows=1 loops=1)
   *   Output: NULL::bigint, count(ROW(characters.id, characters.name)), COALESCE(json_agg(ROW(characters.id, characters.name)), '[]'::json), NULLIF(current_setting('response.headers'::text, true), ''::text), NULLIF(current_setting('response.status'::text, true), ''::text)
   *   ->  Limit  (cost=0.00..18.33 rows=1000 width=40) (actual time=0.005..0.006 rows=3 loops=1)
   *         Output: characters.id, characters.name
   *         ->  Seq Scan on public.characters  (cost=0.00..22.00 rows=1200 width=40) (actual time=0.004..0.005 rows=3 loops=1)
   *               Output: characters.id, characters.name
   * Query Identifier: -4730654291623321173
   * Planning Time: 0.407 ms
   * Execution Time: 0.119 ms
   * ```
   */
  explain({
    analyze,
    verbose,
    settings,
    buffers,
    wal,
    format
  }?: {
    analyze?: boolean;
    verbose?: boolean;
    settings?: boolean;
    buffers?: boolean;
    wal?: boolean;
    format?: 'json' | 'text';
  }): PostgrestBuilder<ClientOptions, Record<string, unknown>[], ThrowOnError> | PostgrestBuilder<ClientOptions, string, ThrowOnError>;
  /**
   * Dry-run this request: execute the query but discard the changes.
   *
   * Server-side, PostgREST runs the query inside a transaction and rolls it back
   * instead of committing. The response still contains the data that *would* have
   * been returned — `RETURNING` clauses execute and RLS, triggers, and constraints
   * are all evaluated — but no row is actually inserted, updated, or deleted.
   *
   * This affects only the single request it is chained to. The JS caller has no
   * handle on the transaction: supabase-js does not group multiple queries into
   * one transaction. For multi-statement transactional logic, use a database
   * function (`supabase.rpc(...)`).
   *
   * Sets the `Prefer: tx=rollback` header. See PostgREST's docs on transaction
   * preferences for the underlying mechanism.
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @example Validate an insert without persisting
   * ```ts
   * const { data, error } = await supabase
   *   .from('countries')
   *   .insert({ name: 'France' })
   *   .select()
   *   .rollback()
   * // `data` shows what would have been inserted; nothing is saved.
   * ```
   */
  rollback(): this;
  /**
   * Override the type of the returned `data`.
   *
   * @typeParam NewResult - The new result type to override with
   * @deprecated Use overrideTypes<yourType, { merge: false }>() method at the end of your call chain instead
   *
   * @category Database
   * @subcategory Using modifiers
   *
   * @remarks
   * - Deprecated: use overrideTypes method instead
   *
   * @example Override type of successful response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .returns<Array<MyType>>()
   * ```
   *
   * @exampleResponse Override type of successful response
   * ```js
   * let x: typeof data // MyType[]
   * ```
   *
   * @example Override type of object response
   * ```ts
   * const { data } = await supabase
   *   .from('countries')
   *   .select()
   *   .maybeSingle()
   *   .returns<MyType>()
   * ```
   *
   * @exampleResponse Override type of object response
   * ```js
   * let x: typeof data // MyType | null
   * ```
   */
  returns<NewResult>(): PostgrestTransformBuilder<ClientOptions, Schema, Row, CheckMatchingArrayTypes<Result$1, NewResult>, RelationName, Relationships, Method, ThrowOnError>;
  /**
   * Set the maximum number of rows that can be affected by the query.
   * Only available in PostgREST v13+ and only works with PATCH and DELETE methods.
   *
   * @param rows - The maximum number of rows that can be affected
   *
   * @category Database
   * @subcategory Using modifiers
   */
  maxAffected(rows: number): MaxAffectedEnabled<ClientOptions['PostgrestVersion']> extends true ? Method extends 'PATCH' | 'DELETE' | 'RPC' ? this : InvalidMethodError<'maxAffected method only available on update or delete'> : InvalidMethodError<'maxAffected method only available on postgrest 13+'>;
}
//#endregion
//#region src/PostgrestFilterBuilder.d.ts
type FilterOperator = 'eq' | 'neq' | 'gt' | 'gte' | 'lt' | 'lte' | 'like' | 'ilike' | 'is' | 'isdistinct' | 'in' | 'cs' | 'cd' | 'sl' | 'sr' | 'nxl' | 'nxr' | 'adj' | 'ov' | 'fts' | 'plfts' | 'phfts' | 'wfts' | 'match' | 'imatch';
type IsStringOperator<Path extends string> = Path extends `${string}->>${string}` ? true : false;
type ResolveFilterValue<Schema extends GenericSchema, Row extends Record<string, unknown>, ColumnName extends string> = ColumnName extends `${infer RelationshipTable}.${infer Remainder}` ? Remainder extends `${infer _}.${infer _}` ? ResolveFilterValue<Schema, Row, Remainder> : ResolveFilterRelationshipValue<Schema, RelationshipTable, Remainder> : ColumnName extends keyof Row ? Row[ColumnName] : IsStringOperator<ColumnName> extends true ? string : JsonPathToType<Row, JsonPathToAccessor<ColumnName>> extends infer JsonPathValue ? JsonPathValue extends never ? never : JsonPathValue : never;
type ResolveFilterRelationshipValue<Schema extends GenericSchema, RelationshipTable$1 extends string, RelationshipColumn extends string> = Schema['Tables'] & Schema['Views'] extends infer TablesAndViews ? RelationshipTable$1 extends keyof TablesAndViews ? 'Row' extends keyof TablesAndViews[RelationshipTable$1] ? RelationshipColumn extends keyof TablesAndViews[RelationshipTable$1]['Row'] ? TablesAndViews[RelationshipTable$1]['Row'][RelationshipColumn] : unknown : unknown : unknown : never;
type InvalidMethodError<S extends string> = {
  Error: S;
};
type NonNullableColumn<T extends Record<string, unknown>, Col extends string> = Col extends keyof T ? { [K in keyof T]: K extends Col ? NonNullable<T[K]> : T[K] } : T;
type NarrowResultColumn<T, Col extends string> = T extends (infer Item)[] ? Item extends Record<string, unknown> ? Col extends keyof Item ? { [K in keyof Item]: K extends Col ? NonNullable<Item[K]> : Item[K] }[] : T : T : T extends Record<string, unknown> ? Col extends keyof T ? { [K in keyof T]: K extends Col ? NonNullable<T[K]> : T[K] } : T : T;
declare class PostgrestFilterBuilder<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Row extends Record<string, unknown>, Result$1, RelationName = unknown, Relationships = unknown, Method = unknown, ThrowOnError extends boolean = false> extends PostgrestTransformBuilder<ClientOptions, Schema, Row, Result$1, RelationName, Relationships, Method, ThrowOnError> {
  throwOnError(): PostgrestFilterBuilder<ClientOptions, Schema, Row, Result$1, RelationName, Relationships, Method, true>;
  /**
   * Match only rows where `column` is equal to `value`.
   *
   * To check if the value of `column` is NULL, you should use `.is()` instead.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .eq('name', 'Leia')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 2,
   *       "name": "Leia"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  eq<ColumnName extends string>(column: ColumnName extends keyof Row ? ColumnName : ColumnName extends `${string}.${string}` | `${string}->${string}` ? ColumnName : string extends ColumnName ? string : keyof Row, value: ResolveFilterValue<Schema, Row, ColumnName> extends never ? NonNullable<unknown> : ResolveFilterValue<Schema, Row, ColumnName> extends infer ResolvedFilterValue ? NonNullable<ResolvedFilterValue> : never): this;
  /**
   * Match only rows where `column` is not equal to `value`.
   *
   * This filter does not include rows where `column` is `NULL`. To match null
   * values, use `.is(column, null)` instead.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .neq('name', 'Leia')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     },
   *     {
   *       "id": 3,
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  neq<ColumnName extends string>(column: ColumnName extends keyof Row ? ColumnName : ColumnName extends `${string}.${string}` | `${string}->${string}` ? ColumnName : string extends ColumnName ? string : keyof Row, value: ResolveFilterValue<Schema, Row, ColumnName> extends never ? unknown : ResolveFilterValue<Schema, Row, ColumnName> extends infer Resolved ? Resolved : never): this;
  /**
   * Match only rows where `column` is greater than `value`.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * When using [reserved words](https://www.postgresql.org/docs/current/sql-keywords-appendix.html) for column names you need
   * to add double quotes e.g. `.gt('"order"', 2)`
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .gt('id', 2)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 3,
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  gt<ColumnName extends string & keyof Row>(column: ColumnName, value: Row[ColumnName]): this;
  gt(column: string, value: unknown): this;
  /**
   * Match only rows where `column` is greater than or equal to `value`.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .gte('id', 2)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 2,
   *       "name": "Leia"
   *     },
   *     {
   *       "id": 3,
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  gte<ColumnName extends string & keyof Row>(column: ColumnName, value: Row[ColumnName]): this;
  gte(column: string, value: unknown): this;
  /**
   * Match only rows where `column` is less than `value`.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .lt('id', 2)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  lt<ColumnName extends string & keyof Row>(column: ColumnName, value: Row[ColumnName]): this;
  lt(column: string, value: unknown): this;
  /**
   * Match only rows where `column` is less than or equal to `value`.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .lte('id', 2)
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     },
   *     {
   *       "id": 2,
   *       "name": "Leia"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  lte<ColumnName extends string & keyof Row>(column: ColumnName, value: Row[ColumnName]): this;
  lte(column: string, value: unknown): this;
  /**
   * Match only rows where `column` matches `pattern` case-sensitively.
   *
   * @param column - The column to filter on
   * @param pattern - The pattern to match with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .like('name', '%Lu%')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  like<ColumnName extends string & keyof Row>(column: ColumnName, pattern: string): this;
  like(column: string, pattern: string): this;
  /**
   * Match only rows where `column` matches all of `patterns` case-sensitively.
   *
   * @param column - The column to filter on
   * @param patterns - The patterns to match with
   *
   * @category Database
   * @subcategory Using filters
   */
  likeAllOf<ColumnName extends string & keyof Row>(column: ColumnName, patterns: readonly string[]): this;
  likeAllOf(column: string, patterns: readonly string[]): this;
  /**
   * Match only rows where `column` matches any of `patterns` case-sensitively.
   *
   * @param column - The column to filter on
   * @param patterns - The patterns to match with
   *
   * @category Database
   * @subcategory Using filters
   */
  likeAnyOf<ColumnName extends string & keyof Row>(column: ColumnName, patterns: readonly string[]): this;
  likeAnyOf(column: string, patterns: readonly string[]): this;
  /**
   * Match only rows where `column` matches `pattern` case-insensitively.
   *
   * @param column - The column to filter on
   * @param pattern - The pattern to match with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .ilike('name', '%lu%')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Luke"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  ilike<ColumnName extends string & keyof Row>(column: ColumnName, pattern: string): this;
  ilike(column: string, pattern: string): this;
  /**
   * Match only rows where `column` matches all of `patterns` case-insensitively.
   *
   * @param column - The column to filter on
   * @param patterns - The patterns to match with
   *
   * @category Database
   * @subcategory Using filters
   */
  ilikeAllOf<ColumnName extends string & keyof Row>(column: ColumnName, patterns: readonly string[]): this;
  ilikeAllOf(column: string, patterns: readonly string[]): this;
  /**
   * Match only rows where `column` matches any of `patterns` case-insensitively.
   *
   * @param column - The column to filter on
   * @param patterns - The patterns to match with
   *
   * @category Database
   * @subcategory Using filters
   */
  ilikeAnyOf<ColumnName extends string & keyof Row>(column: ColumnName, patterns: readonly string[]): this;
  ilikeAnyOf(column: string, patterns: readonly string[]): this;
  /**
   * Match only rows where `column` matches the PostgreSQL regex `pattern`
   * case-sensitively (using the `~` operator).
   *
   * @param column - The column to filter on
   * @param pattern - The PostgreSQL regular expression pattern to match with
   */
  regexMatch<ColumnName extends string & keyof Row>(column: ColumnName, pattern: string): this;
  regexMatch(column: string, pattern: string): this;
  /**
   * Match only rows where `column` matches the PostgreSQL regex `pattern`
   * case-insensitively (using the `~*` operator).
   *
   * @param column - The column to filter on
   * @param pattern - The PostgreSQL regular expression pattern to match with
   */
  regexIMatch<ColumnName extends string & keyof Row>(column: ColumnName, pattern: string): this;
  regexIMatch(column: string, pattern: string): this;
  /**
   * Match only rows where `column` IS `value`.
   *
   * For non-boolean columns, this is only relevant for checking if the value of
   * `column` is NULL by setting `value` to `null`.
   *
   * For boolean columns, you can also set `value` to `true` or `false` and it
   * will behave the same way as `.eq()`.
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription Checking for nullness, true or false
   * Using the `eq()` filter doesn't work when filtering for `null`.
   *
   * Instead, you need to use `is()`.
   *
   * @example Checking for nullness, true or false
   * ```ts
   * const { data, error } = await supabase
   *   .from('countries')
   *   .select()
   *   .is('name', null)
   * ```
   *
   * @exampleSql Checking for nullness, true or false
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   *
   * insert into
   *   countries (id, name)
   * values
   *   (1, 'null'),
   *   (2, null);
   * ```
   *
   * @exampleResponse Checking for nullness, true or false
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 2,
   *       "name": "null"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  is<ColumnName extends string & keyof Row>(column: ColumnName, value: Row[ColumnName] & (boolean | null)): this;
  is(column: string, value: boolean | null): this;
  /**
   * Match only rows where `column` IS DISTINCT FROM `value`.
   *
   * Unlike `.neq()`, this treats `NULL` as a comparable value. Two `NULL` values
   * are considered equal (not distinct), and comparing `NULL` with any non-NULL
   * value returns true (distinct).
   *
   * @param column - The column to filter on
   * @param value - The value to filter with
   */
  isDistinct<ColumnName extends string>(column: ColumnName, value: ResolveFilterValue<Schema, Row, ColumnName> extends never ? unknown : ResolveFilterValue<Schema, Row, ColumnName> extends infer ResolvedFilterValue ? ResolvedFilterValue : never): this;
  /**
   * Match only rows where `column` is included in the `values` array.
   *
   * @param column - The column to filter on
   * @param values - The values array to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .in('name', ['Leia', 'Han'])
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 2,
   *       "name": "Leia"
   *     },
   *     {
   *       "id": 3,
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  in<ColumnName extends string>(column: ColumnName, values: ReadonlyArray<ResolveFilterValue<Schema, Row, ColumnName> extends never ? unknown : ResolveFilterValue<Schema, Row, ColumnName> extends infer ResolvedFilterValue ? ResolvedFilterValue : never>): this;
  /**
   * Match only rows where `column` is NOT included in the `values` array.
   *
   * @param column - The column to filter on
   * @param values - The values array to filter with
   */
  notIn<ColumnName extends string>(column: ColumnName, values: ReadonlyArray<ResolveFilterValue<Schema, Row, ColumnName> extends never ? unknown : ResolveFilterValue<Schema, Row, ColumnName> extends infer ResolvedFilterValue ? ResolvedFilterValue : never>): this;
  /**
   * Only relevant for jsonb, array, and range columns. Match only rows where
   * `column` contains every element appearing in `value`.
   *
   * @param column - The jsonb, array, or range column to filter on
   * @param value - The jsonb, array, or range value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example On array columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('issues')
   *   .select()
   *   .contains('tags', ['is:open', 'priority:low'])
   * ```
   *
   * @exampleSql On array columns
   * ```sql
   * create table
   *   issues (
   *     id int8 primary key,
   *     title text,
   *     tags text[]
   *   );
   *
   * insert into
   *   issues (id, title, tags)
   * values
   *   (1, 'Cache invalidation is not working', array['is:open', 'severity:high', 'priority:low']),
   *   (2, 'Use better names', array['is:open', 'severity:low', 'priority:medium']);
   * ```
   *
   * @exampleResponse On array columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "title": "Cache invalidation is not working"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription On range columns
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example On range columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .contains('during', '[2000-01-01 13:00, 2000-01-01 13:30)')
   * ```
   *
   * @exampleSql On range columns
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse On range columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "room_name": "Emerald",
   *       "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example On `jsonb` columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('users')
   *   .select('name')
   *   .contains('address', { postcode: 90210 })
   * ```
   *
   * @exampleSql On `jsonb` columns
   * ```sql
   * create table
   *   users (
   *     id int8 primary key,
   *     name text,
   *     address jsonb
   *   );
   *
   * insert into
   *   users (id, name, address)
   * values
   *   (1, 'Michael', '{ "postcode": 90210, "street": "Melrose Place" }'),
   *   (2, 'Jane', '{}');
   * ```
   *
   * @exampleResponse On `jsonb` columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Michael"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  contains<ColumnName extends string & keyof Row>(column: ColumnName, value: string | ReadonlyArray<Row[ColumnName]> | Record<string, unknown>): this;
  contains(column: string, value: string | readonly unknown[] | Record<string, unknown>): this;
  /**
   * Only relevant for jsonb, array, and range columns. Match only rows where
   * every element appearing in `column` is contained by `value`.
   *
   * @param column - The jsonb, array, or range column to filter on
   * @param value - The jsonb, array, or range value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example On array columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('classes')
   *   .select('name')
   *   .containedBy('days', ['monday', 'tuesday', 'wednesday', 'friday'])
   * ```
   *
   * @exampleSql On array columns
   * ```sql
   * create table
   *   classes (
   *     id int8 primary key,
   *     name text,
   *     days text[]
   *   );
   *
   * insert into
   *   classes (id, name, days)
   * values
   *   (1, 'Chemistry', array['monday', 'friday']),
   *   (2, 'History', array['monday', 'wednesday', 'thursday']);
   * ```
   *
   * @exampleResponse On array columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Chemistry"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription On range columns
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example On range columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .containedBy('during', '[2000-01-01 00:00, 2000-01-01 23:59)')
   * ```
   *
   * @exampleSql On range columns
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse On range columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "room_name": "Emerald",
   *       "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example On `jsonb` columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('users')
   *   .select('name')
   *   .containedBy('address', {})
   * ```
   *
   * @exampleSql On `jsonb` columns
   * ```sql
   * create table
   *   users (
   *     id int8 primary key,
   *     name text,
   *     address jsonb
   *   );
   *
   * insert into
   *   users (id, name, address)
   * values
   *   (1, 'Michael', '{ "postcode": 90210, "street": "Melrose Place" }'),
   *   (2, 'Jane', '{}');
   * ```
   *
   * @exampleResponse On `jsonb` columns
   * ```json
   *   {
   *     "data": [
   *       {
   *         "name": "Jane"
   *       }
   *     ],
   *     "status": 200,
   *     "statusText": "OK"
   *   }
   *
   * ```
   */
  containedBy<ColumnName extends string & keyof Row>(column: ColumnName, value: string | ReadonlyArray<Row[ColumnName]> | Record<string, unknown>): this;
  containedBy(column: string, value: string | readonly unknown[] | Record<string, unknown>): this;
  /**
   * Only relevant for range columns. Match only rows where every element in
   * `column` is greater than any element in `range`.
   *
   * @param column - The range column to filter on
   * @param range - The range to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .rangeGt('during', '[2000-01-02 08:00, 2000-01-02 09:00)')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   *   {
   *     "data": [
   *       {
   *         "id": 2,
   *         "room_name": "Topaz",
   *         "during": "[\"2000-01-02 09:00:00\",\"2000-01-02 10:00:00\")"
   *       }
   *     ],
   *     "status": 200,
   *     "statusText": "OK"
   *   }
   *
   * ```
   */
  rangeGt<ColumnName extends string & keyof Row>(column: ColumnName, range: string): this;
  rangeGt(column: string, range: string): this;
  /**
   * Only relevant for range columns. Match only rows where every element in
   * `column` is either contained in `range` or greater than any element in
   * `range`.
   *
   * @param column - The range column to filter on
   * @param range - The range to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .rangeGte('during', '[2000-01-02 08:30, 2000-01-02 09:30)')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   *   {
   *     "data": [
   *       {
   *         "id": 2,
   *         "room_name": "Topaz",
   *         "during": "[\"2000-01-02 09:00:00\",\"2000-01-02 10:00:00\")"
   *       }
   *     ],
   *     "status": 200,
   *     "statusText": "OK"
   *   }
   *
   * ```
   */
  rangeGte<ColumnName extends string & keyof Row>(column: ColumnName, range: string): this;
  rangeGte(column: string, range: string): this;
  /**
   * Only relevant for range columns. Match only rows where every element in
   * `column` is less than any element in `range`.
   *
   * @param column - The range column to filter on
   * @param range - The range to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .rangeLt('during', '[2000-01-01 15:00, 2000-01-01 16:00)')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "room_name": "Emerald",
   *       "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  rangeLt<ColumnName extends string & keyof Row>(column: ColumnName, range: string): this;
  rangeLt(column: string, range: string): this;
  /**
   * Only relevant for range columns. Match only rows where every element in
   * `column` is either contained in `range` or less than any element in
   * `range`.
   *
   * @param column - The range column to filter on
   * @param range - The range to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .rangeLte('during', '[2000-01-01 14:00, 2000-01-01 16:00)')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   *   {
   *     "data": [
   *       {
   *         "id": 1,
   *         "room_name": "Emerald",
   *         "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *       }
   *     ],
   *     "status": 200,
   *     "statusText": "OK"
   *   }
   *
   * ```
   */
  rangeLte<ColumnName extends string & keyof Row>(column: ColumnName, range: string): this;
  rangeLte(column: string, range: string): this;
  /**
   * Only relevant for range columns. Match only rows where `column` is
   * mutually exclusive to `range` and there can be no element between the two
   * ranges.
   *
   * @param column - The range column to filter on
   * @param range - The range to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @exampleDescription With `select()`
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .rangeAdjacent('during', '[2000-01-01 12:00, 2000-01-01 13:00)')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "room_name": "Emerald",
   *       "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  rangeAdjacent<ColumnName extends string & keyof Row>(column: ColumnName, range: string): this;
  rangeAdjacent(column: string, range: string): this;
  /**
   * Only relevant for array and range columns. Match only rows where
   * `column` and `value` have an element in common.
   *
   * @param column - The array or range column to filter on
   * @param value - The array or range value to filter with
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example On array columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('issues')
   *   .select('title')
   *   .overlaps('tags', ['is:closed', 'severity:high'])
   * ```
   *
   * @exampleSql On array columns
   * ```sql
   * create table
   *   issues (
   *     id int8 primary key,
   *     title text,
   *     tags text[]
   *   );
   *
   * insert into
   *   issues (id, title, tags)
   * values
   *   (1, 'Cache invalidation is not working', array['is:open', 'severity:high', 'priority:low']),
   *   (2, 'Use better names', array['is:open', 'severity:low', 'priority:medium']);
   * ```
   *
   * @exampleResponse On array columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "title": "Cache invalidation is not working"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription On range columns
   * Postgres supports a number of [range
   * types](https://www.postgresql.org/docs/current/rangetypes.html). You
   * can filter on range columns using the string representation of range
   * values.
   *
   * @example On range columns
   * ```ts
   * const { data, error } = await supabase
   *   .from('reservations')
   *   .select()
   *   .overlaps('during', '[2000-01-01 12:45, 2000-01-01 13:15)')
   * ```
   *
   * @exampleSql On range columns
   * ```sql
   * create table
   *   reservations (
   *     id int8 primary key,
   *     room_name text,
   *     during tsrange
   *   );
   *
   * insert into
   *   reservations (id, room_name, during)
   * values
   *   (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
   *   (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');
   * ```
   *
   * @exampleResponse On range columns
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "room_name": "Emerald",
   *       "during": "[\"2000-01-01 13:00:00\",\"2000-01-01 15:00:00\")"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  overlaps<ColumnName extends string & keyof Row>(column: ColumnName, value: string | ReadonlyArray<Row[ColumnName]>): this;
  overlaps(column: string, value: string | readonly unknown[]): this;
  /**
   * Only relevant for text and tsvector columns. Match only rows where
   * `column` matches the query string in `query`.
   *
   * @param column - The text or tsvector column to filter on
   * @param query - The query text to match with
   * @param options - Named parameters
   * @param options.config - The text search configuration to use
   * @param options.type - Change how the `query` text is interpreted
   *
   * @category Database
   * @subcategory Using filters
   *
   * @remarks
   * - For more information, see [Postgres full text search](/docs/guides/database/full-text-search).
   *
   * @example Text search
   * ```ts
   * const result = await supabase
   *   .from("texts")
   *   .select("content")
   *   .textSearch("content", `'eggs' & 'ham'`, {
   *     config: "english",
   *   });
   * ```
   *
   * @exampleSql Text search
   * ```sql
   * create table texts (
   *   id      bigint
   *           primary key
   *           generated always as identity,
   *   content text
   * );
   *
   * insert into texts (content) values
   *     ('Four score and seven years ago'),
   *     ('The road goes ever on and on'),
   *     ('Green eggs and ham')
   * ;
   * ```
   *
   * @exampleResponse Text search
   * ```json
   * {
   *   "data": [
   *     {
   *       "content": "Green eggs and ham"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription Basic normalization
   * Uses PostgreSQL's `plainto_tsquery` function.
   *
   * @example Basic normalization
   * ```ts
   * const { data, error } = await supabase
   *   .from('quotes')
   *   .select('catchphrase')
   *   .textSearch('catchphrase', `'fat' & 'cat'`, {
   *     type: 'plain',
   *     config: 'english'
   *   })
   * ```
   *
   * @exampleDescription Full normalization
   * Uses PostgreSQL's `phraseto_tsquery` function.
   *
   * @example Full normalization
   * ```ts
   * const { data, error } = await supabase
   *   .from('quotes')
   *   .select('catchphrase')
   *   .textSearch('catchphrase', `'fat' & 'cat'`, {
   *     type: 'phrase',
   *     config: 'english'
   *   })
   * ```
   *
   * @exampleDescription Websearch
   * Uses PostgreSQL's `websearch_to_tsquery` function.
   * This function will never raise syntax errors, which makes it possible to use raw user-supplied input for search, and can be used
   * with advanced operators.
   *
   * - `unquoted text`: text not inside quote marks will be converted to terms separated by & operators, as if processed by plainto_tsquery.
   * - `"quoted text"`: text inside quote marks will be converted to terms separated by `<->` operators, as if processed by phraseto_tsquery.
   * - `OR`: the word “or” will be converted to the | operator.
   * - `-`: a dash will be converted to the ! operator.
   *
   * @example Websearch
   * ```ts
   * const { data, error } = await supabase
   *   .from('quotes')
   *   .select('catchphrase')
   *   .textSearch('catchphrase', `'fat or cat'`, {
   *     type: 'websearch',
   *     config: 'english'
   *   })
   * ```
   */
  textSearch<ColumnName extends string & keyof Row>(column: ColumnName, query: string, options?: {
    config?: string;
    type?: 'plain' | 'phrase' | 'websearch';
  }): this;
  textSearch(column: string, query: string, options?: {
    config?: string;
    type?: 'plain' | 'phrase' | 'websearch';
  }): this;
  /**
   * Match only rows where each column in `query` keys is equal to its
   * associated value. Shorthand for multiple `.eq()`s.
   *
   * @param query - The object to filter with, with column names as keys mapped
   * to their filter values
   *
   * @category Database
   * @subcategory Using filters
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .match({ id: 2, name: 'Leia' })
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Leia"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  match<ColumnName extends string & keyof Row>(query: Record<ColumnName, Row[ColumnName]>): this;
  match(query: Record<string, unknown>): this;
  /**
   * Match only rows which doesn't satisfy the filter.
   *
   * Unlike most filters, `opearator` and `value` are used as-is and need to
   * follow [PostgREST
   * syntax](https://postgrest.org/en/stable/api.html#operators). You also need
   * to make sure they are properly sanitized.
   *
   * @param column - The column to filter on
   * @param operator - The operator to be negated to filter with, following
   * PostgREST syntax
   * @param value - The value to filter with, following PostgREST syntax
   *
   * @category Database
   * @subcategory Using filters
   */
  not<ColumnName extends string & keyof Row>(column: ColumnName, operator: 'is', value: null): PostgrestFilterBuilder<ClientOptions, Schema, NonNullableColumn<Row, ColumnName>, NarrowResultColumn<Result$1, ColumnName>, RelationName, Relationships, Method, ThrowOnError> & this;
  not<ColumnName extends string & keyof Row>(column: ColumnName, operator: FilterOperator, value: Row[ColumnName]): this;
  not(column: string, operator: string, value: unknown): this;
  /**
   * Match only rows which satisfy at least one of the filters.
   *
   * Unlike most filters, `filters` is used as-is and needs to follow [PostgREST
   * syntax](https://postgrest.org/en/stable/api.html#operators). You also need
   * to make sure it's properly sanitized.
   *
   * It's currently not possible to do an `.or()` filter across multiple tables.
   *
   * @param filters - The filters to use, following PostgREST syntax
   * @param options - Named parameters
   * @param options.referencedTable - Set this to filter on referenced tables
   * instead of the parent table
   * @param options.foreignTable - Deprecated, use `referencedTable` instead
   *
   * @category Database
   * @subcategory Using filters
   *
   * @remarks
   * or() expects you to use the raw PostgREST syntax for the filter names and values.
   *
   * ```ts
   * .or('id.in.(5,6,7), arraycol.cs.{"a","b"}')  // Use `()` for `in` filter, `{}` for array values and `cs` for `contains()`.
   * .or('id.in.(5,6,7), arraycol.cd.{"a","b"}')  // Use `cd` for `containedBy()`
   * ```
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .or('id.eq.2,name.eq.Han')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Leia"
   *     },
   *     {
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example Use `or` with `and`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select('name')
   *   .or('id.gt.3,and(id.eq.1,name.eq.Luke)')
   * ```
   *
   * @exampleSql Use `or` with `and`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse Use `or` with `and`
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "Luke"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example Use `or` on referenced tables
   * ```ts
   * const { data, error } = await supabase
   *   .from('orchestral_sections')
   *   .select(`
   *     name,
   *     instruments!inner (
   *       name
   *     )
   *   `)
   *   .or('section_id.eq.1,name.eq.guzheng', { referencedTable: 'instruments' })
   * ```
   *
   * @exampleSql Use `or` on referenced tables
   * ```sql
   * create table
   *   orchestral_sections (id int8 primary key, name text);
   * create table
   *   instruments (
   *     id int8 primary key,
   *     section_id int8 not null references orchestral_sections,
   *     name text
   *   );
   *
   * insert into
   *   orchestral_sections (id, name)
   * values
   *   (1, 'strings'),
   *   (2, 'woodwinds');
   * insert into
   *   instruments (id, section_id, name)
   * values
   *   (1, 2, 'flute'),
   *   (2, 1, 'violin');
   * ```
   *
   * @exampleResponse Use `or` on referenced tables
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "strings",
   *       "instruments": [
   *         {
   *           "name": "violin"
   *         }
   *       ]
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  or(filters: string, {
    foreignTable,
    referencedTable
  }?: {
    foreignTable?: string;
    referencedTable?: string;
  }): this;
  /**
   * Match only rows which satisfy the filter. This is an escape hatch - you
   * should use the specific filter methods wherever possible.
   *
   * Unlike most filters, `opearator` and `value` are used as-is and need to
   * follow [PostgREST
   * syntax](https://postgrest.org/en/stable/api.html#operators). You also need
   * to make sure they are properly sanitized.
   *
   * @param column - The column to filter on
   * @param operator - The operator to filter with, following PostgREST syntax
   * @param value - The value to filter with, following PostgREST syntax
   *
   * @category Database
   * @subcategory Using filters
   *
   * @remarks
   * filter() expects you to use the raw PostgREST syntax for the filter values.
   *
   * ```ts
   * .filter('id', 'in', '(5,6,7)')  // Use `()` for `in` filter
   * .filter('arraycol', 'cs', '{"a","b"}')  // Use `cs` for `contains()`, `{}` for array values
   * ```
   *
   * @example With `select()`
   * ```ts
   * const { data, error } = await supabase
   *   .from('characters')
   *   .select()
   *   .filter('name', 'in', '("Han","Yoda")')
   * ```
   *
   * @exampleSql With `select()`
   * ```sql
   * create table
   *   characters (id int8 primary key, name text);
   *
   * insert into
   *   characters (id, name)
   * values
   *   (1, 'Luke'),
   *   (2, 'Leia'),
   *   (3, 'Han');
   * ```
   *
   * @exampleResponse With `select()`
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 3,
   *       "name": "Han"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example On a referenced table
   * ```ts
   * const { data, error } = await supabase
   *   .from('orchestral_sections')
   *   .select(`
   *     name,
   *     instruments!inner (
   *       name
   *     )
   *   `)
   *   .filter('instruments.name', 'eq', 'flute')
   * ```
   *
   * @exampleSql On a referenced table
   * ```sql
   * create table
   *   orchestral_sections (id int8 primary key, name text);
   * create table
   *    instruments (
   *     id int8 primary key,
   *     section_id int8 not null references orchestral_sections,
   *     name text
   *   );
   *
   * insert into
   *   orchestral_sections (id, name)
   * values
   *   (1, 'strings'),
   *   (2, 'woodwinds');
   * insert into
   *   instruments (id, section_id, name)
   * values
   *   (1, 2, 'flute'),
   *   (2, 1, 'violin');
   * ```
   *
   * @exampleResponse On a referenced table
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "woodwinds",
   *       "instruments": [
   *         {
   *           "name": "flute"
   *         }
   *       ]
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  filter<ColumnName extends string & keyof Row>(column: ColumnName, operator: `${'' | 'not.'}${FilterOperator}`, value: unknown): this;
  filter(column: string, operator: string, value: unknown): this;
}
//#endregion
//#region src/PostgrestQueryBuilder.d.ts
declare class PostgrestQueryBuilder<ClientOptions extends ClientServerOptions, Schema extends GenericSchema, Relation$1 extends GenericTable | GenericView, RelationName = unknown, Relationships = (Relation$1 extends {
  Relationships: infer R;
} ? R : unknown)> {
  url: URL;
  headers: Headers;
  schema?: string;
  signal?: AbortSignal;
  fetch?: Fetch;
  urlLengthLimit: number;
  /**
   * Enable or disable automatic retries for transient errors.
   * When enabled, idempotent requests (GET/HEAD/OPTIONS) that fail with network
   * errors or HTTP 503/520 responses are automatically retried with exponential
   * backoff (1s, 2s, 4s, up to 3 attempts). Defaults to `true` when not specified.
   */
  retry?: boolean;
  /**
   * Creates a query builder scoped to a Postgres table or view.
   *
   * @category Database
   *
   * @param url - The URL for the query
   * @param options - Named parameters
   * @param options.headers - Custom headers
   * @param options.schema - Postgres schema to use
   * @param options.fetch - Custom fetch implementation
   * @param options.urlLengthLimit - Maximum URL length before warning
   * @param options.retry - Enable automatic retries for transient errors (default: true)
   *
   * @example Using supabase-js (recommended)
   * ```ts
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const { data, error } = await supabase.from('users').select('*')
   * ```
   *
   * @example Standalone import for bundle-sensitive environments
   * ```ts
   * import { PostgrestQueryBuilder } from '@supabase/postgrest-js'
   *
   * const query = new PostgrestQueryBuilder(
   *   new URL('https://xyzcompany.supabase.co/rest/v1/users'),
   *   { headers: { apikey: 'your-publishable-key' }, retry: true }
   * )
   * ```
   */
  constructor(url: URL, {
    headers,
    schema,
    fetch,
    urlLengthLimit,
    retry
  }: {
    headers?: HeadersInit;
    schema?: string;
    fetch?: Fetch;
    urlLengthLimit?: number;
    retry?: boolean;
  });
  /**
   * Clone URL and headers to prevent shared state between operations.
   */
  private cloneRequestState;
  /**
       * Perform a SELECT query on the table or view.
       *
       * @param columns - The columns to retrieve, separated by commas. Columns can be renamed when returned with `customName:columnName`
       *
       * @param options - Named parameters
       *
       * @param options.head - When set to `true`, `data` will not be returned.
       * Useful if you only need the count.
       *
       * @param options.count - Count algorithm to use to count rows in the table or view.
       *
       * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
       * hood.
       *
       * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
       * statistics under the hood.
       *
       * `"estimated"`: Uses exact count for low numbers and planned count for high
       * numbers.
       *
       * @remarks
       * When using `count` with `.range()` or `.limit()`, the returned `count` is the total number of rows
       * that match your filters, not the number of rows in the current page. Use this to build pagination UI.
       
     * - By default, Supabase projects return a maximum of 1,000 rows. This setting can be changed in your project's [API settings](/dashboard/project/_/settings/api). It's recommended that you keep it low to limit the payload size of accidental or malicious requests. You can use `range()` queries to paginate through your data.
     * - `select()` can be combined with [Filters](/docs/reference/javascript/using-filters)
     * - `select()` can be combined with [Modifiers](/docs/reference/javascript/using-modifiers)
     * - `apikey` is a reserved keyword if you're using the [Supabase Platform](/docs/guides/platform) and [should be avoided as a column name](https://github.com/supabase/supabase/issues/5465). *
     * @category Database
     *
     * @example Getting your data
     * ```js
     * const { data, error } = await supabase
     *   .from('characters')
     *   .select()
     * ```
     *
     * @exampleSql Getting your data
     * ```sql
     * create table
     *   characters (id int8 primary key, name text);
     *
     * insert into
     *   characters (id, name)
     * values
     *   (1, 'Harry'),
     *   (2, 'Frodo'),
     *   (3, 'Katniss');
     * ```
     *
     * @exampleResponse Getting your data
     * ```json
     * {
     *   "data": [
     *     {
     *       "id": 1,
     *       "name": "Harry"
     *     },
     *     {
     *       "id": 2,
     *       "name": "Frodo"
     *     },
     *     {
     *       "id": 3,
     *       "name": "Katniss"
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Handling errors
     * The most useful field on a Postgres error is usually `hint` — when the database knows the fix, it puts the literal SQL there. For example, a permission-denied error (`code: '42501'`) arrives with a `hint` like `"Grant the required privileges to the current role with: GRANT SELECT ON public.characters TO anon;"`. Log the full `error` object so the hint isn't hidden behind `error.message`.
     *
     * @example Handling errors
     * ```js
     * const { data, error } = await supabase.from('characters').select()
     * if (error) {
     *   // Logs the full error: message, code, details, and hint.
     *   console.error(error)
     *   return
     * }
     * ```
     *
     * @exampleResponse Handling errors
     * ```json
     * {
     *   "error": {
     *     "code": "42501",
     *     "details": null,
     *     "hint": "Grant the required privileges to the current role with: GRANT SELECT ON public.characters TO anon;",
     *     "message": "permission denied for table characters"
     *   },
     *   "status": 401,
     *   "statusText": ""
     * }
     * ```
     *
     * @example Selecting specific columns
     * ```js
     * const { data, error } = await supabase
     *   .from('characters')
     *   .select('name')
     * ```
     *
     * @exampleSql Selecting specific columns
     * ```sql
     * create table
     *   characters (id int8 primary key, name text);
     *
     * insert into
     *   characters (id, name)
     * values
     *   (1, 'Frodo'),
     *   (2, 'Harry'),
     *   (3, 'Katniss');
     * ```
     *
     * @exampleResponse Selecting specific columns
     * ```json
     * {
     *   "data": [
     *     {
     *       "name": "Frodo"
     *     },
     *     {
     *       "name": "Harry"
     *     },
     *     {
     *       "name": "Katniss"
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Query referenced tables
     * If your database has foreign key relationships, you can query related tables too.
     *
     * @example Query referenced tables
     * ```js
     * const { data, error } = await supabase
     *   .from('orchestral_sections')
     *   .select(`
     *     name,
     *     instruments (
     *       name
     *     )
     *   `)
     * ```
     *
     * @exampleSql Query referenced tables
     * ```sql
     * create table
     *   orchestral_sections (id int8 primary key, name text);
     * create table
     *   instruments (
     *     id int8 primary key,
     *     section_id int8 not null references orchestral_sections,
     *     name text
     *   );
     *
     * insert into
     *   orchestral_sections (id, name)
     * values
     *   (1, 'strings'),
     *   (2, 'woodwinds');
     * insert into
     *   instruments (id, section_id, name)
     * values
     *   (1, 2, 'flute'),
     *   (2, 1, 'violin');
     * ```
     *
     * @exampleResponse Query referenced tables
     * ```json
     * {
     *   "data": [
     *     {
     *       "name": "strings",
     *       "instruments": [
     *         {
     *           "name": "violin"
     *         }
     *       ]
     *     },
     *     {
     *       "name": "woodwinds",
     *       "instruments": [
     *         {
     *           "name": "flute"
     *         }
     *       ]
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Query referenced tables with spaces in their names
     * If your table name contains spaces, you must use double quotes in the `select` statement to reference the table.
     *
     * @example Query referenced tables with spaces in their names
     * ```js
     * const { data, error } = await supabase
     *   .from('orchestral sections')
     *   .select(`
     *     name,
     *     "musical instruments" (
     *       name
     *     )
     *   `)
     * ```
     *
     * @exampleSql Query referenced tables with spaces in their names
     * ```sql
     * create table
     *   "orchestral sections" (id int8 primary key, name text);
     * create table
     *   "musical instruments" (
     *     id int8 primary key,
     *     section_id int8 not null references "orchestral sections",
     *     name text
     *   );
     *
     * insert into
     *   "orchestral sections" (id, name)
     * values
     *   (1, 'strings'),
     *   (2, 'woodwinds');
     * insert into
     *   "musical instruments" (id, section_id, name)
     * values
     *   (1, 2, 'flute'),
     *   (2, 1, 'violin');
     * ```
     *
     * @exampleResponse Query referenced tables with spaces in their names
     * ```json
     * {
     *   "data": [
     *     {
     *       "name": "strings",
     *       "musical instruments": [
     *         {
     *           "name": "violin"
     *         }
     *       ]
     *     },
     *     {
     *       "name": "woodwinds",
     *       "musical instruments": [
     *         {
     *           "name": "flute"
     *         }
     *       ]
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Query referenced tables through a join table
     * If you're in a situation where your tables are **NOT** directly
     * related, but instead are joined by a _join table_, you can still use
     * the `select()` method to query the related data. The join table needs
     * to have the foreign keys as part of its composite primary key.
     *
     * @example Query referenced tables through a join table
     * ```ts
     * const { data, error } = await supabase
     *   .from('users')
     *   .select(`
     *     name,
     *     teams (
     *       name
     *     )
     *   `)
     *
     * ```
     *
     * @exampleSql Query referenced tables through a join table
     * ```sql
     * create table
     *   users (
     *     id int8 primary key,
     *     name text
     *   );
     * create table
     *   teams (
     *     id int8 primary key,
     *     name text
     *   );
     * -- join table
     * create table
     *   users_teams (
     *     user_id int8 not null references users,
     *     team_id int8 not null references teams,
     *     -- both foreign keys must be part of a composite primary key
     *     primary key (user_id, team_id)
     *   );
     *
     * insert into
     *   users (id, name)
     * values
     *   (1, 'Kiran'),
     *   (2, 'Evan');
     * insert into
     *   teams (id, name)
     * values
     *   (1, 'Green'),
     *   (2, 'Blue');
     * insert into
     *   users_teams (user_id, team_id)
     * values
     *   (1, 1),
     *   (1, 2),
     *   (2, 2);
     * ```
     *
     * @exampleResponse Query referenced tables through a join table
     * ```json
     *   {
     *     "data": [
     *       {
     *         "name": "Kiran",
     *         "teams": [
     *           {
     *             "name": "Green"
     *           },
     *           {
     *             "name": "Blue"
     *           }
     *         ]
     *       },
     *       {
     *         "name": "Evan",
     *         "teams": [
     *           {
     *             "name": "Blue"
     *           }
     *         ]
     *       }
     *     ],
     *     "status": 200,
     *     "statusText": "OK"
     *   }
     *
     * ```
     *
     * @exampleDescription Query the same referenced table multiple times
     * If you need to query the same referenced table twice, use the name of the
     * joined column to identify which join to use. You can also give each
     * column an alias.
     *
     * @example Query the same referenced table multiple times
     * ```ts
     * const { data, error } = await supabase
     *   .from('messages')
     *   .select(`
     *     content,
     *     from:sender_id(name),
     *     to:receiver_id(name)
     *   `)
     *
     * // To infer types, use the name of the table (in this case `users`) and
     * // the name of the foreign key constraint.
     * const { data, error } = await supabase
     *   .from('messages')
     *   .select(`
     *     content,
     *     from:users!messages_sender_id_fkey(name),
     *     to:users!messages_receiver_id_fkey(name)
     *   `)
     * ```
     *
     * @exampleSql Query the same referenced table multiple times
     * ```sql
     *  create table
     *  users (id int8 primary key, name text);
     *
     *  create table
     *    messages (
     *      sender_id int8 not null references users,
     *      receiver_id int8 not null references users,
     *      content text
     *    );
     *
     *  insert into
     *    users (id, name)
     *  values
     *    (1, 'Kiran'),
     *    (2, 'Evan');
     *
     *  insert into
     *    messages (sender_id, receiver_id, content)
     *  values
     *    (1, 2, '👋');
     *  ```
     * ```
     *
     * @exampleResponse Query the same referenced table multiple times
     * ```json
     * {
     *   "data": [
     *     {
     *       "content": "👋",
     *       "from": {
     *         "name": "Kiran"
     *       },
     *       "to": {
     *         "name": "Evan"
     *       }
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Query nested foreign tables through a join table
     * You can use the result of a joined table to gather data in
     * another foreign table. With multiple references to the same foreign
     * table you must specify the column on which to conduct the join.
     *
     * @example Query nested foreign tables through a join table
     * ```ts
     *   const { data, error } = await supabase
     *     .from('games')
     *     .select(`
     *       game_id:id,
     *       away_team:teams!games_away_team_fkey (
     *         users (
     *           id,
     *           name
     *         )
     *       )
     *     `)
     *
     * ```
     *
     * @exampleSql Query nested foreign tables through a join table
     * ```sql
     * ```sql
     * create table
     *   users (
     *     id int8 primary key,
     *     name text
     *   );
     * create table
     *   teams (
     *     id int8 primary key,
     *     name text
     *   );
     * -- join table
     * create table
     *   users_teams (
     *     user_id int8 not null references users,
     *     team_id int8 not null references teams,
     *
     *     primary key (user_id, team_id)
     *   );
     * create table
     *   games (
     *     id int8 primary key,
     *     home_team int8 not null references teams,
     *     away_team int8 not null references teams,
     *     name text
     *   );
     *
     * insert into users (id, name)
     * values
     *   (1, 'Kiran'),
     *   (2, 'Evan');
     * insert into
     *   teams (id, name)
     * values
     *   (1, 'Green'),
     *   (2, 'Blue');
     * insert into
     *   users_teams (user_id, team_id)
     * values
     *   (1, 1),
     *   (1, 2),
     *   (2, 2);
     * insert into
     *   games (id, home_team, away_team, name)
     * values
     *   (1, 1, 2, 'Green vs Blue'),
     *   (2, 2, 1, 'Blue vs Green');
     * ```
     *
     * @exampleResponse Query nested foreign tables through a join table
     * ```json
     *   {
     *     "data": [
     *       {
     *         "game_id": 1,
     *         "away_team": {
     *           "users": [
     *             {
     *               "id": 1,
     *               "name": "Kiran"
     *             },
     *             {
     *               "id": 2,
     *               "name": "Evan"
     *             }
     *           ]
     *         }
     *       },
     *       {
     *         "game_id": 2,
     *         "away_team": {
     *           "users": [
     *             {
     *               "id": 1,
     *               "name": "Kiran"
     *             }
     *           ]
     *         }
     *       }
     *     ],
     *     "status": 200,
     *     "statusText": "OK"
     *   }
     *
     * ```
     *
     * @exampleDescription Filtering through referenced tables
     * If the filter on a referenced table's column is not satisfied, the referenced
     * table returns `[]` or `null` but the parent table is not filtered out.
     * If you want to filter out the parent table rows, use the `!inner` hint
     *
     * @example Filtering through referenced tables
     * ```ts
     * const { data, error } = await supabase
     *   .from('instruments')
     *   .select('name, orchestral_sections(*)')
     *   .eq('orchestral_sections.name', 'percussion')
     * ```
     *
     * @exampleSql Filtering through referenced tables
     * ```sql
     * create table
     *   orchestral_sections (id int8 primary key, name text);
     * create table
     *   instruments (
     *     id int8 primary key,
     *     section_id int8 not null references orchestral_sections,
     *     name text
     *   );
     *
     * insert into
     *   orchestral_sections (id, name)
     * values
     *   (1, 'strings'),
     *   (2, 'woodwinds');
     * insert into
     *   instruments (id, section_id, name)
     * values
     *   (1, 2, 'flute'),
     *   (2, 1, 'violin');
     * ```
     *
     * @exampleResponse Filtering through referenced tables
     * ```json
     * {
     *   "data": [
     *     {
     *       "name": "flute",
     *       "orchestral_sections": null
     *     },
     *     {
     *       "name": "violin",
     *       "orchestral_sections": null
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Querying referenced table with count
     * You can get the number of rows in a related table by using the
     * **count** property.
     *
     * @example Querying referenced table with count
     * ```ts
     * const { data, error } = await supabase
     *   .from('orchestral_sections')
     *   .select(`*, instruments(count)`)
     * ```
     *
     * @exampleSql Querying referenced table with count
     * ```sql
     * create table orchestral_sections (
     *   "id" "uuid" primary key default "extensions"."uuid_generate_v4"() not null,
     *   "name" text
     * );
     *
     * create table characters (
     *   "id" "uuid" primary key default "extensions"."uuid_generate_v4"() not null,
     *   "name" text,
     *   "section_id" "uuid" references public.orchestral_sections on delete cascade
     * );
     *
     * with section as (
     *   insert into orchestral_sections (name)
     *   values ('strings') returning id
     * )
     * insert into instruments (name, section_id) values
     * ('violin', (select id from section)),
     * ('viola', (select id from section)),
     * ('cello', (select id from section)),
     * ('double bass', (select id from section));
     * ```
     *
     * @exampleResponse Querying referenced table with count
     * ```json
     * [
     *   {
     *     "id": "693694e7-d993-4360-a6d7-6294e325d9b6",
     *     "name": "strings",
     *     "instruments": [
     *       {
     *         "count": 4
     *       }
     *     ]
     *   }
     * ]
     * ```
     *
     * @exampleDescription Querying with count option
     * You can get the number of rows by using the
     * [count](/docs/reference/javascript/select#parameters) option.
     *
     * @example Querying with count option
     * ```ts
     * const { count, error } = await supabase
     *   .from('characters')
     *   .select('*', { count: 'exact', head: true })
     * ```
     *
     * @exampleSql Querying with count option
     * ```sql
     * create table
     *   characters (id int8 primary key, name text);
     *
     * insert into
     *   characters (id, name)
     * values
     *   (1, 'Luke'),
     *   (2, 'Leia'),
     *   (3, 'Han');
     * ```
     *
     * @exampleResponse Querying with count option
     * ```json
     * {
     *   "count": 3,
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Querying JSON data
     * You can select and filter data inside of
     * [JSON](/docs/guides/database/json) columns. Postgres offers some
     * [operators](/docs/guides/database/json#query-the-jsonb-data) for
     * querying JSON data.
     *
     * @example Querying JSON data
     * ```ts
     * const { data, error } = await supabase
     *   .from('users')
     *   .select(`
     *     id, name,
     *     address->city
     *   `)
     * ```
     *
     * @exampleSql Querying JSON data
     * ```sql
     * create table
     *   users (
     *     id int8 primary key,
     *     name text,
     *     address jsonb
     *   );
     *
     * insert into
     *   users (id, name, address)
     * values
     *   (1, 'Frodo', '{"city":"Hobbiton"}');
     * ```
     *
     * @exampleResponse Querying JSON data
     * ```json
     * {
     *   "data": [
     *     {
     *       "id": 1,
     *       "name": "Frodo",
     *       "city": "Hobbiton"
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Querying referenced table with inner join
     * If you don't want to return the referenced table contents, you can leave the parenthesis empty.
     * Like `.select('name, orchestral_sections!inner()')`.
     *
     * @example Querying referenced table with inner join
     * ```ts
     * const { data, error } = await supabase
     *   .from('instruments')
     *   .select('name, orchestral_sections!inner(name)')
     *   .eq('orchestral_sections.name', 'woodwinds')
     *   .limit(1)
     * ```
     *
     * @exampleSql Querying referenced table with inner join
     * ```sql
     * create table orchestral_sections (
     *   "id" "uuid" primary key default "extensions"."uuid_generate_v4"() not null,
     *   "name" text
     * );
     *
     * create table instruments (
     *   "id" "uuid" primary key default "extensions"."uuid_generate_v4"() not null,
     *   "name" text,
     *   "section_id" "uuid" references public.orchestral_sections on delete cascade
     * );
     *
     * with section as (
     *   insert into orchestral_sections (name)
     *   values ('woodwinds') returning id
     * )
     * insert into instruments (name, section_id) values
     * ('flute', (select id from section)),
     * ('clarinet', (select id from section)),
     * ('bassoon', (select id from section)),
     * ('piccolo', (select id from section));
     * ```
     *
     * @exampleResponse Querying referenced table with inner join
     * ```json
     * {
     *   "data": [
     *     {
     *       "name": "flute",
     *       "orchestral_sections": {"name": "woodwinds"}
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
     *
     * @exampleDescription Switching schemas per query
     * In addition to setting the schema during initialization, you can also switch schemas on a per-query basis.
     * Make sure you've set up your [database privileges and API settings](/docs/guides/api/using-custom-schemas).
     *
     * @example Switching schemas per query
     * ```ts
     * const { data, error } = await supabase
     *   .schema('myschema')
     *   .from('mytable')
     *   .select()
     * ```
     *
     * @exampleSql Switching schemas per query
     * ```sql
     * create schema myschema;
     *
     * create table myschema.mytable (
     *   id uuid primary key default gen_random_uuid(),
     *   data text
     * );
     *
     * insert into myschema.mytable (data) values ('mydata');
     * ```
     *
     * @exampleResponse Switching schemas per query
     * ```json
     * {
     *   "data": [
     *     {
     *       "id": "4162e008-27b0-4c0f-82dc-ccaeee9a624d",
     *       "data": "mydata"
     *     }
     *   ],
     *   "status": 200,
     *   "statusText": "OK"
     * }
     * ```
       */
  select<Query extends string = '*', ResultOne = GetResult<Schema, Relation$1['Row'], RelationName, Relationships, Query, ClientOptions>>(columns?: Query, options?: {
    head?: boolean;
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
  }): PostgrestFilterBuilder<ClientOptions, Schema, Relation$1['Row'], ResultOne[], RelationName, Relationships, 'GET'>;
  /**
   * Perform an INSERT into the table or view.
   *
   * By default, inserted rows are not returned. To return it, chain the call
   * with `.select()`.
   *
   * @param values - The values to insert. Pass an object to insert a single row
   * or an array to insert multiple rows.
   *
   * @param options - Named parameters
   *
   * @param options.count - Count algorithm to use to count inserted rows.
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   *
   * @param options.defaultToNull - Make missing fields default to `null`.
   * Otherwise, use the default value for the column. Only applies for bulk
   * inserts.
   *
   * @category Database
   *
   * @example Create a record
   * ```ts
   * const { error } = await supabase
   *   .from('countries')
   *   .insert({ id: 1, name: 'Mordor' })
   * ```
   *
   * @exampleSql Create a record
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   * ```
   *
   * @exampleResponse Create a record
   * ```json
   * {
   *   "status": 201,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Handling errors
   * `error.hint` from Postgres often contains the actionable fix (e.g. `"Grant the required privileges to the current role with: GRANT INSERT ON public.countries TO anon;"` for a `42501` permission-denied error). Log the full `error` object so it isn't hidden behind `error.message`.
   *
   * @example Handling errors
   * ```js
   * const { error } = await supabase.from('countries').insert({ id: 1, name: 'Mordor' })
   * if (error) console.error(error)
   * ```
   *
   * @example Create a record and return it
   * ```ts
   * const { data, error } = await supabase
   *   .from('countries')
   *   .insert({ id: 1, name: 'Mordor' })
   *   .select()
   * ```
   *
   * @exampleSql Create a record and return it
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   * ```
   *
   * @exampleResponse Create a record and return it
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Mordor"
   *     }
   *   ],
   *   "status": 201,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Bulk create
   * A bulk create operation is handled in a single transaction.
   * If any of the inserts fail, none of the rows are inserted.
   *
   * @example Bulk create
   * ```ts
   * const { error } = await supabase
   *   .from('countries')
   *   .insert([
   *     { id: 1, name: 'Mordor' },
   *     { id: 1, name: 'The Shire' },
   *   ])
   * ```
   *
   * @exampleSql Bulk create
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   * ```
   *
   * @exampleResponse Bulk create
   * ```json
   * {
   *   "error": {
   *     "code": "23505",
   *     "details": "Key (id)=(1) already exists.",
   *     "hint": null,
   *     "message": "duplicate key value violates unique constraint \"countries_pkey\""
   *   },
   *   "status": 409,
   *   "statusText": ""
   * }
   * ```
   */
  insert<Row extends (Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never)>(values: RejectExcessProperties<Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never, Row> | RejectExcessProperties<Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never, Row>[], {
    count,
    defaultToNull
  }?: {
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
    defaultToNull?: boolean;
  }): PostgrestFilterBuilder<ClientOptions, Schema, Relation$1['Row'], null, RelationName, Relationships, 'POST'>;
  /**
   * Perform an UPSERT on the table or view. Depending on the column(s) passed
   * to `onConflict`, `.upsert()` allows you to perform the equivalent of
   * `.insert()` if a row with the corresponding `onConflict` columns doesn't
   * exist, or if it does exist, perform an alternative action depending on
   * `ignoreDuplicates`.
   *
   * By default, upserted rows are not returned. To return it, chain the call
   * with `.select()`.
   *
   * @param values - The values to upsert with. Pass an object to upsert a
   * single row or an array to upsert multiple rows.
   *
   * @param options - Named parameters
   *
   * @param options.onConflict - Comma-separated UNIQUE column(s) to specify how
   * duplicate rows are determined. Two rows are duplicates if all the
   * `onConflict` columns are equal.
   *
   * @param options.ignoreDuplicates - If `true`, duplicate rows are ignored. If
   * `false`, duplicate rows are merged with existing rows.
   *
   * @param options.count - Count algorithm to use to count upserted rows.
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   *
   * @param options.defaultToNull - Make missing fields default to `null`.
   * Otherwise, use the default value for the column. This only applies when
   * inserting new rows, not when merging with existing rows under
   * `ignoreDuplicates: false`. This also only applies when doing bulk upserts.
   *
   * @example Upsert a single row using a unique key
   * ```ts
   * // Upserting a single row, overwriting based on the 'username' unique column
   * const { data, error } = await supabase
   *   .from('users')
   *   .upsert({ username: 'supabot' }, { onConflict: 'username' })
   *
   * // Example response:
   * // {
   * //   data: [
   * //     { id: 4, message: 'bar', username: 'supabot' }
   * //   ],
   * //   error: null
   * // }
   * ```
   *
   * @example Upsert with conflict resolution and exact row counting
   * ```ts
   * // Upserting and returning exact count
   * const { data, error, count } = await supabase
   *   .from('users')
   *   .upsert(
   *     {
   *       id: 3,
   *       message: 'foo',
   *       username: 'supabot'
   *     },
   *     {
   *       onConflict: 'username',
   *       count: 'exact'
   *     }
   *   )
   *
   * // Example response:
   * // {
   * //   data: [
   * //     {
   * //       id: 42,
   * //       handle: "saoirse",
   * //       display_name: "Saoirse"
   * //     }
   * //   ],
   * //   count: 1,
   * //   error: null
   * // }
   * ```
   *
   * @category Database
   *
   * @remarks
   * - Primary keys must be included in `values` to use upsert.
   *
   * @example Upsert your data
   * ```ts
   * const { data, error } = await supabase
   *   .from('instruments')
   *   .upsert({ id: 1, name: 'piano' })
   *   .select()
   * ```
   *
   * @exampleSql Upsert your data
   * ```sql
   * create table
   *   instruments (id int8 primary key, name text);
   *
   * insert into
   *   instruments (id, name)
   * values
   *   (1, 'harpsichord');
   * ```
   *
   * @exampleResponse Upsert your data
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "piano"
   *     }
   *   ],
   *   "status": 201,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Handling errors
   * `error.hint` from Postgres often contains the actionable fix (e.g. `"Grant the required privileges to the current role with: GRANT INSERT, UPDATE ON public.instruments TO anon;"` for a `42501` permission-denied error). Log the full `error` object so it isn't hidden behind `error.message`.
   *
   * @example Handling errors
   * ```js
   * const { data, error } = await supabase.from('instruments').upsert({ id: 1, name: 'piano' }).select()
   * if (error) console.error(error)
   * ```
   *
   * @example Bulk Upsert your data
   * ```ts
   * const { data, error } = await supabase
   *   .from('instruments')
   *   .upsert([
   *     { id: 1, name: 'piano' },
   *     { id: 2, name: 'harp' },
   *   ])
   *   .select()
   * ```
   *
   * @exampleSql Bulk Upsert your data
   * ```sql
   * create table
   *   instruments (id int8 primary key, name text);
   *
   * insert into
   *   instruments (id, name)
   * values
   *   (1, 'harpsichord');
   * ```
   *
   * @exampleResponse Bulk Upsert your data
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "piano"
   *     },
   *     {
   *       "id": 2,
   *       "name": "harp"
   *     }
   *   ],
   *   "status": 201,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Upserting into tables with constraints
   * In the following query, `upsert()` implicitly uses the `id`
   * (primary key) column to determine conflicts. If there is no existing
   * row with the same `id`, `upsert()` inserts a new row, which
   * will fail in this case as there is already a row with `handle` `"saoirse"`.
   * Using the `onConflict` option, you can instruct `upsert()` to use
   * another column with a unique constraint to determine conflicts.
   *
   * @example Upserting into tables with constraints
   * ```ts
   * const { data, error } = await supabase
   *   .from('users')
   *   .upsert({ id: 42, handle: 'saoirse', display_name: 'Saoirse' })
   *   .select()
   * ```
   *
   * @exampleSql Upserting into tables with constraints
   * ```sql
   * create table
   *   users (
   *     id int8 generated by default as identity primary key,
   *     handle text not null unique,
   *     display_name text
   *   );
   *
   * insert into
   *   users (id, handle, display_name)
   * values
   *   (1, 'saoirse', null);
   * ```
   *
   * @exampleResponse Upserting into tables with constraints
   * ```json
   * {
   *   "error": {
   *     "code": "23505",
   *     "details": "Key (handle)=(saoirse) already exists.",
   *     "hint": null,
   *     "message": "duplicate key value violates unique constraint \"users_handle_key\""
   *   },
   *   "status": 409,
   *   "statusText": ""
   * }
   * ```
   */
  upsert<Row extends (Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never)>(values: RejectExcessProperties<Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never, Row> | RejectExcessProperties<Relation$1 extends {
    Insert: unknown;
  } ? Relation$1['Insert'] : never, Row>[], {
    onConflict,
    ignoreDuplicates,
    count,
    defaultToNull
  }?: {
    onConflict?: string;
    ignoreDuplicates?: boolean;
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
    defaultToNull?: boolean;
  }): PostgrestFilterBuilder<ClientOptions, Schema, Relation$1['Row'], null, RelationName, Relationships, 'POST'>;
  /**
   * Perform an UPDATE on the table or view.
   *
   * By default, updated rows are not returned. To return it, chain the call
   * with `.select()` after filters.
   *
   * @param values - The values to update with
   *
   * @param options - Named parameters
   *
   * @param options.count - Count algorithm to use to count updated rows.
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   *
   * @category Database
   *
   * @remarks
   * - `update()` should always be combined with [Filters](/docs/reference/javascript/using-filters) to target the item(s) you wish to update.
   *
   * @example Updating your data
   * ```ts
   * const { error } = await supabase
   *   .from('instruments')
   *   .update({ name: 'piano' })
   *   .eq('id', 1)
   * ```
   *
   * @exampleSql Updating your data
   * ```sql
   * create table
   *   instruments (id int8 primary key, name text);
   *
   * insert into
   *   instruments (id, name)
   * values
   *   (1, 'harpsichord');
   * ```
   *
   * @exampleResponse Updating your data
   * ```json
   * {
   *   "status": 204,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Handling errors
   * `error.hint` from Postgres often contains the actionable fix (e.g. `"Grant the required privileges to the current role with: GRANT UPDATE ON public.instruments TO anon;"` for a `42501` permission-denied error). Log the full `error` object so it isn't hidden behind `error.message`.
   *
   * @example Handling errors
   * ```js
   * const { error } = await supabase.from('instruments').update({ name: 'piano' }).eq('id', 1)
   * if (error) console.error(error)
   * ```
   *
   * @example Update a record and return it
   * ```ts
   * const { data, error } = await supabase
   *   .from('instruments')
   *   .update({ name: 'piano' })
   *   .eq('id', 1)
   *   .select()
   * ```
   *
   * @exampleSql Update a record and return it
   * ```sql
   * create table
   *   instruments (id int8 primary key, name text);
   *
   * insert into
   *   instruments (id, name)
   * values
   *   (1, 'harpsichord');
   * ```
   *
   * @exampleResponse Update a record and return it
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "piano"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription Updating JSON data
   * Postgres offers some
   * [operators](/docs/guides/database/json#query-the-jsonb-data) for
   * working with JSON data. Currently, it is only possible to update the entire JSON document.
   *
   * @example Updating JSON data
   * ```ts
   * const { data, error } = await supabase
   *   .from('users')
   *   .update({
   *     address: {
   *       street: 'Melrose Place',
   *       postcode: 90210
   *     }
   *   })
   *   .eq('address->postcode', 90210)
   *   .select()
   * ```
   *
   * @exampleSql Updating JSON data
   * ```sql
   * create table
   *   users (
   *     id int8 primary key,
   *     name text,
   *     address jsonb
   *   );
   *
   * insert into
   *   users (id, name, address)
   * values
   *   (1, 'Michael', '{ "postcode": 90210 }');
   * ```
   *
   * @exampleResponse Updating JSON data
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Michael",
   *       "address": {
   *         "street": "Melrose Place",
   *         "postcode": 90210
   *       }
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  update<Row extends (Relation$1 extends {
    Update: unknown;
  } ? Relation$1['Update'] : never)>(values: RejectExcessProperties<Relation$1 extends {
    Update: unknown;
  } ? Relation$1['Update'] : never, Row>, {
    count
  }?: {
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
  }): PostgrestFilterBuilder<ClientOptions, Schema, Relation$1['Row'], null, RelationName, Relationships, 'PATCH'>;
  /**
   * Perform a DELETE on the table or view.
   *
   * By default, deleted rows are not returned. To return it, chain the call
   * with `.select()` after filters.
   *
   * @param options - Named parameters
   *
   * @param options.count - Count algorithm to use to count deleted rows.
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   *
   * @category Database
   *
   * @remarks
   * - `delete()` should always be combined with [filters](/docs/reference/javascript/using-filters) to target the item(s) you wish to delete.
   * - If you use `delete()` with filters and you have
   *   [RLS](/docs/learn/auth-deep-dive/auth-row-level-security) enabled, only
   *   rows visible through `SELECT` policies are deleted. Note that by default
   *   no rows are visible, so you need at least one `SELECT`/`ALL` policy that
   *   makes the rows visible.
   * - When using `delete().in()`, specify an array of values to target multiple rows with a single query. This is particularly useful for batch deleting entries that share common criteria, such as deleting users by their IDs. Ensure that the array you provide accurately represents all records you intend to delete to avoid unintended data removal.
   *
   * @example Delete a single record
   * ```ts
   * const response = await supabase
   *   .from('countries')
   *   .delete()
   *   .eq('id', 1)
   * ```
   *
   * @exampleSql Delete a single record
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   *
   * insert into
   *   countries (id, name)
   * values
   *   (1, 'Mordor');
   * ```
   *
   * @exampleResponse Delete a single record
   * ```json
   * {
   *   "status": 204,
   *   "statusText": ""
   * }
   * ```
   *
   * @exampleDescription Handling errors
   * `error.hint` from Postgres often contains the actionable fix (e.g. `"Grant the required privileges to the current role with: GRANT DELETE ON public.countries TO anon;"` for a `42501` permission-denied error). Log the full `error` object so it isn't hidden behind `error.message`.
   *
   * @example Handling errors
   * ```js
   * const { error } = await supabase.from('countries').delete().eq('id', 1)
   * if (error) console.error(error)
   * ```
   *
   * @example Delete a record and return it
   * ```ts
   * const { data, error } = await supabase
   *   .from('countries')
   *   .delete()
   *   .eq('id', 1)
   *   .select()
   * ```
   *
   * @exampleSql Delete a record and return it
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   *
   * insert into
   *   countries (id, name)
   * values
   *   (1, 'Mordor');
   * ```
   *
   * @exampleResponse Delete a record and return it
   * ```json
   * {
   *   "data": [
   *     {
   *       "id": 1,
   *       "name": "Mordor"
   *     }
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example Delete multiple records
   * ```ts
   * const response = await supabase
   *   .from('countries')
   *   .delete()
   *   .in('id', [1, 2, 3])
   * ```
   *
   * @exampleSql Delete multiple records
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   *
   * insert into
   *   countries (id, name)
   * values
   *   (1, 'Rohan'), (2, 'The Shire'), (3, 'Mordor');
   * ```
   *
   * @exampleResponse Delete multiple records
   * ```json
   * {
   *   "status": 204,
   *   "statusText": ""
   * }
   * ```
   */
  delete({
    count
  }?: {
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
  }): PostgrestFilterBuilder<ClientOptions, Schema, Relation$1['Row'], null, RelationName, Relationships, 'DELETE'>;
}
//#endregion
//#region src/types/common/rpc.d.ts
type IsMatchingArgs<FnArgs extends GenericFunction['Args'], PassedArgs extends GenericFunction['Args']> = [FnArgs] extends [Record<PropertyKey, never>] ? PassedArgs extends Record<PropertyKey, never> ? true : false : keyof PassedArgs extends keyof FnArgs ? PassedArgs extends FnArgs ? true : false : false;
type MatchingFunctionArgs<Fn$1 extends GenericFunction, Args extends GenericFunction['Args']> = Fn$1 extends {
  Args: infer A extends GenericFunction['Args'];
} ? IsMatchingArgs<A, Args> extends true ? Fn$1 : never : false;
type FindMatchingFunctionByArgs<FnUnion, Args extends GenericFunction['Args']> = FnUnion extends infer Fn extends GenericFunction ? MatchingFunctionArgs<Fn, Args> : false;
type TablesAndViews$1<Schema extends GenericSchema> = Schema['Tables'] & Exclude<Schema['Views'], ''>;
type UnionToIntersection<U> = (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;
type LastOf<T> = UnionToIntersection<T extends any ? () => T : never> extends (() => infer R) ? R : never;
type IsAny<T> = 0 extends 1 & T ? true : false;
type ExactMatch<T, S> = [T] extends [S] ? ([S] extends [T] ? true : false) : false;
type ExtractExactFunction<Fns, Args> = Fns extends infer F ? F extends GenericFunction ? ExactMatch<F['Args'], Args> extends true ? F : never : never : never;
type IsNever<T> = [T] extends [never] ? true : false;
type RpcFunctionNotFound<FnName> = {
  Row: any;
  Result: {
    error: true;
  } & "Couldn't infer function definition matching provided arguments";
  RelationName: FnName;
  Relationships: null;
};
type CrossSchemaError<TableRef extends string> = {
  error: true;
} & `Function returns SETOF from a different schema ('${TableRef}'). Use .overrideTypes<YourReturnType>() to specify the return type explicitly.`;
type GetRpcFunctionFilterBuilderByArgs<Schema extends GenericSchema, FnName extends string & keyof Schema['Functions'], Args> = {
  0: Schema['Functions'][FnName];
  1: IsAny<Schema> extends true ? any : IsNever<Args> extends true ? IsNever<ExtractExactFunction<Schema['Functions'][FnName], Args>> extends true ? LastOf<Schema['Functions'][FnName]> : ExtractExactFunction<Schema['Functions'][FnName], Args> : Args extends Record<PropertyKey, never> ? LastOf<Schema['Functions'][FnName]> : Args extends GenericFunction['Args'] ? IsNever<LastOf<FindMatchingFunctionByArgs<Schema['Functions'][FnName], Args>>> extends true ? LastOf<Schema['Functions'][FnName]> : LastOf<FindMatchingFunctionByArgs<Schema['Functions'][FnName], Args>> : ExtractExactFunction<Schema['Functions'][FnName], Args> extends GenericFunction ? ExtractExactFunction<Schema['Functions'][FnName], Args> : any;
}[1] extends infer Fn ? IsAny<Fn> extends true ? {
  Row: any;
  Result: any;
  RelationName: FnName;
  Relationships: null;
} : Fn extends GenericFunction ? {
  Row: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] extends keyof TablesAndViews$1<Schema> ? TablesAndViews$1<Schema>[Fn['SetofOptions']['to']]['Row'] : Fn['Returns'] extends any[] ? Fn['Returns'][number] extends Record<string, unknown> ? Fn['Returns'][number] : CrossSchemaError<Fn['SetofOptions']['to'] & string> : Fn['Returns'] extends Record<string, unknown> ? Fn['Returns'] : CrossSchemaError<Fn['SetofOptions']['to'] & string> : Fn['Returns'] extends any[] ? Fn['Returns'][number] extends Record<string, unknown> ? Fn['Returns'][number] : never : Fn['Returns'] extends Record<string, unknown> ? Fn['Returns'] : never;
  Result: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['isSetofReturn'] extends true ? Fn['SetofOptions']['isOneToOne'] extends true ? Fn['Returns'][] : Fn['Returns'] : Fn['Returns'] : Fn['Returns'];
  RelationName: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] : FnName;
  Relationships: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] extends keyof Schema['Tables'] ? Schema['Tables'][Fn['SetofOptions']['to']]['Relationships'] : Fn['SetofOptions']['to'] extends keyof Schema['Views'] ? Schema['Views'][Fn['SetofOptions']['to']]['Relationships'] : null : null;
} : Fn extends false ? RpcFunctionNotFound<FnName> : RpcFunctionNotFound<FnName> : RpcFunctionNotFound<FnName>;
//#endregion
//#region src/PostgrestClient.d.ts
/**
 * PostgREST client.
 *
 * @typeParam Database - Types for the schema from the [type
 * generator](https://supabase.com/docs/reference/javascript/next/typescript-support)
 *
 * @typeParam SchemaName - Postgres schema to switch to. Must be a string
 * literal, the same one passed to the constructor. If the schema is not
 * `"public"`, this must be supplied manually.
 */
declare class PostgrestClient<Database = any, ClientOptions extends ClientServerOptions = (Database extends {
  __InternalSupabase: infer I extends ClientServerOptions;
} ? I : {}), SchemaName extends string & keyof Omit<Database, '__InternalSupabase'> = ('public' extends keyof Omit<Database, '__InternalSupabase'> ? 'public' : string & keyof Omit<Database, '__InternalSupabase'>), Schema extends GenericSchema = (Omit<Database, '__InternalSupabase'>[SchemaName] extends GenericSchema ? Omit<Database, '__InternalSupabase'>[SchemaName] : any)> {
  url: string;
  headers: Headers;
  schemaName?: SchemaName;
  fetch?: Fetch;
  urlLengthLimit: number;
  retry?: boolean;
  /**
   * Creates a PostgREST client.
   *
   * @param url - URL of the PostgREST endpoint
   * @param options - Named parameters
   * @param options.headers - Custom headers
   * @param options.schema - Postgres schema to switch to
   * @param options.fetch - Custom fetch
   * @param options.timeout - Optional timeout in milliseconds for all requests. When set, requests will automatically abort after this duration to prevent indefinite hangs.
   * @param options.urlLengthLimit - Maximum URL length in characters before warnings/errors are triggered. Defaults to 8000.
   * @param options.retry - Enable or disable automatic retries for transient errors.
   *   When enabled, idempotent requests (GET, HEAD, OPTIONS) that fail with network
   *   errors or HTTP 503/520 responses will be automatically retried up to 3 times
   *   with exponential backoff (1s, 2s, 4s). Defaults to `true`.
   * @example Using supabase-js (recommended)
   * ```ts
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const { data, error } = await supabase.from('profiles').select('*')
   * ```
   *
   * @category Database
   *
   * @remarks
   * - A `timeout` option (in milliseconds) can be set to automatically abort requests that take too long.
   * - A `urlLengthLimit` option (default: 8000) can be set to control when URL length warnings are included in error messages for aborted requests.
   *
   * @example Standalone import for bundle-sensitive environments
   * ```ts
   * import { PostgrestClient } from '@supabase/postgrest-js'
   *
   * const postgrest = new PostgrestClient('https://xyzcompany.supabase.co/rest/v1', {
   *   headers: { apikey: 'your-publishable-key' },
   *   schema: 'public',
   *   timeout: 30000, // 30 second timeout
   * })
   * ```
   */
  constructor(url: string, {
    headers,
    schema,
    fetch,
    timeout,
    urlLengthLimit,
    retry
  }?: {
    headers?: HeadersInit;
    schema?: SchemaName;
    fetch?: Fetch;
    timeout?: number;
    urlLengthLimit?: number;
    retry?: boolean;
  });
  /**
   * Perform a query on a table or a view.
   *
   * @param relation - The table or view name to query
   *
   * @category Database
   */
  from<TableName$1 extends string & keyof Schema['Tables'], Table extends Schema['Tables'][TableName$1]>(relation: TableName$1): PostgrestQueryBuilder<ClientOptions, Schema, Table, TableName$1>;
  from<ViewName extends string & keyof Schema['Views'], View extends Schema['Views'][ViewName]>(relation: ViewName): PostgrestQueryBuilder<ClientOptions, Schema, View, ViewName>;
  /**
   * Select a schema to query or perform an function (rpc) call.
   *
   * The schema needs to be on the list of exposed schemas inside Supabase.
   *
   * @param schema - The schema to query
   *
   * @category Database
   */
  schema<DynamicSchema extends string & keyof Omit<Database, '__InternalSupabase'>>(schema: DynamicSchema): PostgrestClient<Database, ClientOptions, DynamicSchema, Database[DynamicSchema] extends GenericSchema ? Database[DynamicSchema] : any>;
  /**
   * Fetch the OpenAPI description PostgREST publishes for this client's schema.
   *
   * The document lists only the tables, views and functions the caller's role
   * holds privileges on; PostgREST applies that filtering server-side. The
   * schema is the one this client was created with, so call `.schema()` first
   * to describe a different one. Transient failures are retried according to
   * the client's `retry` option, like any other idempotent request.
   *
   * @example
   * ```ts
   * const { data, error } = await supabase.getOpenApiSpec()
   * ```
   *
   * @example Describe a schema other than the client default
   * ```ts
   * const { data, error } = await supabase.schema('billing').getOpenApiSpec()
   * ```
   *
   * @category Database
   */
  getOpenApiSpec(): Promise<PostgrestSingleResponse<PostgrestOpenApiSpec>>;
  /**
   * Perform a function call.
   *
   * @param fn - The function name to call
   * @param args - The arguments to pass to the function call
   * @param options - Named parameters
   * @param options.head - When set to `true`, `data` will not be returned.
   * Useful if you only need the count.
   * @param options.get - When set to `true`, the function will be called with
   * read-only access mode.
   * @param options.count - Count algorithm to use to count rows returned by the
   * function. Only applicable for [set-returning
   * functions](https://www.postgresql.org/docs/current/functions-srf.html).
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   *
   * @example
   * ```ts
   * // For cross-schema functions where type inference fails, use overrideTypes:
   * const { data } = await supabase
   *   .schema('schema_b')
   *   .rpc('function_a', {})
   *   .overrideTypes<{ id: string; user_id: string }[]>()
   * ```
   *
   * @category Database
   *
   * @example Call a Postgres function without arguments
   * ```ts
   * const { data, error } = await supabase.rpc('hello_world')
   * ```
   *
   * @exampleSql Call a Postgres function without arguments
   * ```sql
   * create function hello_world() returns text as $$
   *   select 'Hello world';
   * $$ language sql;
   * ```
   *
   * @exampleResponse Call a Postgres function without arguments
   * ```json
   * {
   *   "data": "Hello world",
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example Call a Postgres function with arguments
   * ```ts
   * const { data, error } = await supabase.rpc('echo', { say: '👋' })
   * ```
   *
   * @exampleSql Call a Postgres function with arguments
   * ```sql
   * create function echo(say text) returns text as $$
   *   select say;
   * $$ language sql;
   * ```
   *
   * @exampleResponse Call a Postgres function with arguments
   * ```json
   *   {
   *     "data": "👋",
   *     "status": 200,
   *     "statusText": "OK"
   *   }
   *
   * ```
   *
   * @exampleDescription Bulk processing
   * You can process large payloads by passing in an array as an argument.
   *
   * @example Bulk processing
   * ```ts
   * const { data, error } = await supabase.rpc('add_one_each', { arr: [1, 2, 3] })
   * ```
   *
   * @exampleSql Bulk processing
   * ```sql
   * create function add_one_each(arr int[]) returns int[] as $$
   *   select array_agg(n + 1) from unnest(arr) as n;
   * $$ language sql;
   * ```
   *
   * @exampleResponse Bulk processing
   * ```json
   * {
   *   "data": [
   *     2,
   *     3,
   *     4
   *   ],
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @exampleDescription Call a Postgres function with filters
   * Postgres functions that return tables can also be combined with [Filters](/docs/reference/javascript/using-filters) and [Modifiers](/docs/reference/javascript/using-modifiers).
   *
   * @example Call a Postgres function with filters
   * ```ts
   * const { data, error } = await supabase
   *   .rpc('list_stored_countries')
   *   .eq('id', 1)
   *   .single()
   * ```
   *
   * @exampleSql Call a Postgres function with filters
   * ```sql
   * create table
   *   countries (id int8 primary key, name text);
   *
   * insert into
   *   countries (id, name)
   * values
   *   (1, 'Rohan'),
   *   (2, 'The Shire');
   *
   * create function list_stored_countries() returns setof countries as $$
   *   select * from countries;
   * $$ language sql;
   * ```
   *
   * @exampleResponse Call a Postgres function with filters
   * ```json
   * {
   *   "data": {
   *     "id": 1,
   *     "name": "Rohan"
   *   },
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   *
   * @example Call a read-only Postgres function
   * ```ts
   * const { data, error } = await supabase.rpc('hello_world', undefined, { get: true })
   * ```
   *
   * @exampleSql Call a read-only Postgres function
   * ```sql
   * create function hello_world() returns text as $$
   *   select 'Hello world';
   * $$ language sql;
   * ```
   *
   * @exampleResponse Call a read-only Postgres function
   * ```json
   * {
   *   "data": "Hello world",
   *   "status": 200,
   *   "statusText": "OK"
   * }
   * ```
   */
  rpc<FnName extends string & keyof Schema['Functions'], Args extends Schema['Functions'][FnName]['Args'] = never, FilterBuilder extends GetRpcFunctionFilterBuilderByArgs<Schema, FnName, Args> = GetRpcFunctionFilterBuilderByArgs<Schema, FnName, Args>>(fn: FnName, args?: Args, {
    head,
    get,
    count
  }?: {
    head?: boolean;
    get?: boolean;
    count?: 'exact' | 'planned' | 'estimated' | (string & {});
  }): PostgrestFilterBuilder<ClientOptions, Schema, FilterBuilder['Row'], FilterBuilder['Result'], FilterBuilder['RelationName'], FilterBuilder['Relationships'], 'RPC'>;
}
//#endregion
//#region src/index.d.ts
declare const _default: {
  PostgrestClient: typeof PostgrestClient;
  PostgrestQueryBuilder: typeof PostgrestQueryBuilder;
  PostgrestFilterBuilder: typeof PostgrestFilterBuilder;
  PostgrestTransformBuilder: typeof PostgrestTransformBuilder;
  PostgrestBuilder: typeof PostgrestBuilder;
  PostgrestError: typeof PostgrestError;
};
//#endregion
export { PostgrestBuilder, PostgrestClient, type ClientServerOptions as PostgrestClientOptions, PostgrestError, PostgrestFilterBuilder, type PostgrestMaybeSingleResponse, type PostgrestOpenApiSpec, PostgrestQueryBuilder, type PostgrestResponse, type PostgrestResponseFailure, type PostgrestResponseSuccess, type PostgrestSingleResponse, PostgrestTransformBuilder, type GetResult as UnstableGetResult, _default as default };
//# sourceMappingURL=index.d.cts.map