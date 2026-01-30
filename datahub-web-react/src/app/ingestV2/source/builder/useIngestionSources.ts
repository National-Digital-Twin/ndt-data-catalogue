/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useMemo } from 'react';

import sourcesJson from '@app/ingestV2/source/builder/sources.json';
import { SourceConfig } from '@app/ingestV2/source/builder/types';

export function useIngestionSources() {
    // TODO: replace with call to server once we have access to dynamic list of sources
    const ingestionSources: SourceConfig[] = useMemo(() => JSON.parse(JSON.stringify(sourcesJson)), []);

    return { ingestionSources };
}
