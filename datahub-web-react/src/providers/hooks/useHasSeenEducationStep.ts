/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useContext } from 'react';

import { useUserContext } from '@app/context/useUserContext';
import { convertStepId } from '@app/onboarding/utils';
import { EducationStepsContext } from '@providers/EducationStepsContext';

export default function useHasSeenEducationStep(stepId: string, isForUser = true) {
    const { educationSteps } = useContext(EducationStepsContext);
    const { user } = useUserContext();

    if (isForUser && !user?.urn) {
        // assume they have seen the step while user loads
        return true;
    }

    const finalStepId = isForUser && user?.urn ? convertStepId(stepId, user.urn) : stepId;

    // always assume they've seen the step while steps are loading
    return educationSteps?.some((step) => step.id === finalStepId) ?? true;
}
