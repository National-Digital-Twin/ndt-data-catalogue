/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { createGlobalStyle } from 'styled-components';

import { colors } from '@components/theme';

export const SelectCronGlobalStyles = createGlobalStyle`

    .react-js-cron-select-dropdown {

        .ant-select-item {
            color: ${colors.gray[500]};
            font-size: 14px;
            font-weight: 400;
        }
    }
`;
