/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { AnchorHTMLAttributes } from 'react';

import type { ColorOptions, FontColorLevelOptions } from '@components/theme/config';

export interface LinkPropsDefaults {
    color: ColorOptions;
    colorLevel?: FontColorLevelOptions;
    target: string;
    rel: string;
}

export interface LinkProps extends Partial<LinkPropsDefaults>, Omit<AnchorHTMLAttributes<HTMLAnchorElement>, 'color'> {}

export interface LinkStyleProps {
    color: ColorOptions;
    colorLevel?: FontColorLevelOptions;
}
