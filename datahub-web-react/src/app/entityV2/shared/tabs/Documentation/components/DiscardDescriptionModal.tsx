/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React from 'react';

import { ConfirmationModal } from '@app/sharedV2/modals/ConfirmationModal';

type Props = {
    cancelModalVisible?: boolean;
    onDiscard?: () => void;
    onCancel?: () => void;
};

export const DiscardDescriptionModal = ({ cancelModalVisible, onDiscard, onCancel }: Props) => {
    return (
        <ConfirmationModal
            isOpen={!!cancelModalVisible}
            handleClose={() => {
                onCancel?.();
            }}
            handleConfirm={() => onDiscard?.()}
            modalTitle="Exit Editor"
            modalText="Are you sure you want to close the documentation editor? Any unsaved changes will be lost."
        />
    );
};
