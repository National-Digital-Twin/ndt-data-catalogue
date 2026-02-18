/*
 * SPDX-License-Identifier: Apache-2.0

 * Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced, and maintained by
 * the National Digital Twin Programme.
 *
 * Modifications made by the National Digital Twin Programme (NDTP)
 * © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
 * and is legally attributed to the Department for Business and Trade (UK) as the governing
 * entity.
 */
import ColorTheme from '@conf/theme/colorThemes/types';

export type Theme = {
    id: string;
    colors: ColorTheme & {
        glossaryPalette?: string[];
        domainPalette?: string[];
    };
    styles: {
        'primary-color': string;
        'primary-color-light': string;
        'primary-color-dark': string;
        'layout-header-color': string;
        'body-background': string;
        'content-background'?: string;
        'border-color-base': string;
        'homepage-background-upper-fade': string;
        'homepage-background-lower-fade': string;
        'homepage-text-color': string;
        'box-shadow': string;
        'box-shadow-hover': string;
        'box-shadow-navbar-redesign': string;
        'border-radius-navbar-redesign': string;
        'highlight-color': string;
        'highlight-border-color': string;
        'layout-header-background'?: string;
        'layout-body-background'?: string;
        'component-background'?: string;
        'text-color'?: string;
        'text-color-secondary'?: string;
        'logo-text-size'?: string;
        'heading-color'?: string;
        'background-color-light'?: string;
        'divider-color'?: string;
        'disabled-color'?: string;
        'steps-nav-arrow-color'?: string;
        'nav-item-text'?: string;
        'nav-item-hover'?: string;
        'icon-selected'?: string;

        // Solid Buttons
        'solid-button-bg-color'?: string;
        'solid-button-text-color'?: string;
        'solid-button-hover-color'?: string;

        // Outline/No Outline Buttons
        'outline-button-text-color'?: string;
        'outline-button-border-color'?: string;
        'outline-button-hover-text-color'?: string;
        'outline-button-hover-border-color'?: string;

        // Segmented Button
        'segmented-button-text-color'?: string;
        'segmented-button-border-color'?: string;
        'segmented-button-hover-color'?: string;
        'segmented-button-focus-border-color'?: string;
        'segmented-button-selected-bg-color'?: string;
        'segmented-button-selected-text-color'?: string;

        // Action Button
        'action-button-text-color'?: string;
        'action-button-border-color'?: string;
        'action-button-hover-color'?: string;
        'action-button-focus-border-color'?: string;
        'action-button-focus-text-color'?: string;

        // Toggle
        'toggle-off-bg-color'?: string;
        'toggle-off-dot-color'?: string;
        'toggle-on-bg-color'?: string;
        'toggle-on-dot-color'?: string;
        'toggle-label-color'?: string;

        // Tabs
        'tab-text-color'?: string;
        'tab-hover-bg-color'?: string;
        'tab-selected-text-color'?: string;
        'tab-hover-underline-color'?: string;
        'tab-selected-underline-color'?: string;

        // Lineage
        'lineage-arrow-icon-color'?: string;
        'lineage-arrow-hover-bg-color'?: string;
        'lineage-arrow-border-color'?: string;
        'lineage-node-border-color'?: string;
        'lineage-node-title-color'?: string;
        'lineage-node-selected-border-color'?: string;
        'columns-button-text-color'?: string;
        'columns-button-hover-color'?: string;
        'lineage-home-badge-bg-color'?: string;
        'lineage-home-badge-text-color'?: string;

        // Dropdown
        'dropdown-menu-item-text-color'?: string;
        'dropdown-menu-item-hover-color'?: string;

        // Search
        'search-bar-border-color'?: string;
        'search-bar-hover-border-color'?: string;
        'search-bar-focus-border-color'?: string;

        // Pagination
        'pagination-text-color'?: string;
        'pagination-hover-bg-color'?: string;
        'pagination-selected-bg-color'?: string;
        'pagination-selected-text-color'?: string;
        'pagination-disabled-text-color'?: string;

        // Chips
        'action-chip-border-color'?: string;
        'action-chip-hover-border-color'?: string;
        'action-chip-hover-bg-color'?: string;
        'action-chip-text-color'?: string;
        'filter-chip-bg-color'?: string;
        'filter-chip-text-color'?: string;
    };
    assets: {
        logoUrl: string;
    };
    content: {
        title: string;
        subtitle?: string;
        search: {
            searchbarMessage: string;
        };
        menu: {
            items: {
                label: string;
                path: string;
                shouldOpenInNewTab: boolean;
                description?: string;
            }[];
        };
    };
};
