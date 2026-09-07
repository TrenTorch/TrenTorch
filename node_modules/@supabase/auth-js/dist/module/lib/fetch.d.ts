import { AuthResponse, AuthResponsePassword, SSOResponse, GenerateLinkProperties, GenerateLinkResponse, User, UserResponse, WeakPassword } from './types';
export type Fetch = typeof fetch;
/** Raw session data from GoTrue server response. */
interface GoTrueSessionData {
    access_token?: string;
    refresh_token?: string;
    expires_in?: number;
    expires_at?: number;
    user?: User;
    [key: string]: any;
}
/** Raw session data that includes weak password info (password sign-in endpoints). */
interface GoTrueSessionPasswordData extends GoTrueSessionData {
    weak_password?: WeakPassword;
}
/** Raw user data — either `{ user: User }` or the User object itself. */
interface GoTrueUserData {
    user?: User;
    [key: string]: any;
}
/** Raw generate-link data — link properties + User fields flattened into one object. */
type GoTrueGenerateLinkData = GenerateLinkProperties & Record<string, any>;
export interface FetchOptions {
    headers?: {
        [key: string]: string;
    };
    noResolveJson?: boolean;
}
export interface FetchParameters {
    signal?: AbortSignal;
}
export type RequestMethodType = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
export declare function handleError(error: unknown): Promise<void>;
interface GotrueRequestOptions extends FetchOptions {
    jwt?: string;
    redirectTo?: string;
    body?: object;
    query?: {
        [key: string]: string;
    };
    /**
     * Function that transforms api response from gotrue into a desirable / standardised format
     */
    xform?: (data: any) => any;
}
export declare function _request(fetcher: Fetch, method: RequestMethodType, url: string, options?: GotrueRequestOptions): Promise<any>;
export declare function _sessionResponse(data: GoTrueSessionData): AuthResponse;
export declare function _sessionResponsePassword(data: GoTrueSessionPasswordData): AuthResponsePassword;
export declare function _userResponse(data: GoTrueUserData): UserResponse;
export declare function _ssoResponse(data: Record<string, any>): SSOResponse;
export declare function _generateLinkResponse(data: GoTrueGenerateLinkData): GenerateLinkResponse;
export declare function _noResolveJsonResponse(data: Response): Response;
export {};
//# sourceMappingURL=fetch.d.ts.map