/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { DISMISSED_PRODUCT_UPDATES_KEY, SKIP_WELCOME_MODAL_KEY } from '@app/shared/constants';

/**
 * Check if the welcome modal has been dismissed/skipped by the user
 */
export function checkShouldSkipWelcomeModal(): boolean {
    return localStorage.getItem(SKIP_WELCOME_MODAL_KEY) === 'true';
}

/**
 * Mark the welcome modal as dismissed/skipped
 */
export function setSkipWelcomeModal(skip = true): void {
    localStorage.setItem(SKIP_WELCOME_MODAL_KEY, String(skip));
}

/**
 * Check if a specific product update has been dismissed
 * @deprecated Use server-side step state instead (see useIsProductAnnouncementVisible)
 */
export function checkProductUpdateDismissed(updateId: string): boolean {
    const dismissedUpdates = localStorage.getItem(DISMISSED_PRODUCT_UPDATES_KEY);
    if (!dismissedUpdates) return false;
    try {
        const dismissed: string[] = JSON.parse(dismissedUpdates);
        return dismissed.includes(updateId);
    } catch {
        return false;
    }
}

/**
 * Mark a product update as dismissed
 * @deprecated Use server-side step state instead (see useDismissProductAnnouncement)
 */
export function dismissProductUpdate(updateId: string): void {
    const dismissedUpdates = localStorage.getItem(DISMISSED_PRODUCT_UPDATES_KEY);
    let dismissed: string[] = [];
    if (dismissedUpdates) {
        try {
            dismissed = JSON.parse(dismissedUpdates);
        } catch {
            dismissed = [];
        }
    }
    if (!dismissed.includes(updateId)) {
        dismissed.push(updateId);
        localStorage.setItem(DISMISSED_PRODUCT_UPDATES_KEY, JSON.stringify(dismissed));
    }
}
