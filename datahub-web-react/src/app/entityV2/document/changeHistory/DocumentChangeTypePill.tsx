/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Pill } from '@components';
import React from 'react';

import { DocumentChangeType } from '@types';

interface DocumentChangeTypePillProps {
    changeType: DocumentChangeType;
}

const CHANGE_TYPE_LABELS: Record<DocumentChangeType, string> = {
    [DocumentChangeType.Created]: 'Created',
    [DocumentChangeType.TitleChanged]: 'Title Changed',
    [DocumentChangeType.TextChanged]: 'Content Changed',
    [DocumentChangeType.ParentChanged]: 'Moved',
    [DocumentChangeType.StateChanged]: 'State Changed',
    [DocumentChangeType.RelatedAssetsChanged]: 'Related Assets Updated',
    [DocumentChangeType.RelatedDocumentsChanged]: 'Related Documents Updated',
    [DocumentChangeType.Deleted]: 'Deleted',
};

const CHANGE_TYPE_COLORS: Record<DocumentChangeType, 'violet' | 'green' | 'blue' | 'yellow' | 'red'> = {
    [DocumentChangeType.Created]: 'green',
    [DocumentChangeType.TitleChanged]: 'blue',
    [DocumentChangeType.TextChanged]: 'blue',
    [DocumentChangeType.ParentChanged]: 'violet',
    [DocumentChangeType.StateChanged]: 'yellow',
    [DocumentChangeType.RelatedAssetsChanged]: 'violet',
    [DocumentChangeType.RelatedDocumentsChanged]: 'violet',
    [DocumentChangeType.Deleted]: 'red',
};

export const DocumentChangeTypePill: React.FC<DocumentChangeTypePillProps> = ({ changeType }) => {
    return (
        <Pill
            label={CHANGE_TYPE_LABELS[changeType] || changeType}
            color={CHANGE_TYPE_COLORS[changeType] || 'blue'}
            size="sm"
            clickable={false}
        />
    );
};
