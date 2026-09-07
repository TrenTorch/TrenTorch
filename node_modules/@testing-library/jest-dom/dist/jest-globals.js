'use strict';

var globals = require('@jest/globals');
var matchers = require('./matchers-3ed9c960.js');
require('@testing-library/dom');
require('redent');
require('@adobe/css-tools');
require('dom-accessibility-api');
require('aria-query');
require('picocolors');
require('css.escape');

/* istanbul ignore file */


globals.expect.extend(matchers.extensions);
