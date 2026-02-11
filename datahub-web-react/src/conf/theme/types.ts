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
        'border-button-disabled'?: string;
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
        'accent-primary'?: string;
        'tab-control'?: string;
        'tab-control-selected'?: string;
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
