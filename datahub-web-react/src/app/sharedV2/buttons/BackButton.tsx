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
import { Tooltip } from '@components';
import KeyboardBackspaceIcon from '@mui/icons-material/KeyboardBackspace';
import { Button } from 'antd';
import React from 'react';
import styled from 'styled-components';

const StyledButton = styled(Button)`
    height: 25px;
    width: 25px;
    color: ${(props) => props.theme.styles['action-button-text-color']};
    padding: 0px;
    border-radius: 20px;
    border: 1px solid ${(props) => props.theme.styles['action-button-border-color']};
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: -4px;
    margin-right: 10px;
    margin-top: 2px;

    &:hover {
        background-color: ${(p) => p.theme.styles['action-button-hover-color']};
        color: ${(props) => props.theme.styles['action-button-focus-text-color']};
        border-color: ${(props) => props.theme.styles['action-button-focus-border-color']};
    }
`;

const StyledLeftOutlined = styled(KeyboardBackspaceIcon)`
    && {
        font-size: 20px;
        margin: 0px;
        padding 0px;
    }
`;

interface Props {
    onGoBack?: () => void;
}

export const BackButton = ({ onGoBack }: Props) => {
    return (
        <Tooltip title="Go back" showArrow={false} placement="bottom">
            <StyledButton onClick={onGoBack}>
                <StyledLeftOutlined />
            </StyledButton>
        </Tooltip>
    );
};
