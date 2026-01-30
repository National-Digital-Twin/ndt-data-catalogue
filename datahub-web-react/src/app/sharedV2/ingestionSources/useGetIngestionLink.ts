/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useIngestionOnboardingRedesignV1 } from '@app/ingestV2/hooks/useIngestionOnboardingRedesignV1';
import { PageRoutes } from '@conf/Global';

export const useGetIngestionLink = (hasIngestionSources: boolean) => {
    const showIngestionOnboardingRedesign = useIngestionOnboardingRedesignV1();

    let ingestionLink = PageRoutes.INGESTION;

    if (showIngestionOnboardingRedesign) {
        ingestionLink = hasIngestionSources ? PageRoutes.INGESTION : PageRoutes.INGESTION_CREATE;
    }

    return ingestionLink;
};
