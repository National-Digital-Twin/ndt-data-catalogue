/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Entity, Owner } from '@types';

export function getOwnersChanges(owners: Entity[] | undefined, existingOwners: Owner[] | undefined) {
    // excluding `existingOwners` from `owners` to get only added owners
    const ownersToAdd: Entity[] = (owners ?? []).filter(
        (owner) => !(existingOwners ?? []).some((existingOwner) => existingOwner.owner.urn === owner.urn),
    );

    // excluding `owners` from `existingOwners` to get only removed owners
    const ownersToRemove: Owner[] = (existingOwners ?? []).filter(
        (existingOwner) => !owners?.some((owner) => existingOwner.owner.urn === owner.urn),
    );

    return { ownersToAdd, ownersToRemove };
}
