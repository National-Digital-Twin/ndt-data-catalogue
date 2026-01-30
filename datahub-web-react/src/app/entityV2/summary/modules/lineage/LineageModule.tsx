/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React from 'react';
import { useHistory } from 'react-router';

import { useEntityData } from '@app/entity/shared/EntityContext';
import LargeModule from '@app/homeV3/module/components/LargeModule';
import { ModuleProps } from '@app/homeV3/module/types';
import LineageExplorer from '@app/lineageV3/LineageExplorer';
import LineageGraphContext from '@app/lineageV3/LineageGraphContext';
import { useEntityRegistryV2 } from '@app/useEntityRegistry';

export default function LineageModule(props: ModuleProps) {
    const { urn, entityType } = useEntityData();
    const history = useHistory();
    const entityRegistry = useEntityRegistryV2();

    const navigateToLineageTab = () => {
        history.push(`${entityRegistry.getEntityUrl(entityType, urn)}/Lineage`);
    };
    return (
        <LargeModule
            {...props}
            onClickViewAll={navigateToLineageTab}
            viewAllText="View All in Lineage"
            dataTestId="lineage-module"
        >
            <LineageGraphContext.Provider value={{ isDAGView: false, isModuleView: true }}>
                <LineageExplorer urn={urn} type={entityType} />
            </LineageGraphContext.Provider>
        </LargeModule>
    );
}
