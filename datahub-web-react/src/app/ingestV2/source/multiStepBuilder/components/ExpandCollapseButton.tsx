/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Button, Icon } from '@components';
import React from 'react';

interface Props {
    expanded?: boolean;
    onToggle?: () => void;
}

export function ExpandCollapseButton({ expanded, onToggle }: Props) {
    return (
        <Button variant="link" color="gray" onClick={onToggle}>
            <Icon
                source="phosphor"
                icon={expanded ? 'CaretDown' : 'CaretRight'}
                size="2xl"
                color="gray"
                colorLevel={1800}
            />
        </Button>
    );
}
