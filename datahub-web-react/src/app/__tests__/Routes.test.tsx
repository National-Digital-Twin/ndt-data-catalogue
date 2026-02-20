/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { MockedProvider } from '@apollo/client/testing';
import { render, waitFor } from '@testing-library/react';
import React from 'react';

import { Routes } from '@app/Routes';
import { mocks } from '@src/Mocks';
import TestPageContainer from '@utils/test-utils/TestPageContainer';

const mockMfeConfigFetch = () => {
    global.fetch = vi.fn().mockImplementation((url) => {
        let requestUrl: string;

        if (typeof url === 'string') {
            requestUrl = url;
        } else if (url && typeof (url as Request).url === 'string') {
            requestUrl = url.url;
        } else {
            requestUrl = String(url);
        }

        if (requestUrl.includes('/mfe/config')) {
            return Promise.resolve({
                ok: true,
                text: () =>
                    Promise.resolve(`subNavigationMode: false
microFrontends:
    - id: myapp
        label: myapp from Yaml
        path: /myapp-mfe
        remoteEntry: http://localhost:9111/remoteEntry.js
        module: myapp/mount
        flags:
            enabled: true
            showInNav: false
        navIcon: Globe`),
            });
        }

        return Promise.reject(new Error(`Unhandled fetch: ${url}`));
    });
};

test('renders embed page properly', async () => {
    mockMfeConfigFetch();

    const { getByText } = render(
        <MockedProvider mocks={mocks} addTypename={false}>
            <TestPageContainer initialEntries={['/embed/dataset/urn:li:dataset:3']}>
                <Routes />
            </TestPageContainer>
        </MockedProvider>,
    );

    await waitFor(() => expect(getByText('Yet Another Dataset')).toBeInTheDocument());

    vi.restoreAllMocks();
});

test('loads mfe config for missing mfe route when some mfes are active', async () => {
    mockMfeConfigFetch();

    const { getByTestId } = render(
        <MockedProvider mocks={mocks} addTypename={false}>
            <TestPageContainer initialEntries={['/mfe/missing']}>
                <Routes />
            </TestPageContainer>
        </MockedProvider>,
    );

    await waitFor(() => expect(global.fetch).toHaveBeenCalled(), { timeout: 10000 });
    await waitFor(() => expect(getByTestId('search-input')).toBeInTheDocument(), { timeout: 10000 });

    vi.restoreAllMocks();
}, 15000);
