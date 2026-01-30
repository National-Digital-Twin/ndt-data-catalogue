/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Button } from '@components';
import React, { useCallback, useState } from 'react';

import {
    IngestionSourceFormStep,
    MultiStepSourceBuilderState,
    SubmitOptions,
} from '@app/ingestV2/source/multiStepBuilder/types';
import { MultiStepFormBottomPanel } from '@app/sharedV2/forms/multiStepForm/MultiStepFormBottomPanel';
import { useMultiStepContext } from '@app/sharedV2/forms/multiStepForm/MultiStepFormContext';

export function IngestionSourceBottomPanel() {
    const { isFinalStep, isCurrentStepCompleted, submit } = useMultiStepContext<
        MultiStepSourceBuilderState,
        IngestionSourceFormStep,
        SubmitOptions
    >();
    const [isSaveAndRunInProgress, setIsSaveAndRunInProgress] = useState<boolean>(false);

    const save = useCallback(
        async (options: SubmitOptions) => {
            setIsSaveAndRunInProgress(true);
            try {
                await submit?.(options);
            } finally {
                setIsSaveAndRunInProgress(false);
            }
        },
        [submit],
    );

    const onSave = useCallback(async () => {
        await save({ shouldRun: false });
    }, [save]);

    const onSaveAndRun = useCallback(async () => {
        await save({ shouldRun: true });
    }, [save]);

    const renderRightButtons = useCallback(
        (buttons: React.ReactNode[]) => {
            if (!isFinalStep()) return buttons;
            return [
                ...buttons,
                <Button
                    size="sm"
                    variant="outline"
                    disabled={!isCurrentStepCompleted() || isSaveAndRunInProgress}
                    onClick={onSave}
                >
                    Save
                </Button>,
                <Button size="sm" disabled={!isCurrentStepCompleted() || isSaveAndRunInProgress} onClick={onSaveAndRun}>
                    Save and Run
                </Button>,
            ];
        },
        [isFinalStep, isCurrentStepCompleted, onSave, onSaveAndRun, isSaveAndRunInProgress],
    );

    return (
        <MultiStepFormBottomPanel
            renderRightButtons={renderRightButtons}
            disabledNextTooltip="Enter a name to continue"
        />
    );
}
