/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { get } from 'lodash';
import YAML from 'yamljs';

import { RecipeField } from '@app/ingestV2/source/builder/RecipeForm/common';

export function getValuesFromRecipe(displayRecipe: string, allFields: RecipeField[]) {
    const initialValues = {};
    const recipeObj = YAML.parse(displayRecipe);

    if (recipeObj) {
        allFields.forEach((field) => {
            if (field.getValueFromRecipeOverride) {
                initialValues[field.name] = field.getValueFromRecipeOverride(recipeObj);
            } else {
                initialValues[field.name] = get(recipeObj, field.fieldPath);
            }
        });
    }

    return initialValues;
}
