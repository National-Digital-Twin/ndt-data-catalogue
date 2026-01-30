/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { SYSTEM_INTERNAL_SOURCE_TYPE } from '@app/ingestV2/constants';

import { useGetNoOfIngestionSourcesQuery } from '@graphql/ingestion.generated';

export const useHasIngestionSources = () => {
    const { data, loading, error } = useGetNoOfIngestionSourcesQuery({
        variables: {
            input: {
                start: 0,
                count: 0,
                filters: [
                    {
                        field: 'sourceType',
                        values: [SYSTEM_INTERNAL_SOURCE_TYPE],
                        negated: true,
                    },
                ],
            },
        },
        fetchPolicy: 'cache-and-network',
    });

    const totalSources = data?.listIngestionSources?.total ?? 0;
    const hasIngestionSources = totalSources > 0;

    return {
        totalSources,
        hasIngestionSources,
        loading,
        error,
    };
};
