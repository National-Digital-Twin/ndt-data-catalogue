/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React, { useMemo } from 'react';
import styled from 'styled-components';

import { RecipeField } from '@app/ingestV2/source/builder/RecipeForm/common';
import {
    CustomLabelFormItem,
    CustomLabelFormItemProps,
} from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/components/CustomFormItem';
import { HelperText } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/fields/shared/HelperText';

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
`;

interface Props extends CustomLabelFormItemProps {
    recipeField?: RecipeField;
    showTooltip?: boolean;
    showHelperText?: boolean;
}

export function RecipeFormItem({
    children,
    recipeField,
    showHelperText,
    showTooltip,
    tooltip,
    ...props
}: React.PropsWithChildren<Props>) {
    const rules = useMemo(() => {
        if (recipeField?.rules) return recipeField.rules;
        if (recipeField?.required) return [{ required: true, message: `${recipeField.label} is required` }];
        return undefined;
    }, [recipeField]);

    const helperText = useMemo(() => {
        return recipeField?.helper ?? recipeField?.tooltip;
    }, [recipeField]);

    // Don't render the field if it's hidden
    if (recipeField?.hidden) {
        return null;
    }

    return (
        <Wrapper>
            <CustomLabelFormItem
                required={recipeField?.required}
                label={recipeField?.label}
                name={recipeField?.name}
                tooltip={showTooltip ? (recipeField?.tooltip ?? tooltip) : undefined}
                rules={rules}
                showError={false}
                {...props}
            >
                {children}
            </CustomLabelFormItem>
            {showHelperText && helperText && <HelperText text={helperText} />}
        </Wrapper>
    );
}
