/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Text } from '@components';
import React from 'react';
import styled from 'styled-components';

const ContentContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 8px;
`;

export default function RegexTooltipContent() {
    return (
        <ContentContainer>
            <Text color="gray">Use fully qualified names based on your filter type.</Text>
            <Text color="gray" weight="semiBold">
                {' '}
                Examples:
            </Text>
            <Text color="gray">
                <ul>
                    <li>Exact: public.customers</li>
                    <li>Pattern: public.sales_.*</li>
                    <li>Multiple: public.orders, analytics.*</li>
                </ul>
                Separate entries with commas.
            </Text>
        </ContentContainer>
    );
}
