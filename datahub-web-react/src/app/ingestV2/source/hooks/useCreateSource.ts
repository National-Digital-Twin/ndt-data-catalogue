/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useCallback } from 'react';

import { useAddOwners } from '@app/sharedV2/owners/useAddOwners';

import { useCreateIngestionSourceMutation } from '@graphql/ingestion.generated';
import { Entity, UpdateIngestionSourceInput } from '@types';

export function useCreateSource() {
    const [createIngestionSource] = useCreateIngestionSourceMutation();

    const addOwners = useAddOwners();

    const createSource = useCallback(
        async (input: UpdateIngestionSourceInput, owners?: Entity[]): Promise<string | undefined> => {
            return new Promise((resolve, reject) => {
                createIngestionSource({ variables: { input } })
                    .then((result) => {
                        const newSourceUrn = result?.data?.createIngestionSource;
                        if (newSourceUrn) {
                            addOwners(owners, newSourceUrn);
                            resolve(newSourceUrn);
                        } else {
                            reject(new Error('Failed to create ingestion source!'));
                        }
                    })
                    .catch((e) => {
                        reject(new Error(`Failed to create ingestion source!: \n ${e.message || ''}`));
                    });
            });
        },
        [addOwners, createIngestionSource],
    );

    return createSource;
}
