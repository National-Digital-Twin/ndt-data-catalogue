/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { Layout } from 'antd';
import React, { useContext, useState } from 'react';
import styled, { useTheme } from 'styled-components';

import { useNavBarContext } from '@app/homeV2/layout/navBarRedesign/NavBarContext';
import NavBarToggler from '@app/homeV2/layout/navBarRedesign/NavBarToggler';
import { useShowHomePageRedesign } from '@app/homeV3/context/hooks/useShowHomePageRedesign';
import OnboardingContext from '@app/onboarding/OnboardingContext';
import { V2_SEARCH_BAR_ID } from '@app/onboarding/configV2/HomePageOnboardingConfig';
import { SearchBar } from '@app/searchV2/SearchBar';
import { SearchBarV2 } from '@app/searchV2/searchBarV2/SearchBarV2';
import useSearchViewAll from '@app/searchV2/useSearchViewAll';
import { useIsHomePage } from '@app/shared/useIsHomePage';
import { useAppConfig } from '@app/useAppConfig';
import { useShowNavBarRedesign } from '@app/useShowNavBarRedesign';
import { EntityRegistry } from '@src/entityRegistryContext';

import { AutoCompleteResultForEntity } from '@types';
import analytics, { EventType } from '@src/app/analytics';

import { Link } from 'react-router-dom';
import { Theme } from '@conf/theme/types';

const getStyles = ($isShowNavBarRedesign?: boolean) => {
    return {
        input: {
            backgroundColor: $isShowNavBarRedesign ? 'white' : '#343444',
        },
        searchBox: {
            maxWidth: $isShowNavBarRedesign ? '100%' : 620,
            minWidth: $isShowNavBarRedesign ? 300 : 400,
        },
        searchBoxContainer: {
            padding: 0,
            display: 'flex',
            justifyContent: 'center',
            width: $isShowNavBarRedesign ? '648px' : '620px',
            minWidth: '400px',
        },
    };
};

const Wrapper = styled.div<{ $isShowNavBarRedesign?: boolean }>`
    position: fixed;
    width: 100%;
    ${(props) =>
        !props.$isShowNavBarRedesign &&
        `
        line-height: 20px;
        padding: 0px 12px;
    `}
`;

const LogoWrapper = styled.div`
    display: flex;
    flex: 1;
    gap: 8px;
`

const Header = styled(Layout)<{ $isNavBarCollapsed?: boolean; $isShowNavBarRedesign?: boolean }>`
    background-color: transparent;
    height: ${(props) => (props.$isShowNavBarRedesign ? '85px' : '72px')};
    display: flex;
    ${(props) =>
        props.$isShowNavBarRedesign &&
        `
        margin-top: 8px;
        gap: 16px;
        flex-direction: row;

        // preventing of NavBar's overlapping
        position: relative; 
        left: ${props.$isNavBarCollapsed ? '-112px' : '-270px'};
        transition: none;
        @media only screen and (min-width: 1280px) {
            transition: padding-left 250ms ease-in-out;
            padding-left: ${props.$isNavBarCollapsed ? '380px' : '602px'};
            left: -270px;
        }
        @media only screen and (max-width: 1200px) {
            transition: padding 250ms ease-in-out;
        }
    `}
    ${(props) => props.$isShowNavBarRedesign && !props.$isNavBarCollapsed && 'justify-content: space-between;'}
    align-items: center;
`;

const HeaderBackground = styled.div<{ $isShowNavBarRedesign?: boolean }>`
    ${(props) => !props.$isShowNavBarRedesign && 'background-color: #171723;'}
    position: fixed;
    height: 100px;
    width: 100%;
    z-index: -1;
`;
const HeaderWrapper = styled.div<{ $isShowNavBarRedesign?: boolean }>`
    display: flex;
    flex: 1;
    align-items: center;
    ${(props) =>
        !props.$isShowNavBarRedesign &&
        `
        margin-left: 80px;
        margin-top: 6px;
    `}
`;

const SearchBarContainer = styled.div<{ $isShowNavBarRedesign?: boolean }>`
    display: flex;
    flex: 1;
`;

