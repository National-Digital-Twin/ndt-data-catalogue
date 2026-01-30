/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useCallback } from 'react';

import { useUpdateOwners } from '@app/sharedV2/owners/useUpdateOwners';

import { useUpdateIngestionSourceMutation } from '@graphql/ingestion.generated';
import { Entity, Owner, UpdateIngestionSourceInput } from '@types';

export function useUpdateIngestionSource() {
    const [updateIngestionSource] = useUpdateIngestionSourceMutation();

    const updateOwners = useUpdateOwners();

    const updateSource = useCallback(
        async (sourceUrn: string, input: UpdateIngestionSourceInput, owners?: Entity[], existingOwners?: Owner[]) => {
            return new Promise<void>((resolve, reject) => {
                updateIngestionSource({ variables: { urn: sourceUrn, input } })
                    .then(() => {
                        updateOwners(owners, existingOwners, sourceUrn);
                        resolve();
                    })
                    .catch((e) => {
                        reject(new Error(`Failed to update ingestion source!: \n ${e.message || ''}`));
                    });
            });
        },
        [updateOwners, updateIngestionSource],
    );

    return updateSource;
}
