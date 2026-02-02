/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { useCallback } from 'react';

import { useBatchRemoveOwnersMutation } from '@graphql/mutations.generated';
import { Owner } from '@types';

export function useRemoveOwners() {
    const [batchRemoveOwnersMutation] = useBatchRemoveOwnersMutation();

    const removeOwners = useCallback(
        (owners: Owner[] | undefined, resourceUrn: string) => {
            const ownersToRemoveUrns: string[] = owners?.map((owner) => owner.owner.urn) || [];

            if (ownersToRemoveUrns?.length) {
                batchRemoveOwnersMutation({
                    variables: {
                        input: {
                            ownerUrns: ownersToRemoveUrns,
                            resources: [{ resourceUrn }],
                        },
                    },
                });
            }
        },
        [batchRemoveOwnersMutation],
    );

    return removeOwners;
}
