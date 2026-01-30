/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import styled from 'styled-components';

import { LinkStyleProps } from '@components/components/Link/types';
import { getColor } from '@components/theme/utils';

export const StyledLink = styled.a<LinkStyleProps>`
    color: ${(props) => getColor(props.color, props.colorLevel)};
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.2s ease;

    &:hover {
        opacity: 0.8;
        text-decoration: underline;
    }

    &:active {
        opacity: 0.6;
    }
`;
