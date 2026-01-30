/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { Link } from '@components';
import React from 'react';

import { useIngestionSources } from '@app/ingestV2/source/builder/useIngestionSources';
import { IngestionSourceFormStep, MultiStepSourceBuilderState } from '@app/ingestV2/source/multiStepBuilder/types';
import { CUSTOM_SOURCE_DISPLAY_NAME, getSourceConfigs } from '@app/ingestV2/source/utils';
import { useMultiStepContext } from '@app/sharedV2/forms/multiStepForm/MultiStepFormContext';

export function ConnectionDetailsSubTitle() {
    const { state } = useMultiStepContext<MultiStepSourceBuilderState, IngestionSourceFormStep>();
    const { type } = state;
    const { ingestionSources } = useIngestionSources();
    const sourceConfigs = getSourceConfigs(ingestionSources, type as string);
    const sourceDisplayName = sourceConfigs?.displayName;
    const docsUrl = sourceConfigs?.docsUrl;

    const isCustomSource = sourceDisplayName === CUSTOM_SOURCE_DISPLAY_NAME;
    const displayName = isCustomSource ? 'this source' : sourceDisplayName;
    const linkDisplayName = isCustomSource ? 'Metadata Ingestion' : displayName;

    return (
        <>
            Provide credentials and define what metadata to collect from {displayName}.
            {docsUrl && (
                <>
                    {' '}
                    Check out the <Link href={docsUrl}>{linkDisplayName} Guide</Link> for more information.
                </>
            )}
        </>
    );
}
