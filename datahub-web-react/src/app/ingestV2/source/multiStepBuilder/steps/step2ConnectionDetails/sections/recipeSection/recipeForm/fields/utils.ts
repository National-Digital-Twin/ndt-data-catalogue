/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { RecipeField } from '@app/ingestV2/source/builder/RecipeForm/common';

export function resolveDynamicOptions<T extends RecipeField>(field: T, values: Record<string, any>): T {
    let resolvedField = field;
    if (field.dynamicRequired) {
        resolvedField = { ...resolvedField, required: field.dynamicRequired(values) };
    }

    if (field.dynamicHidden) {
        resolvedField = { ...resolvedField, hidden: field.dynamicHidden(values) };
    }

    if (field.dynamicLabel) {
        resolvedField = { ...resolvedField, label: field.dynamicLabel(values) };
    }

    if (field.dynamicDisabled) {
        resolvedField = { ...resolvedField, disabled: field.dynamicDisabled(values) };
    }

    return resolvedField;
}
