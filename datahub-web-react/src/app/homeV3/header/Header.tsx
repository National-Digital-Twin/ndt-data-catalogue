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
import React from 'react';
import styled from 'styled-components';

import GreetingText from '@app/homeV3/header/components/GreetingText';
import { CenteredContainer, contentWidth } from '@app/homeV3/styledComponents';

export const HeaderWrapper = styled.div`
    display: flex;
    justify-content: center;
    padding: 27px 0 24px 0;
    width: 100%;
    border-radius: 12px 12px 0 0;
    position: relative;
`;

const StyledCenteredContainer = styled(CenteredContainer)`
    padding: 0 43px;
    ${contentWidth(0)}
`;

const Header = () => {
    return (
        <HeaderWrapper>
            <StyledCenteredContainer>
                <GreetingText />
            </StyledCenteredContainer>
        </HeaderWrapper>
    );
};

export default Header;
