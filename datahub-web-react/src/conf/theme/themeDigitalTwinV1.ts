/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Theme } from '@conf/theme/types';
import digitalTwinColours from './colorThemes/digitalTwin';

const themeDigitalTwinV1: Theme = {
    id: 'themeDigitalTwinV1',
    colors: digitalTwinColours,
    styles: {
        'primary-color': '#533FD1',
        'primary-color-dark': '#5C3FD1',
        'primary-color-light': '#ece9f8',
        'layout-header-color': '#434343',
        'body-background': `linear-gradient(180deg, ${digitalTwinColours.bgGradientTop} 0%, ${digitalTwinColours.bgGradientBottom} 100%)`,
        'content-background': digitalTwinColours.bg,
        'border-color-base': '#ececec',
        'homepage-background-upper-fade': '#FFFFFF',
        'homepage-background-lower-fade': '#FFFFFF',
        'homepage-text-color': '#434343',
        'box-shadow': '0px 0px 30px 0px rgb(239 239 239)',
        'box-shadow-hover': '0px 1px 0px 0.5px rgb(239 239 239)',
        'box-shadow-navbar-redesign': '0 0 6px 0px rgba(93, 102, 139, 0.20)',
        'border-radius-navbar-redesign': '12px',
        'highlight-color': '#ece9f8',
        'highlight-border-color': '#07878180',
        'nav-item-text': digitalTwinColours.navItemText,
        'nav-item-hover': digitalTwinColours.navItemHover,
        'icon-selected': digitalTwinColours.iconSelected,
        'logo-text-size': '24px',

    },
    assets: {
        logoUrl: 'assets/logos/data-catalogue-logo.png',
    },
    content: {
        title: 'Digital Twin Data Catalogue',
        search: {
            searchbarMessage: 'Find tables, dashboards, people, and more',
        },
        menu: {
            items: [
                {
                    label: 'DataHub Project',
                    path: 'https://docs.datahub.com',
                    shouldOpenInNewTab: true,
                    description: 'Explore DataHub Project website',
                },
                {
                    label: 'DataHub GitHub',
                    path: 'https://github.com/linkedin/datahub',
                    shouldOpenInNewTab: true,
                },
            ],
        },
    },
};

export default themeDigitalTwinV1;
