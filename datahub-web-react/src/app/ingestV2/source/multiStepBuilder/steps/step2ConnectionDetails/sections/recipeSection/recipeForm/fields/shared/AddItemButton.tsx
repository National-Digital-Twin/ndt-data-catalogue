/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Button, Icon, Text } from '@components';
import React from 'react';
import styled from 'styled-components';

export const CentredButton = styled(Button)`
    justify-content: center;
`;

interface Props {
    onClick: () => void;
    text?: string;
    className?: string;
}

export function AddItemButton({ onClick, text, className }: Props) {
    return (
        <CentredButton
            onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onClick();
            }}
            variant="text"
            type="button"
            size="xs"
            className={className}
        >
            <Icon source="phosphor" icon="Plus" size="lg" />
            <Text>{text}</Text>
        </CentredButton>
    );
}
