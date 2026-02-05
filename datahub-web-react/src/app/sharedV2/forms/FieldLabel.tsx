/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { QuestionCircleOutlined } from '@ant-design/icons';
import { Text, colors, typography } from '@components';
import { Tooltip } from 'antd';
import React from 'react';
import styled from 'styled-components';

const LabelContainer = styled.span`
    display: inline-flex;
    gap: 4px;
    align-items: center;
`;

const RequiredMark = styled.span`
    color: ${colors.red[1200]};
    font-family: ${typography.fonts.body};
`;

const TooltipIcon = styled(QuestionCircleOutlined)`
    cursor: pointer;
    svg {
        fill: ${colors.gray[1800]};
    }
`;

interface Props {
    label: string;
    required?: boolean;
    tooltip?: React.ReactNode;
    labelHelper?: React.ReactNode;
    className?: string;
}

export function FieldLabel({ label, required, tooltip, labelHelper, className }: Props) {
    return (
        <LabelContainer className={className}>
            <Text size="sm" weight="bold" color="gray" colorLevel={600}>
                {label}
            </Text>
            {required && <RequiredMark>*</RequiredMark>}
            {tooltip && (
                <Tooltip title={tooltip}>
                    <TooltipIcon />
                </Tooltip>
            )}
            {labelHelper}
        </LabelContainer>
    );
}
