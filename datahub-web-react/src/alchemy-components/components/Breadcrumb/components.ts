/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Divider } from 'antd';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

import { Text } from '@components/components/Text';
import { colors } from '@components/theme';

export const Wrapper = styled.nav`
    display: flex;
    align-items: center;
    gap: 4px;
`;

export const BreadcrumbItemContainer = styled.span`
    display: flex;
    align-items: center;
    gap: 4px;
`;

export const BreadcrumbLink = styled(Link)<{ $isCurrent?: boolean }>`
    color: ${(props) => (props.$isCurrent ? colors.gray[600] : colors.gray[1800])};
    font-size: 12px;
    text-decoration: none;
    cursor: pointer;
`;

export const BreadcrumbButton = styled(Text)<{ $isCurrent?: boolean }>`
    cursor: pointer;
    color: ${(props) => (props.$isCurrent ? colors.gray[600] : colors.gray[1800])};

    :hover {
        color: ${colors.primary[500]};
    }
`;

export const VerticalDivider = styled(Divider)`
    color: ${colors.gray[100]};
    height: 16px;
    width: 2px;
    margin: 0 4px;
`;
