/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React from 'react';
import { Link } from 'react-router-dom';

import { getActorDisplayName, isSystemActor } from '@app/entityV2/document/changeHistory/utils/changeUtils';
import { Avatar } from '@src/alchemy-components';
import { HoverEntityTooltip } from '@src/app/recommendations/renderer/component/HoverEntityTooltip';
import { useEntityRegistryV2 } from '@src/app/useEntityRegistry';

import { DocumentChange } from '@types';

interface DocumentChangeTimelineDotProps {
    change: DocumentChange;
}

export const DocumentChangeTimelineDot: React.FC<DocumentChangeTimelineDotProps> = ({ change }) => {
    const entityRegistry = useEntityRegistryV2();
    const { actor } = change;

    if (!actor) {
        // If no actor, show a system icon or default avatar
        return <Avatar name="System" size="xl" />;
    }

    const avatarUrl = actor.editableProperties?.pictureLink || undefined;
    const actorName = getActorDisplayName(actor, entityRegistry);

    // For DataHub AI (system actor), use "AI" as the name to show "AI" initials
    const avatarName = isSystemActor(actor) ? 'AI' : actorName;

    return (
        <HoverEntityTooltip entity={actor} showArrow={false}>
            <Link to={`${entityRegistry.getEntityUrl(actor.type, actor.urn)}`}>
                <Avatar name={avatarName} imageUrl={avatarUrl} size="xl" />
            </Link>
        </HoverEntityTooltip>
    );
};
