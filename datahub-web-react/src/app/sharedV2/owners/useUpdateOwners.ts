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
import { useRemoveOwners } from '@app/sharedV2/owners/useRemoveOwners';
import { getOwnersChanges } from '@app/sharedV2/owners/utils';

import { Entity, Owner } from '@types';

export function useUpdateOwners() {
    const addOwners = useAddOwners();
    const removeOwners = useRemoveOwners();

    const updateOwners = useCallback(
        (owners: Entity[] | undefined, existingOwners: Owner[] | undefined, resourceUrn: string) => {
            const { ownersToAdd, ownersToRemove } = getOwnersChanges(owners, existingOwners);
            addOwners(ownersToAdd, resourceUrn);
            removeOwners(ownersToRemove, resourceUrn);
        },
        [addOwners, removeOwners],
    );

    return updateOwners;
}
