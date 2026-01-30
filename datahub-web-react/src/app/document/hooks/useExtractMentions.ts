/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { useMemo } from 'react';

import { extractMentions } from '@app/document/utils/extractMentions';

/**
 * Hook to extract @ mentions (URNs) from markdown text.
 * Searches for markdown link patterns like [@Entity](urn:li:entityType:id)
 *
 * This hook memoizes the result of extractMentions to avoid recalculating on every render.
 */
export const useExtractMentions = (content: string) => {
    return useMemo(() => extractMentions(content), [content]);
};
