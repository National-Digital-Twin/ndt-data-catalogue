/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { createContext, useContext } from 'react';

// Context for handling breadcrumb navigation within the document modal
export const DocumentModalNavigationContext = createContext<{
    navigateToDocument: ((urn: string) => void) | null;
}>({
    navigateToDocument: null,
});

export const useDocumentModalNavigation = () => {
    const context = useContext(DocumentModalNavigationContext);
    return context;
};
