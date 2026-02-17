/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { get } from 'lodash';

import { useEntityData } from '@src/app/entity/shared/EntityContext';

interface UseEntityDataExtractorOptions {
    customPath?: string;
    defaultPath: string;
    arrayProperty: string; // 'tags' or 'terms'
}

export const useEntityDataExtractor = ({ customPath, defaultPath, arrayProperty }: UseEntityDataExtractorOptions) => {
    const { entityData } = useEntityData();

    const extractData = () => {
        if (customPath) {
            return get(entityData, customPath);
        }
        return get(entityData, defaultPath);
    };

    const data = extractData();
    const isEmpty = !data?.[arrayProperty]?.length;

    return { data, isEmpty };
};
