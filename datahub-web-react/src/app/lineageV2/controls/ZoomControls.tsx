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
import React from 'react';
import { Panel, useReactFlow } from 'reactflow';
import styled from 'styled-components';

import { TRANSITION_DURATION_MS } from '@app/lineageV2/common';

import ZoomInIcon from '@images/dt-zoom-in.svg?react';
import ZoomOutIcon from '@images/dt-zoom-out.svg?react';

const StyledZoomButton = styled(Button)`
    border-radius: 4px;
    border: 1px solid ${(props) => props.theme.styles['action-button-border-color']};
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.16);
    height: 48px;
    width: 48px;
    margin-bottom: 8px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    display: flex;
    &:focus {
        border-color: #00000015;
    }
    &:hover {
        background-color: ${(props) => props.theme.styles['action-button-hover-color']};
        border: 1px solid ${(props) => props.theme.styles['action-button-border-color']};
    }
`;

const ZoomControls: React.FC = () => {
    const { zoomIn, zoomOut } = useReactFlow();

    return (
        <Panel position="bottom-left">
            <StyledZoomButton tabIndex={-1} onClick={() => zoomIn({ duration: TRANSITION_DURATION_MS })}>
                <ZoomInIcon />
            </StyledZoomButton>
            <StyledZoomButton tabIndex={-1} onClick={() => zoomOut({ duration: TRANSITION_DURATION_MS })}>
                <ZoomOutIcon />
            </StyledZoomButton>
        </Panel>
    );
};

export default ZoomControls;
