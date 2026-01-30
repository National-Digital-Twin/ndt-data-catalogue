/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useCallback, useContext } from 'react';

import { useUserContext } from '@app/context/useUserContext';
import { convertStepId } from '@app/onboarding/utils';
import { EducationStepsContext } from '@providers/EducationStepsContext';

import { useBatchUpdateStepStatesMutation } from '@graphql/step.generated';
import { StepStateResult } from '@types';

export default function useUpdateEducationStep() {
    const { setEducationSteps } = useContext(EducationStepsContext);
    const user = useUserContext();
    const [batchUpdateStepStates] = useBatchUpdateStepStatesMutation();

    const updateEducationStep = useCallback(
        (stepId: string, isForUser = true) => {
            const finalStepId = isForUser ? convertStepId(stepId, user.urn || '') : stepId;
            const finalStep: StepStateResult = { id: finalStepId, properties: [] };
            batchUpdateStepStates({ variables: { input: { states: [finalStep] } } }).then(() => {
                setEducationSteps((existingSteps) => (existingSteps ? [...existingSteps, finalStep] : [finalStep]));
            });
        },
        [batchUpdateStepStates, setEducationSteps, user?.urn],
    );

    return { updateEducationStep };
}
