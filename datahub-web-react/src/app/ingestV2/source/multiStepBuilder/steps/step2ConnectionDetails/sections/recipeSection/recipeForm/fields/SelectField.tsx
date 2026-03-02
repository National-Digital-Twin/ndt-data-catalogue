/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { SimpleSelect } from '@components';
import { Form } from 'antd';
import React from 'react';

import { RecipeFormItem } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/fields/RecipeFormItem';
import { CommonFieldProps } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/fields/types';

export function SelectField({ field, updateFormValue }: CommonFieldProps) {
    const form = Form.useFormInstance();
    const value = Form.useWatch([field.name], form);

    const handleUpdate = (values?: string[]) => {
        const selectedValue = values?.[0];
        form.setFieldsValue({ [field.name]: selectedValue });
        updateFormValue(field.name, selectedValue);
    };

    return (
        <RecipeFormItem recipeField={field} showHelperText>
            <SimpleSelect
                values={value ? [value] : []}
                onUpdate={handleUpdate}
                placeholder={field.placeholder}
                options={field.options ?? []}
                showClear={!field.required}
                width="full"
            />
        </RecipeFormItem>
    );
}
