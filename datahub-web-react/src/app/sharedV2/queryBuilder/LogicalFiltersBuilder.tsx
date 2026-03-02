/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React from 'react';

import QueryBuilder from '@app/sharedV2/queryBuilder/QueryBuilder';
import { Property } from '@app/sharedV2/queryBuilder/builder/property/types/properties';
import { LogicalPredicate, PropertyPredicate } from '@app/sharedV2/queryBuilder/builder/types';

interface Props {
    filters: LogicalPredicate | PropertyPredicate;
    onChangeFilters: (newPredicate?: LogicalPredicate) => void;
    properties: Property[];
    /** When true, hides the "Add Group" button (use when the backend model is flat). */
    hideAddGroup?: boolean;
}

const LogicalFiltersBuilder = ({ filters, onChangeFilters, properties, hideAddGroup }: Props) => {
    const clearFilters = () => {
        onChangeFilters(undefined);
    };

    return (
        <QueryBuilder
            selectedPredicate={filters}
            onChangePredicate={onChangeFilters}
            properties={properties}
            clearFilters={clearFilters}
            depth={0}
            index={0}
            hideAddGroup={hideAddGroup}
        />
    );
};

export default LogicalFiltersBuilder;
