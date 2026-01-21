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

const typography = {
    letterSpacings: {
        tighter: '-2px',
        tight: '-1px',
        normal: '0',
        wide: '1px',
        wider: '2px',
        widest: '4px',
    },

    lineHeights: {
        normal: 'normal',
        none: 1,
        xs: '16px',
        sm: '20px',
        md: '24px',
        lg: '28px',
        xl: '32px',
        '2xl': '36px',
        '3xl': '40px',
        '4xl': '44px',
    },

    fontWeights: {
        normal: 400, // regular
        medium: 500,
        semiBold: 600,
        bold: 700,
    },

    fonts: {
        heading: `'Inter'`,
        body: `'Inter'`,
        mono: `SFMono-Regular, Menlo, Monaco, Consolas,
		'Liberation Mono', 'Courier New', monospace`,
    },

    fontSizes: {
        xs: '12.64px',
        sm: '14.2px',
        md: '16px', // default body text size
        lg: '18px',
        xl: '18px',
        '2xl': '20px',
        '3xl': '22px',
        '4xl': '24px',
    },
};

export default typography;
