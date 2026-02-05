/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Checkbox, Text } from '@components';
import React from 'react';
import styled from 'styled-components';

const CheckboxWithHelper = styled.div`
    // compensate checkbox container size
    // see datahub-web-react/src/alchemy-components/components/Checkbox/components.ts -> CheckboxBase for details
    position: relative;
    left: -5px;

    display: flex;
    flex-direction: row;
    gap: 4px;
    align-items: center;
`;

interface Props {
    id?: string;
    checked?: boolean;
    onChange?: (newValue: boolean) => void;
    helper?: string | React.ReactNode;
    disabled?: boolean;
}

export function AntdFormCompatibleCheckbox({ id, checked, onChange, helper, disabled }: Props) {
    return (
        <CheckboxWithHelper>
            <Checkbox
                id={id}
                isChecked={checked}
                onCheckboxChange={onChange}
                justifyContent="flex-start"
                isDisabled={disabled}
            />
            {helper && (
                <Text size="sm" color="gray" colorLevel={600}>
                    {helper}
                </Text>
            )}
        </CheckboxWithHelper>
    );
}
