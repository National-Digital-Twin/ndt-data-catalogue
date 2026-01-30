/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { describe, expect, test } from 'vitest';

import { encodeSecret } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/utils';

describe('utils', () => {
    describe('encodeSecret', () => {
        test('should encode a secret name with the expected format', () => {
            const secretName = 'mySecret';
            // eslint-disable-next-line no-template-curly-in-string
            const expectedResult = '${mySecret}';

            const result = encodeSecret(secretName);

            expect(result).toBe(expectedResult);
        });

        test('should encode an empty string', () => {
            const secretName = '';
            // eslint-disable-next-line no-template-curly-in-string
            const expectedResult = '${}';

            const result = encodeSecret(secretName);

            expect(result).toBe(expectedResult);
        });

        test('should handle special characters in secret name', () => {
            const secretName = 'my-secret_value.123';
            // eslint-disable-next-line no-template-curly-in-string
            const expectedResult = '${my-secret_value.123}';

            const result = encodeSecret(secretName);

            expect(result).toBe(expectedResult);
        });
    });
});
