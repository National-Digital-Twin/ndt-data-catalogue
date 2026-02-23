/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { FacetFilter } from '@types';

export enum ViewBuilderMode {
    /**
     * See a View definition in Preview Mode.
     */
    PREVIEW,
    /**
     * Create or Edit a View.
     */
    EDITOR,
}

/**
 * Represents a single filter criterion within a View definition.
 * Used as the intermediate representation between the UI filter tabs
 * and the backend-compatible FacetFilter format.
 */
export type ViewFilter = {
    field: string;
    values: string[];
    condition?: FacetFilter['condition'];
    negated?: boolean;
};
