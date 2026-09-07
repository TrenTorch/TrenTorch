export type Msg<T> = {
    join_ref?: string | null;
    ref?: string | null;
    topic: string;
    event: string;
    payload: T;
};
export default class Serializer {
    HEADER_LENGTH: number;
    USER_BROADCAST_PUSH_META_LENGTH: number;
    KINDS: {
        userBroadcastPush: number;
        userBroadcast: number;
    };
    BINARY_ENCODING: number;
    JSON_ENCODING: number;
    BROADCAST_EVENT: string;
    allowedMetadataKeys: string[];
    constructor(allowedMetadataKeys?: string[] | null);
    encode(msg: Msg<{
        [key: string]: any;
    }>, callback: (result: ArrayBuffer | string) => any): any;
    private _binaryEncodeUserBroadcastPush;
    private _encodeBinaryUserBroadcastPush;
    private _encodeJsonUserBroadcastPush;
    private _encodeUserBroadcastPush;
    decode(rawPayload: ArrayBuffer | string, callback: Function): any;
    private _binaryDecode;
    private _decodeUserBroadcast;
    private _isArrayBuffer;
    private _pick;
}
//# sourceMappingURL=serializer.d.ts.map