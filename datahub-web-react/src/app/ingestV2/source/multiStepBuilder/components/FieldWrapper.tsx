/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React from 'react';
import styled from 'styled-components';

import { HelperText } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/fields/shared/HelperText';
import { FieldLabel } from '@app/sharedV2/forms/FieldLabel';

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
`;

const FieldLabelWithBottomPadding = styled(FieldLabel)`
    padding-bottom: 8px;
`;

interface Props {
    label: string;
    help?: string;
    required?: boolean;
}

export function FieldWrapper({ children, label, help, required }: React.PropsWithChildren<Props>) {
    return (
        <Wrapper>
            <FieldLabelWithBottomPadding label={label} required={required} />
            {children}
            {help && <HelperText text={help} />}
        </Wrapper>
    );
}
