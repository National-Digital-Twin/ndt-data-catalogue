/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { useAppConfig } from '@app/useAppConfig';

export function useFeatureFlag(featureFlagKey: string) {
    const appConfig = useAppConfig();

    const featureFlagValue = appConfig?.config?.featureFlags?.[featureFlagKey];

    if (appConfig.loaded) {
        setInLocalStorage(featureFlagKey, featureFlagValue);
        return featureFlagValue;
    }

    return loadFromLocalStorage(featureFlagKey);
}

export function setInLocalStorage(flagKey: string, value: boolean) {
    const rawValue = localStorage.getItem(flagKey);
    const storedValue = rawValue === null ? undefined : rawValue === 'true';

    if (rawValue === null || storedValue !== value) {
        saveToLocalStorage(flagKey, value);
    }
}

export function loadFromLocalStorage(flagKey: string): boolean {
    return localStorage.getItem(flagKey) === 'true';
}

function saveToLocalStorage(flagKey: string, value: boolean) {
    localStorage.setItem(flagKey, String(value));
}
