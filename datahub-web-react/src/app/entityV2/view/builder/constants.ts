/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { LogicalOperatorType, LogicalPredicate } from '@app/sharedV2/queryBuilder/builder/types';

import { EntityType } from '@types';

export const URN_FILTER_NAME = 'urn';

/**
 * Entity types that can be searched and selected as individual assets in the View builder.
 * All selected entities are stored as URN filters, so the View shows exactly those assets.
 */
export const SELECTABLE_ASSET_ENTITY_TYPES = [
    EntityType.Dataset,
    EntityType.Dashboard,
    EntityType.Chart,
    EntityType.DataFlow,
    EntityType.DataJob,
    EntityType.Container,
    EntityType.Domain,
    EntityType.GlossaryTerm,
    EntityType.GlossaryNode,
    EntityType.Tag,
    EntityType.CorpUser,
    EntityType.CorpGroup,
    EntityType.DataPlatform,
    EntityType.Mlmodel,
    EntityType.MlfeatureTable,
    EntityType.MlprimaryKey,
    EntityType.Notebook,
    EntityType.Document,
    EntityType.Application,
];

/**
 * Tab keys for the view definition builder.
 * Build Filters (dynamic) is the default tab.
 */
export const BUILD_FILTERS_TAB_KEY = 'buildFilters';
export const SELECT_ASSETS_TAB_KEY = 'selectAssets';

/**
 * Default filter state for the Build Filters tab.
 * Starts with one blank condition row so users can immediately pick a property.
 */
export const DEFAULT_DYNAMIC_FILTER: LogicalPredicate = {
    type: 'logical',
    operator: LogicalOperatorType.AND,
    operands: [{ type: 'property' }],
};
