/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

export interface ResizablePillsProps<T> {
    // Core
    items: T[];
    renderPill: (item: T, index: number) => React.ReactNode;
    getItemWidth: (item: T) => number;

    // Overflow handling (handled inside component)
    overflowTooltipContent?: (hiddenItems: T[]) => React.ReactNode;
    overflowLabel?: (count: number) => string;

    // Customization
    gap?: number;
    overflowButtonWidth?: number;
    minContainerWidthForOne?: number;

    // Styling
    className?: string;
    style?: React.CSSProperties;

    // Advanced
    keyExtractor?: (item: T) => string;
    debounceMs?: number;
}
