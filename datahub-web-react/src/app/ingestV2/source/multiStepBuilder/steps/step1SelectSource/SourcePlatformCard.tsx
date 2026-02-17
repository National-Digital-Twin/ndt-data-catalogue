/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Card, Pill } from '@components';
import React from 'react';

import { SourceConfig } from '@app/ingestV2/source/builder/types';
import SourceLogo from '@app/ingestV2/source/multiStepBuilder/steps/step1SelectSource/SourceLogo';
import {
    CARD_HEIGHT,
    CARD_WIDTH,
    PillLabel,
    getPillLabel,
} from '@app/ingestV2/source/multiStepBuilder/steps/step1SelectSource/utils';

const logoStyles = {
    alignSelf: 'start',
};

interface Props {
    source: SourceConfig;
    onSelect: (platform: SourceConfig) => void;
}

export default function SourcePlatformCard({ source, onSelect }: Props) {
    const pillLabel = getPillLabel(source);
    return (
        <Card
            title={source.displayName}
            subTitle={source.description}
            icon={<SourceLogo sourceName={source.name} />}
            height={`${CARD_HEIGHT}px`}
            width={`${CARD_WIDTH}px`}
            noOfSubtitleLines={2}
            iconAlignment="horizontal"
            iconStyles={logoStyles}
            pill={
                pillLabel && (
                    <Pill
                        label={pillLabel}
                        size="sm"
                        color={pillLabel === PillLabel.New ? 'blue' : 'primary'}
                        clickable={false}
                        variant={pillLabel === PillLabel.External ? 'outline' : 'filled'}
                    />
                )
            }
            onClick={() => onSelect(source)}
            isCardClickable
        />
    );
}
