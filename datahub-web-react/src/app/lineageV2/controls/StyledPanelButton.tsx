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
import { Button } from 'antd';
import styled from 'styled-components';

export const StyledPanelButton = styled(Button)`
    padding: 3px 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    height: 48px;
    margin: 0;

    &:hover {
        background-color: ${(props) => props.theme.styles['action-button-hover-color']};
    }
`;
