/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Input } from '@components';
import { Form, FormInstance } from 'antd';
import React from 'react';
import styled from 'styled-components';

import { LoginFormValues } from '@app/auth/shared/types';
import { FieldLabel } from '@app/sharedV2/forms/FieldLabel';

const FormContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 0 20px;
`;

const ItemContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 4px;
`;

interface Props {
    form: FormInstance;
    handleSubmit: (values: LoginFormValues) => void;
    onFormChange: () => void;
    isSubmitDisabled: boolean;
}

export default function LoginForm({ form, handleSubmit, onFormChange, isSubmitDisabled }: Props) {
    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !isSubmitDisabled) {
            form.submit();
        }
    };

    return (
        <FormContainer>
            <Form form={form} onFinish={handleSubmit} onFieldsChange={onFormChange} onKeyDown={handleKeyDown}>
                <ItemContainer>
                    <FieldLabel label="Username" required />
                    <Form.Item rules={[{ required: true, message: 'Please fill in your username' }]} name="username">
                        <Input placeholder="Enter username" inputTestId="username" />
                    </Form.Item>
                </ItemContainer>

                <ItemContainer>
                    <FieldLabel label="Password" required />
                    <Form.Item rules={[{ required: true, message: 'Please fill in your password' }]} name="password">
                        <Input placeholder="********" type="password" inputTestId="password" />
                    </Form.Item>
                </ItemContainer>
            </Form>
        </FormContainer>
    );
}
