/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { SourceBuilderState } from '@app/ingestV2/source/builder/types';
import { Step } from '@app/sharedV2/forms/multiStepForm/types';

import { IngestionSource } from '@types';

export interface IngestionSourceFormStep extends Step {
    hideRightPanel?: boolean;
    hideBottomPanel?: boolean;
}

export interface MultiStepSourceBuilderState extends SourceBuilderState {
    shouldRun?: boolean;
    ingestionSource?: IngestionSource;
    isEditing?: boolean;
    // To restore last validation state after moving back
    isConnectionDetailsValid?: boolean;
}

export interface SubmitOptions {
    shouldRun?: boolean;
}
