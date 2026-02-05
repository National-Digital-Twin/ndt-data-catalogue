/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Input } from '@components';
import React, { useCallback, useState } from 'react';

import { FieldWrapper } from '@app/ingestV2/source/multiStepBuilder/components/FieldWrapper';
import { ErrorWrapper } from '@app/ingestV2/source/multiStepBuilder/steps/step2ConnectionDetails/sections/recipeSection/recipeForm/components/ErrorWrapper';

interface Props {
    label: string;
    value?: string;
    onChange?: (value: string) => void;
    name: string;
    required?: boolean;
    placeholder?: string;
}

export function Field({ label, value, onChange, name, required, placeholder }: Props) {
    const [isTouched, setIsTouched] = useState<boolean>(false);

    const onSetValue = useCallback(
        (newValue: string) => {
            onChange?.(newValue);
            setIsTouched(true);
        },
        [onChange],
    );

    return (
        <FieldWrapper label={label} required={required}>
            <Input
                label=""
                value={value}
                setValue={onSetValue}
                name={name}
                placeholder={placeholder}
                isRequired={required}
            />
            {!value && isTouched && <ErrorWrapper errors={[`${label} is required`]} />}
        </FieldWrapper>
    );
}
