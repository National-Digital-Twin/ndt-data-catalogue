/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Button, Card } from '@components';
import React from 'react';
import styled from 'styled-components';

import { SourceConfig } from '@app/ingestV2/source/builder/types';
import SourceLogo from '@app/ingestV2/source/multiStepBuilder/steps/step1SelectSource/SourceLogo';
import { CARD_HEIGHT, CARD_WIDTH } from '@app/ingestV2/source/multiStepBuilder/steps/step1SelectSource/utils';

const CardContentWrapper = styled.div`
    display: flex;
    gap: 16px;
    align-items: center;
    justify-content: space-between;
`;

const LogosContainer = styled.div`
    display: flex;
    gap: 8px;
    align-items: center;
`;

const ButtonContainer = styled.div`
    display: flex;
`;

const cardStyles = {
    justifyContent: 'center',
};

interface Props {
    hiddenSources: SourceConfig[];
    onShowAll: () => void;
}

export default function ShowAllCard({ hiddenSources, onShowAll }: Props) {
    const firstSixSources = hiddenSources.slice(0, 5);

    return (
        <Card height={`${CARD_HEIGHT}px`} width={`${CARD_WIDTH}px`} style={cardStyles}>
            <CardContentWrapper>
                <LogosContainer>
                    {firstSixSources.map((source) => (
                        <SourceLogo sourceName={source.name} />
                    ))}
                </LogosContainer>
                <ButtonContainer>
                    <Button variant="outline" size="xs" onClick={onShowAll}>
                        Show All
                    </Button>
                </ButtonContainer>
            </CardContentWrapper>
        </Card>
    );
}
