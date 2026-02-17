/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React, { useCallback, useMemo } from 'react';

import { ActorsSearchSelect } from '@app/entityV2/shared/EntitySearchSelect/ActorsSearchSelect';
import { ActorEntity } from '@app/entityV2/shared/utils/actorUtils';
import { FieldWrapper } from '@app/ingestV2/source/multiStepBuilder/components/FieldWrapper';

interface Props {
    label: string;
    ownerUrns?: string[];
    updateOwners?: (owners: ActorEntity[]) => void;
    defaultActors?: ActorEntity[];
}

export function ActorsField({ label, ownerUrns, updateOwners, defaultActors }: Props) {
    const urns = useMemo(() => ownerUrns ?? [], [ownerUrns]);
    const onUpdate = useCallback((owners: ActorEntity[]) => updateOwners?.(owners), [updateOwners]);

    return (
        <FieldWrapper label={label}>
            <ActorsSearchSelect
                selectedActorUrns={urns}
                onUpdate={onUpdate}
                placeholder="Search for users or groups"
                defaultActors={defaultActors}
            />
        </FieldWrapper>
    );
}
