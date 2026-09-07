import { expect } from 'vitest';
import { e as extensions } from './matchers-b01dabb1.mjs';
import '@testing-library/dom';
import 'redent';
import '@adobe/css-tools';
import 'dom-accessibility-api';
import 'aria-query';
import 'picocolors';
import 'css.escape';

/* istanbul ignore file */


expect.extend(extensions);
