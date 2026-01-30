/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Drawer } from '@components';
import React from 'react';
import styled from 'styled-components';

import { DocumentHistoryTimeline } from '@app/entityV2/document/changeHistory/DocumentHistoryTimeline';

import { useGetDocumentChangeHistoryQuery } from '@graphql/document.generated';
import { DocumentChange } from '@types';

const DrawerContent = styled.div`
    display: flex;
    flex-direction: column;
    gap: 16px;
`;

interface DocumentChangeHistoryDrawerProps {
    urn: string;
    open: boolean;
    onClose: () => void;
}

export const DocumentChangeHistoryDrawer: React.FC<DocumentChangeHistoryDrawerProps> = ({ urn, open, onClose }) => {
    const { data, loading } = useGetDocumentChangeHistoryQuery({
        variables: {
            urn,
            limit: 100, // Fetch up to 100 most recent changes.
        },
        skip: !open, // Only fetch when drawer is open
        fetchPolicy: 'network-only', // Always fetch fresh data - important for real-time updates
    });

    const changes = (data?.document?.changeHistory || []) as DocumentChange[];

    return (
        <Drawer
            title="History"
            open={open}
            onClose={onClose}
            width={542}
            maskTransparent
            dataTestId="document-change-history"
        >
            <DrawerContent>
                <DocumentHistoryTimeline documentUrn={urn} changes={changes} loading={loading} />
            </DrawerContent>
        </Drawer>
    );
};
