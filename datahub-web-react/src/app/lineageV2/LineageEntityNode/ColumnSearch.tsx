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
import { Input } from 'antd';
import React, { Dispatch, SetStateAction } from 'react';
import styled from 'styled-components';

import { onClickPreventSelect } from '@app/lineageV2/common';

import SearchIcon from '@images/dt-search.svg?react';

const SearchInput = styled(Input)`
    border-radius: 4px;
    border: 0.5px solid ${(props) => props.theme.styles['search-bar-border-color']};
    cursor: text;
    font-size: 14px;
    height: 22px;
    padding: 8px;
    width: 100%;
    height: 32px;

    :focus,
    :hover {
        border: 0.5px solid ${(props) => props.theme.styles['search-bar-hover-border-color']} !important;
        box-shadow: none;
        outline: none;
    }

    &.ant-input-affix-wrapper-focused {
        border: 0.5px solid ${(props) => props.theme.styles['search-bar-focus-border-color']} !important;
        box-shadow: none;
        outline: none;
    }

    &.ant-input-affix-wrapper {
        padding: 0;
        padding-left: 4px;
    }
`;

interface Props {
    searchText: string;
    setSearchText: Dispatch<SetStateAction<string>>;
}

export default function ColumnSearch({ searchText, setSearchText }: Props) {
    // Add nodrag class to prevent node from being selected on click
    // See https://reactflow.dev/api-reference/types/node-props#notes
    return (
        <>
            <SearchInput
                defaultValue={searchText}
                placeholder="Find column"
                onChange={(e) => setSearchText(e.target.value.trim())}
                onClick={onClickPreventSelect}
                prefix={<SearchIcon height="16px" width="16px" />}
            />
        </>
    );
}
