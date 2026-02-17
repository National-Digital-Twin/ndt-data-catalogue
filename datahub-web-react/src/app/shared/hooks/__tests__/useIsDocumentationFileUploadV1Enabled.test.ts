/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { renderHook } from '@testing-library/react-hooks';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { useIsDocumentationFileUploadV1Enabled } from '@app/shared/hooks/useIsDocumentationFileUploadV1Enabled';
import { useAppConfig } from '@app/useAppConfig';

vi.mock('@app/useAppConfig', () => ({
    useAppConfig: vi.fn(),
}));

describe('useIsDocumentationFileUploadV1Enabled', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should return value of documentationFileUploadV1 feature flag', () => {
        (useAppConfig as any).mockReturnValue({
            config: {
                featureFlags: {
                    documentationFileUploadV1: true,
                },
            },
        });

        const { result } = renderHook(() => useIsDocumentationFileUploadV1Enabled());
        expect(result.current).toBe(true);
    });
});
