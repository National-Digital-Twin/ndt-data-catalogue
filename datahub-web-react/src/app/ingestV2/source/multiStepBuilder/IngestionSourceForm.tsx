/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React, { useEffect, useMemo } from 'react';

import { useDiscardUnsavedChangesConfirmationContext } from '@app/sharedV2/confirmation/DiscardUnsavedChangesConfirmationContext';
import { useMultiStepContext } from '@app/sharedV2/forms/multiStepForm/MultiStepFormContext';

export function IngestionSourceForm() {
    const { getCurrentStep, isDirty } = useMultiStepContext();

    const { setIsDirty } = useDiscardUnsavedChangesConfirmationContext();
    useEffect(() => setIsDirty(isDirty()), [isDirty, setIsDirty]);

    const currentStep = useMemo(() => getCurrentStep?.(), [getCurrentStep]);

    if (!currentStep) return null;

    return <>{currentStep.content}</>;
}
