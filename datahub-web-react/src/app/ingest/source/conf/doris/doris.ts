/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { SourceConfig } from '@app/ingest/source/conf/types';

import dorisLogo from '@images/dorislogo.png';

const placeholderRecipe = `\
source: 
    type: doris
    config: 
        # Coordinates
        host_port: # Your Apache Doris host and port, e.g. doris:9030
        database: # Your Apache Doris database name, e.g. datahub
    
        # Credentials
        # Add secret in Secrets Tab with relevant names for each variable
        username: "\${DORIS_USERNAME}" # Your Apache Doris username, e.g. root
        password: "\${DORIS_PASSWORD}" # Your Apache Doris password, e.g. password_01

        # Options
        include_tables: True
        include_views: True

        # Profiling
        profiling:
            enabled: false
`;

const dorisConfig: SourceConfig = {
    type: 'doris',
    placeholderRecipe,
    displayName: 'Apache Doris',
    docsUrl: 'https://docs.datahub.com/docs/generated/ingestion/sources/doris/',
    logoUrl: dorisLogo,
};

export default dorisConfig;
