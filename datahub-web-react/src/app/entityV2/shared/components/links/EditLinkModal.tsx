/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Form } from 'antd';
import React, { useCallback } from 'react';

import AddEditLinkModal from '@app/entityV2/shared/components/links/AddEditLinkModal';
import { LinkFormData } from '@app/entityV2/shared/components/links/types';
import { useLinkUtils } from '@app/entityV2/shared/components/links/useLinkUtils';
import { getInitialLinkFormDataFromInstitutionMemory } from '@app/entityV2/shared/components/links/utils';
import { useIsDocumentationFileUploadV1Enabled } from '@app/shared/hooks/useIsDocumentationFileUploadV1Enabled';

import { InstitutionalMemoryMetadata } from '@types';

interface Props {
    link?: InstitutionalMemoryMetadata | null;
    onClose: () => void;
}

export function EditLinkModal({ link, onClose }: Props) {
    const isDocumentationFileUploadV1Enabled = useIsDocumentationFileUploadV1Enabled();
    const { handleUpdateLink, showInAssetPreview, setShowInAssetPreview } = useLinkUtils(link);
    const [form] = Form.useForm<LinkFormData>();

    const handleUpdate = useCallback(() => {
        if (link) {
            form.validateFields()
                .then((values) => handleUpdateLink(values))
                .then(() => onClose());
        }
    }, [handleUpdateLink, onClose, link, form]);

    const handleClose = useCallback(() => {
        form.resetFields();
        onClose();
    }, [onClose, form]);

    return (
        <AddEditLinkModal
            variant="update"
            form={form}
            initialValues={getInitialLinkFormDataFromInstitutionMemory(link, isDocumentationFileUploadV1Enabled)}
            onSubmit={handleUpdate}
            onClose={handleClose}
            showInAssetPreview={showInAssetPreview}
            setShowInAssetPreview={setShowInAssetPreview}
        />
    );
}
