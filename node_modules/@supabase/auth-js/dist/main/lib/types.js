"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SIGN_OUT_SCOPES = void 0;
const WeakPasswordReasons = ['length', 'characters', 'pwned'];
const AMRMethods = [
    'password',
    'otp',
    'oauth',
    'totp',
    'mfa/totp',
    'mfa/phone',
    'mfa/webauthn',
    'mfa/recovery_code',
    'anonymous',
    'sso/saml',
    'magiclink',
    'web3',
    'oauth_provider/authorization_code',
];
const FactorTypes = ['totp', 'phone', 'webauthn', 'recovery_code'];
const FactorVerificationStatuses = ['verified', 'unverified'];
const MFATOTPChannels = ['sms', 'whatsapp'];
exports.SIGN_OUT_SCOPES = ['global', 'local', 'others'];
//# sourceMappingURL=types.js.map