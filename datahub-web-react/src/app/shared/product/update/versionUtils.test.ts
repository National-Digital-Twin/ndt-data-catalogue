/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { isVersionMatch } from '@app/shared/product/update/versionUtils';

describe('isVersionMatch', () => {
    it('returns true for exact version match', () => {
        expect(isVersionMatch('v1.4.0', 'v1.4.0')).toBe(true);
        expect(isVersionMatch('1.3.15', '1.3.15')).toBe(true);
    });

    it('returns true for exact match with different prefix styles', () => {
        expect(isVersionMatch('1.4.0', 'v1.4.0')).toBe(true);
        expect(isVersionMatch('v1.4.0', '1.4.0')).toBe(true);
    });

    it('returns false for version mismatch', () => {
        expect(isVersionMatch('v1.3.10', 'v1.3.15')).toBe(false);
        expect(isVersionMatch('v1.4.0', 'v1.3.15')).toBe(false);
        expect(isVersionMatch('v2.0.0', 'v1.4.0')).toBe(false);
    });

    it('returns true when no required version is specified', () => {
        expect(isVersionMatch('v1.0.0', null)).toBe(true);
        expect(isVersionMatch('v1.0.0', undefined)).toBe(true);
        expect(isVersionMatch('v1.0.0', '')).toBe(true);
        expect(isVersionMatch('v1.0.0', 'null')).toBe(true);
    });

    it('returns false when no current version is available', () => {
        expect(isVersionMatch(null, 'v1.0.0')).toBe(false);
        expect(isVersionMatch(undefined, 'v1.0.0')).toBe(false);
        expect(isVersionMatch('', 'v1.0.0')).toBe(false);
    });

    it('handles whitespace in version strings', () => {
        expect(isVersionMatch(' v1.4.0 ', 'v1.4.0')).toBe(true);
        expect(isVersionMatch('v1.4.0', ' 1.4.0 ')).toBe(true);
    });

    it('returns false for different major versions', () => {
        expect(isVersionMatch('v2.0.0', 'v1.0.0')).toBe(false);
    });

    it('returns false for different minor versions', () => {
        expect(isVersionMatch('v1.5.0', 'v1.4.0')).toBe(false);
    });

    it('returns false for different patch versions', () => {
        expect(isVersionMatch('v1.4.1', 'v1.4.0')).toBe(false);
    });
});
