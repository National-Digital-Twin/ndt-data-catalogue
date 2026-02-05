/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { colors } from '@components';
import React from 'react';
import styled from 'styled-components';

import backgroundVideo from '@images/login-signup-animation.mp4';

export const VideoWrapper = styled.div`
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    background-color: ${colors.gray[1600]};
`;

const BackgroundVideo = styled.video`
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100vw;
    height: 100vh;
    transform: translate(-50%, -50%);
    z-index: 1;
    object-fit: cover;
`;

export const Content = styled.div`
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

interface Props {
    children: React.ReactNode;
}

export default function AuthPageContainer({ children }: Props) {
    return (
        <VideoWrapper>
            <BackgroundVideo src={backgroundVideo} autoPlay muted loop playsInline preload="auto" />
            <Content>{children}</Content>
        </VideoWrapper>
    );
}
