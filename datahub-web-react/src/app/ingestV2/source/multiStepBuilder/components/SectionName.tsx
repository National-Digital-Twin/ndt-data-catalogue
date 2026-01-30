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

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
`;

const TopRow = styled.div`
    display: flex;
    flex-direction: row;
    margin-top: 12px;
`;

const Spacer = styled.div`
    flex: 1;
`;

interface Props {
    name: string;
    description?: string;
    topRowRightItems?: React.ReactNode;
}

export function SectionName({ name, description, topRowRightItems }: Props) {
    return (
        <Wrapper>
            <TopRow>
                <Text weight="semiBold" size="lg">
                    {name}
                </Text>
                <Spacer />
                {topRowRightItems}
            </TopRow>
            {description && <Text color="gray">{description}</Text>}
        </Wrapper>
    );
}
