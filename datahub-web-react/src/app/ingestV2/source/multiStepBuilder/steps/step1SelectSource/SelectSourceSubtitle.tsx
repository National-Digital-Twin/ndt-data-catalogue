/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Link } from '@components';
import React from 'react';

export default function SelectSourceSubtitle() {
    return (
        <>
            Select a platform to connect to DataHub.{' '}
            <Link href="https://docs.datahub.com/docs/metadata-ingestion-security" style={{ fontStyle: 'italic' }}>
                Learn more about keeping credentials in your environment.
            </Link>
        </>
    );
}
