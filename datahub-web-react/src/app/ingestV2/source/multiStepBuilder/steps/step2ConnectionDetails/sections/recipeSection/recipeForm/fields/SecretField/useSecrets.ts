/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useMemo } from 'react';

import { useListSecretsQuery } from '@graphql/ingestion.generated';

export function useSecrets() {
    const { data, refetch: refetchSecrets } = useListSecretsQuery({
        variables: {
            input: {
                start: 0,
                count: 1000, // get all secrets
            },
        },
        nextFetchPolicy: 'cache-first',
    });

    const secrets = useMemo(() => {
        const fetchedSecrets = data?.listSecrets?.secrets || [];
        return [...fetchedSecrets].sort((secretA, secretB) => secretA.name.localeCompare(secretB.name));
    }, [data?.listSecrets?.secrets]);

    return { secrets, refetchSecrets };
}
