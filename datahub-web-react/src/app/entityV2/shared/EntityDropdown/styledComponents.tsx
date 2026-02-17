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

import { ANTD_GRAY, REDESIGN_COLORS } from '@app/entityV2/shared/constants';

const MenuItem = styled.div`
    font-size: 12px;
    padding: 0 4px;
    color: #262626;
`;

export const ActionMenuItem = styled(Button)<{ disabled?: boolean; fontSize?: number }>`
    flex-shrink: 0;
    width: ${(props) => (props.fontSize ? `${props.fontSize}px` : '28px')};
    height: ${(props) => (props.fontSize ? `${props.fontSize}px` : '28px')};
    padding: 0px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: none;
    background-color: 'white';
    border: 1px solid ${(props) => props.theme.styles['action-button-border-color']};
    color: ${(props) => props.theme.styles['action-button-text-color']};
    box-shadow: none;
    &&:hover {
        background-color: ${ANTD_GRAY[3]};
        color: ${(props) => props.theme.styles['action-button-focus-text-color']};
        border-color: ${(props) => props.theme.styles['action-button-focus-border-color']};
    }
    &&:focus {
        color: ${(props) => props.theme.styles['action-button-focus-text-color']};
        border-color: ${(props) => props.theme.styles['action-button-focus-border-color']};
    }
    ${(props) =>
        props.disabled
            ? `
            ${MenuItem} {
                color: ${ANTD_GRAY[7]};
            }
    `
            : ''};
`;
