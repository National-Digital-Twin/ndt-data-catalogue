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

import WaffleButton from '@images/dt-waffle.svg?react';

const Container = styled.div`
    display: flex;
    width: 100%;
    height: 85px;
    min-height: 40px;
    align-items: center;
    gap: 8px;
    margin-left: 12px;
    transition: padding 250ms ease-in-out;
`;

export default function NavBarHeader() {
    return (
        <Container>
            <WaffleButton width={32} height={32} />
        </Container>
    );
}