const Logotype = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 36px;
    max-height: 40px;
    max-width: 181px;
    border-radius: 4px;
    position: relative;
    object-fit: contain;

    & svg,
    img {
        max-height: 40px;
        max-width: 181px;
        min-width: 181px;
        object-fit: contain;
    }
`;

const CustomLogo = styled.img`
    object-fit: contain;
    max-height: 36px;
    max-width: 36px;
    min-height: 20px;
    min-width: 20px;
`;

const StyledLink = styled(Link)`
    display: flex;
    height: 40px;
    align-items: center;
    margin-left: 25px;
`;

const UserMenuWrapper = styled.div`
    display: flex;
    flex: 1;
`;

type Props = {
    initialQuery: string;
    placeholderText: string;
    suggestions: Array<AutoCompleteResultForEntity>;
    onSearch: (query: string) => void;
    onQueryChange: (query: string) => void;
    entityRegistry: EntityRegistry;
    hideSearchBar?: boolean;
};

/**
 * A header containing a Logo, Search Bar view, & an account management dropdown.
 */
export const SearchHeader = ({
    initialQuery,
    placeholderText,
    suggestions,
    onSearch,
    onQueryChange,
    entityRegistry,
    hideSearchBar,
}: Props) => {
    const [, setIsSearchBarFocused] = useState(false);
    const appConfig = useAppConfig();
    const viewsEnabled = appConfig.config?.viewsConfig?.enabled || false;
    const { isUserInitializing } = useContext(OnboardingContext);
    const { toggle, isCollapsed } = useNavBarContext();
    const isShowNavBarRedesign = useShowNavBarRedesign();
    const showHomepageRedesign = useShowHomePageRedesign();
    const isHomePage = useIsHomePage();
    const styles = getStyles(isShowNavBarRedesign);
    const theme = useTheme() as Theme;

    const showSearchBarAutocompleteRedesign = appConfig.config.featureFlags?.showSearchBarAutocompleteRedesign;
    const FinalSearchBar = showSearchBarAutocompleteRedesign ? SearchBarV2 : SearchBar;
    
    function handleLogoClick() {
        if (isHomePage && showHomepageRedesign) {
            toggle();
        }
        analytics.event({ type: EventType.NavBarItemClick, label: 'Home' });
    }

    return (
        <>
            <HeaderBackground $isShowNavBarRedesign={isShowNavBarRedesign} />
            <Wrapper $isShowNavBarRedesign={isShowNavBarRedesign}>
                <Header $isShowNavBarRedesign={isShowNavBarRedesign} $isNavBarCollapsed={isCollapsed}>
                    {!hideSearchBar && (
                        <HeaderWrapper $isShowNavBarRedesign={isShowNavBarRedesign}>
                            <LogoWrapper>
                                <NavBarToggler />
                                <StyledLink to="/" onClick={handleLogoClick}>
                                    <Logotype>{<CustomLogo alt="logo" src={theme.assets.logoUrl} />}</Logotype>
                                </StyledLink>
                            </LogoWrapper>
                            <SearchBarContainer>
                                <FinalSearchBar
                                    isLoading={isUserInitializing || !appConfig.loaded}
                                    id={V2_SEARCH_BAR_ID}
                                    style={styles.searchBoxContainer}
                                    autoCompleteStyle={styles.searchBox}
                                    inputStyle={styles.input}
                                    initialQuery={initialQuery}
                                    placeholderText={placeholderText}
                                    suggestions={suggestions}
                                    onSearch={onSearch}
                                    onQueryChange={onQueryChange}
                                    entityRegistry={entityRegistry}
                                    setIsSearchBarFocused={setIsSearchBarFocused}
                                    viewsEnabled={viewsEnabled}
                                    isShowNavBarRedesign={isShowNavBarRedesign}
                                    combineSiblings
                                    fixAutoComplete
                                    showQuickFilters
                                    showViewAllResults
                                    showCommandK
                                />
                            </SearchBarContainer>
                            <UserMenuWrapper></UserMenuWrapper>
                        </HeaderWrapper>
                    )}
                </Header>
            </Wrapper>
        </>
    );
};
