/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { useCallback, useEffect, useMemo } from 'react';
import { useHistory, useLocation } from 'react-router';

import { updateUrlParam } from '@app/shared/updateUrlParam';

export const useUrlQueryParam = (paramKey: string, defaultValue?: string) => {
    const location = useLocation();
    const history = useHistory();

    const searchParams = useMemo(() => new URLSearchParams(location.search), [location.search]);

    const value = searchParams.get(paramKey) || defaultValue;
    const locationState = location.state;

    useEffect(() => {
        if (!searchParams.get(paramKey) && defaultValue) {
            updateUrlParam(history, paramKey, defaultValue, locationState);
        }
    }, [paramKey, defaultValue, history, searchParams, locationState]);

    const setValue = useCallback(
        (paramValue: string) => {
            updateUrlParam(history, paramKey, paramValue, locationState);
        },
        [paramKey, history, locationState],
    );

    return { value, setValue };
};
