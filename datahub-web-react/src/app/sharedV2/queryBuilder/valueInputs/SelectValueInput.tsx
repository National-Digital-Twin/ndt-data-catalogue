/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Select, SelectOption } from '@components';
import React, { useMemo } from 'react';

import { SelectOption as BuilderSelectOption } from '@app/sharedV2/queryBuilder/builder/property/types/values';

type Props = {
    options: BuilderSelectOption[];
    selected?: string[];
    label?: string;
    mode?: 'multiple' | 'tags';
    placeholder?: string;
    onChangeSelected: (newSelectedIds: string[] | undefined) => void;
};

export default function SelectValueInput({ options, selected, label, mode, placeholder, onChangeSelected }: Props) {
    const selectOptions: SelectOption[] = useMemo(() => {
        return options.map((option) => ({
            value: option.id,
            label: option.displayName,
        }));
    }, [options]);

    const isMultiSelect = mode === 'multiple';

    const hasSelection = (selected?.length ?? 0) > 0;

    return (
        <Select
            values={selected}
            onUpdate={onChangeSelected}
            placeholder={placeholder || 'Select a value...'}
            options={selectOptions}
            isMultiSelect={isMultiSelect}
            selectLabelProps={
                hasSelection
                    ? {
                          variant: 'labeled',
                          label: label ?? 'Items',
                      }
                    : undefined
            }
            width="full"
            showClear
        />
    );
}
