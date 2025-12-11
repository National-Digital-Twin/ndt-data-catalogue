/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Modal } from '@components';
import { Form, Input } from 'antd';
import React from 'react';

import { IncidentState } from '@types';

const { TextArea } = Input;

type AddIncidentProps = {
    handleResolved: () => void;
    isResolvedModalVisible: boolean;
    updateIncidentStatus: (state: IncidentState, resolvedMessage: string) => void;
};

export const ResolveIncidentModal = ({
    handleResolved,
    isResolvedModalVisible,
    updateIncidentStatus,
}: AddIncidentProps) => {
    const [form] = Form.useForm();

    const handleClose = () => {
        form.resetFields();
        handleResolved();
    };

    const onResolvedIncident = (formData: any) => {
        updateIncidentStatus(IncidentState.Resolved, formData.message);
        handleClose();
    };

    return (
        <>
            <Modal
                title="Resolve Incident"
                open={isResolvedModalVisible}
                destroyOnClose
                onCancel={handleClose}
                buttons={[
                    {
                        text: 'Cancel',
                        variant: 'text',
                        onClick: handleClose,
                    },
                    {
                        text: 'Resolve',
                        variant: 'filled',
                        onClick: form.submit,
                        buttonDataTestId: 'confirm-resolve',
                    },
                ]}
            >
                <Form form={form} name="resolveIncidentForm" onFinish={onResolvedIncident} layout="vertical">
                    <Form.Item name="message" label="Note (optional)">
                        <TextArea rows={4} />
                    </Form.Item>
                </Form>
            </Modal>
        </>
    );
};
