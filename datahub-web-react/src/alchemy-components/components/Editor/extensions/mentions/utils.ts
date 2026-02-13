/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

/**
 * Dropdown placement threshold in pixels.
 * If less than this much space is available below the cursor, the dropdown will appear above.
 */
export const DROPDOWN_HEIGHT_THRESHOLD = 350;

/**
 * Calculates the optimal placement for the mentions dropdown based on cursor position.
 * Returns 'top-start' if there isn't enough space below the cursor, otherwise 'bottom-start'.
 *
 * @param cursorBottom - The bottom Y coordinate of the cursor in viewport pixels
 * @param viewportHeight - The height of the viewport (window.innerHeight)
 * @param threshold - Minimum space required below cursor (defaults to DROPDOWN_HEIGHT_THRESHOLD)
 * @returns 'top-start' or 'bottom-start'
 */
export function calculateMentionsPlacement(
    cursorBottom: number,
    viewportHeight: number,
    threshold: number = DROPDOWN_HEIGHT_THRESHOLD,
): 'top-start' | 'bottom-start' {
    const spaceBelow = viewportHeight - cursorBottom;
    return spaceBelow < threshold ? 'top-start' : 'bottom-start';
}
