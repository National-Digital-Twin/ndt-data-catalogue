/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useCallback, useMemo } from 'react';

import { useUrlQueryParam } from '@app/shared/useUrlQueryParam';
import usePagination, { Pagination } from '@app/sharedV2/pagination/usePagination';

export default function useUrlParamsPagination(defaultPageSize?: number) {
    const { value: urlParamPage, setValue: setUrlParamPage } = useUrlQueryParam('page', '1');

    const urlPage = useMemo(() => Number(urlParamPage), [urlParamPage]);
    const setUrlPage = useCallback((newPage: number) => setUrlParamPage(newPage.toString()), [setUrlParamPage]);

    const { page, setPage, pageSize, setPageSize, start, count } = usePagination(defaultPageSize, urlPage);

    const onSetPage = useCallback(
        (newPage: number) => {
            setUrlPage(newPage);
            setPage(newPage);
        },
        [setUrlPage, setPage],
    );

    return { page, setPage: onSetPage, pageSize, setPageSize, start, count } as Pagination;
}
