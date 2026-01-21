/*
 * SPDX-License-Identifier: Apache-2.0

 * Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced, and maintained by
 * the National Digital Twin Programme.
 *
 * Modifications made by the National Digital Twin Programme (NDTP)
 * © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme
 * and is legally attributed to the Department for Business and Trade (UK) as the governing
 * entity.
 */
import React from 'react';

import PersonalizationLoadingModal from '@app/homeV2/persona/PersonalizationLoadingModal';
import HomePageContent from '@app/homeV3/HomePageContent';
import Header from '@app/homeV3/header/Header';
import { HomePageContainer, PageWrapper } from '@app/homeV3/styledComponents';
import { WelcomeToDataHubModal } from '@app/onboarding/WelcomeToDataHubModal';
import { SearchablePage } from '@app/searchV2/SearchablePage';

export const HomePage = () => {
    return (
        <>
            <SearchablePage>
                <HomePageContainer>
                    <PageWrapper>
                        <Header />
                        <HomePageContent />
                    </PageWrapper>
                </HomePageContainer>
            </SearchablePage>
            <PersonalizationLoadingModal />
            <WelcomeToDataHubModal />
        </>
    );
};
