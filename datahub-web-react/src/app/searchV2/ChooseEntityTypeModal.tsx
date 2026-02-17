/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Modal } from '@components';
import { Select } from 'antd';
import React, { useState } from 'react';

import { useEntityRegistry } from '@app/useEntityRegistry';

import { EntityType } from '@types';

type Props = {
    onCloseModal: () => void;
    onOk?: (results: string[]) => void;
    title: string;
    defaultValues?: string[];
};

const { Option } = Select;

export const ChooseEntityTypeModal = ({ defaultValues, onCloseModal, onOk, title }: Props) => {
    const entityRegistry = useEntityRegistry();
    const entityTypes = entityRegistry.getSearchEntityTypes();

    const [stagedValues, setStagedValues] = useState(defaultValues || []);

    const addEntityType = (newType) => {
        setStagedValues([...stagedValues, newType]);
    };

    const removeEntityType = (type) => {
        setStagedValues(stagedValues.filter((stagedValue) => stagedValue !== type));
    };

    return (
        <Modal
            title={title}
            open
            onCancel={onCloseModal}
            keyboard
            buttons={[
                {
                    text: 'Cancel',
                    variant: 'text',
                    onClick: onCloseModal,
                },
                {
                    text: 'Done',
                    variant: 'filled',
                    disabled: stagedValues.length === 0,
                    onClick: () => onOk?.(stagedValues),
                },
            ]}
        >
            <Select
                mode="multiple"
                style={{ width: '100%' }}
                placeholder="Datasets, Dashboards, Charts, and more..."
                onSelect={(newValue) => addEntityType(newValue)}
                onDeselect={(newValue) => removeEntityType(newValue)}
                value={stagedValues.map((stagedEntityType) => ({
                    value: stagedEntityType,
                    label: entityRegistry.getCollectionName(stagedEntityType as EntityType),
                }))}
                dropdownMatchSelectWidth={false}
            >
                {entityTypes.map((type) => (
                    <Option key={type} value={type}>
                        {entityRegistry.getCollectionName(type)}
                    </Option>
                ))}
            </Select>
        </Modal>
    );
};
