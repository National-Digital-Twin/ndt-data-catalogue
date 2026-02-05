/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { QuestionCircleOutlined } from '@ant-design/icons';
import { Icon, Text, spacing } from '@components';
import { Tooltip } from 'antd';
import React from 'react';
import styled from 'styled-components/macro';

const Container = styled.div`
    align-items: start;
    display: flex;
    flex-direction: row;
    gap: ${spacing.xsm};
`;

const IconWrapper = styled.div`
    margin-top: 3px;
`;

const CapabilityInfo = styled.div`
    display: flex;
    flex-direction: column;
`;

const StyledQuestion = styled(QuestionCircleOutlined)`
    color: rgba(0, 0, 0, 0.45);
    margin-left: 4px;
`;

interface Props {
    success: boolean;
    capability: string;
    displayMessage: string | null;
    tooltipMessage: string | null;
    number?: number;
}

export function ConnectionCapabilityView({ success, capability, displayMessage, tooltipMessage, number }: Props) {
    return (
        <Container>
            <IconWrapper>
                {success ? (
                    <Icon source="phosphor" icon="Check" size="2xl" color="green" colorLevel={1000} />
                ) : (
                    <Icon source="phosphor" icon="X" size="2xl" color="red" colorLevel={1000} />
                )}
            </IconWrapper>

            <CapabilityInfo>
                <Text>
                    {number && `${number}. `} {capability}
                </Text>
                <Text size="sm">
                    {displayMessage}
                    {tooltipMessage && (
                        <Tooltip overlay={tooltipMessage}>
                            <StyledQuestion />
                        </Tooltip>
                    )}
                </Text>
            </CapabilityInfo>
        </Container>
    );
}
