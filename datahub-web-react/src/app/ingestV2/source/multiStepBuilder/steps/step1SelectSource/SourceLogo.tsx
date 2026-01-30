/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Icon } from '@components';
import { Image } from 'antd';
import React from 'react';
import styled from 'styled-components';

import { CUSTOM } from '@app/ingestV2/source/builder/constants';
import useGetSourceLogoUrl from '@app/ingestV2/source/builder/useGetSourceLogoUrl';

const PlatformLogo = styled(Image)`
    max-height: 32px;
    height: 32px;
    width: auto;
    object-fit: contain;
    background-color: transparent;
    max-width: 32px;
    margin: 8px 0;
`;

const StyledIcon = styled(Icon)`
    margin: 6px 0;
`;

interface Props {
    sourceName: string;
}

export default function SourceLogo({ sourceName }: Props) {
    const logoUrl = useGetSourceLogoUrl(sourceName);

    let logoComponent;
    if (sourceName === CUSTOM) {
        logoComponent = <StyledIcon icon="NotePencil" source="phosphor" color="gray" />;
    }

    return logoUrl ? <PlatformLogo preview={false} src={logoUrl} alt={sourceName} /> : logoComponent || null;
}
