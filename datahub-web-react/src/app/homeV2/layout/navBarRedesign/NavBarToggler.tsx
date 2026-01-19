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
import { Sidebar } from '@phosphor-icons/react';
import React from 'react';
import styled from 'styled-components';

import { useNavBarContext } from '@app/homeV2/layout/navBarRedesign/NavBarContext';
import { colors } from '@src/alchemy-components';
import analytics, { EventType } from '@src/app/analytics';

const Toggler = styled.button<{ $isCollapsed?: boolean }>`
    cursor: pointer;
    margin: 0 0 0 0;
    padding: 4px;
    border-radius: 6px;
    border: none;
    display: flex;
    transition: background 300ms ease-in;
    background: transparent;

    & svg {
        height: 24px;
        width: 24px;
        color: ${colors.gray[1800]};
        transition: color 200ms ease-in-out;

        &:hover {
            color: white;
    }
`;

export default function NavBarToggler() {
    const { toggle, isCollapsed } = useNavBarContext();

    function handleToggle() {
        analytics.event({ type: EventType.NavBarExpandCollapse, isExpanding: isCollapsed });
        toggle();
    }

    return (
        <Toggler onClick={handleToggle} aria-label="Navbar toggler">
            <Sidebar />
        </Toggler>
    );
}
