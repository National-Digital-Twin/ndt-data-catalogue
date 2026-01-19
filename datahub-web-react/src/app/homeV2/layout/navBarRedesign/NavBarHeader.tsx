/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
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
