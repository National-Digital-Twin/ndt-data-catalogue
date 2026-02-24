/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { renderHook } from '@testing-library/react-hooks';
import React from 'react';
import { describe, expect, it } from 'vitest';

import { useHideLineageInSearchCards } from '@app/useAppConfig';
import { AppConfigContext } from '@src/appConfigContext';

import type { AppConfig } from '@types';

describe('useHideLineageInSearchCards', () => {
    const createWrapper = (config: Partial<AppConfig>) => {
        const appConfigValue = {
            loaded: true,
            config: config as AppConfig,
            refreshContext: () => null,
        };

        return ({ children }: { children: React.ReactNode }) => (
            <AppConfigContext.Provider value={appConfigValue}>{children}</AppConfigContext.Provider>
        );
    };

    it('should return true when feature flag is enabled', () => {
        const wrapper = createWrapper({
            featureFlags: { hideLineageInSearchCards: true },
        } as Partial<AppConfig>);

        const { result } = renderHook(() => useHideLineageInSearchCards(), { wrapper });
        expect(result.current).toBe(true);
    });

    it('should return false when feature flag is disabled', () => {
        const wrapper = createWrapper({
            featureFlags: { hideLineageInSearchCards: false },
        } as Partial<AppConfig>);

        const { result } = renderHook(() => useHideLineageInSearchCards(), { wrapper });
        expect(result.current).toBe(false);
    });

    it('should return undefined when feature flag is not set', () => {
        const wrapper = createWrapper({
            featureFlags: {},
        } as Partial<AppConfig>);

        const { result } = renderHook(() => useHideLineageInSearchCards(), { wrapper });
        expect(result.current).toBeUndefined();
    });
});
