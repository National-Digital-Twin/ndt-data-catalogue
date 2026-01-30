/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import React from 'react';

import LoginModal from '@app/auth/loginV2/LoginModal';
import AuthPageContainer from '@app/auth/shared/AuthPageContainer';

export default function LoginV2() {
    return (
        <AuthPageContainer>
            <LoginModal />
        </AuthPageContainer>
    );
}
