/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Input } from '@components';
import { Form } from 'antd';
import React, { useMemo } from 'react';

import { LinkFormData, LinkFormVariant } from '@app/entityV2/shared/components/links/types';

export function UrlLinkForm() {
    const form = Form.useFormInstance<LinkFormData>();
    const variant = Form.useWatch('variant', form);

    const isRequired = useMemo(() => {
        return variant !== LinkFormVariant.UploadFile;
    }, [variant]);

    return (
        <Form.Item
            name="url"
            rules={
                isRequired
                    ? [
                          {
                              required: true,
                              message: 'A URL is required.',
                          },
                          {
                              type: 'url',
                              message: 'This field must be a valid url.',
                          },
                      ]
                    : []
            }
        >
            <Input label="URL" placeholder="https://" inputTestId="url-input" isRequired={isRequired} />
        </Form.Item>
    );
}
