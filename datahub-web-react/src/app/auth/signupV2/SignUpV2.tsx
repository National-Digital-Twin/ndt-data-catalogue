/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React from 'react';

import AuthPageContainer from '@app/auth/shared/AuthPageContainer';
import SignUpModal from '@app/auth/signupV2/SignUpModal';

export default function SignUpV2() {
    return (
        <AuthPageContainer>
            <SignUpModal />
        </AuthPageContainer>
    );
}
