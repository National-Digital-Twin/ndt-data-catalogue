/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Icon } from '@components';
import React from 'react';
import styled from 'styled-components';

const StyledIcon = styled(Icon)`
    flex-shrink: 0;

    &:hover {
        cursor: pointer;
    }
`;

interface Props {
    onClick?: () => void;
    className?: string;
}

export function RemoveIcon({ onClick, className }: Props) {
    return <StyledIcon source="phosphor" icon="Trash" onClick={onClick} size="lg" color="red" className={className} />;
}
