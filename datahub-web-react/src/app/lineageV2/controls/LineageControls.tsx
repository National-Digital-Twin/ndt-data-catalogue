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
import { Button, Divider } from 'antd';
import React, { useContext, useEffect, useState } from 'react';
import { Panel, useReactFlow } from 'reactflow';
import styled from 'styled-components';

import { useGetLineageTimeParams } from '@app/lineage/utils/useGetLineageTimeParams';
import { LineageNodesContext, TRANSITION_DURATION_MS } from '@app/lineageV2/common';
import DownloadLineageScreenshotButton from '@app/lineageV2/controls/DownloadLineageScreenshotButton';
import LineageSearchFilters from '@app/lineageV2/controls/LineageSearchFilters';
import LineageTimeRangeControls from '@app/lineageV2/controls/LineageTimeRangeControls';
import { StyledPanelButton } from '@app/lineageV2/controls/StyledPanelButton';
import { ControlPanel } from '@app/lineageV2/controls/common';
import TabFullsizedContext from '@app/shared/TabFullsizedContext';

import EnlargeIcon from '@images/dt-enlarge.svg?react';
import ReduceIcon from '@images/dt-reduce.svg?react';
import CalendarIcon from '@images/dt-calendar.svg?react';
import FilterIcon from '@images/dt-filter.svg?react';
import HomeIcon from '@images/dt-home.svg?react';
import ExpandRightIcon from '@images/dt-expand-right.svg?react';
import CollapseLeftIcon from '@images/dt-collapse-left.svg?react';


const StyledPanel = styled(Panel)`
    margin-top: 80px;
    display: flex;
    flex-direction: row;
    gap: 10px;
    height: 0; // Allow pointer events in gaps
`;

const StyledControlsPanel = styled(ControlPanel)<{ isExpanded: boolean }>`
    padding: 0;
    width: ${({ isExpanded }) => (isExpanded ? '150px' : '48px')};
    transition: width ${TRANSITION_DURATION_MS}ms ease-in-out;
    border-color: ${(props) => props.theme.styles['action-button-border-color']} !important;
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.16);
    border-radius: 4px;

    && .ant-btn > svg {
        flex-shrink: 0;
    }
`;

const StyledExpandContractButton = styled(Button)`
    border-radius: 4px;
    height: 48px;
    width: 48px;
    margin-top: 8px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    display: flex;
    border-color: ${(props) => props.theme.styles['action-button-border-color']} !important;
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.16);

    &:hover {
        background-color: ${(props) => props.theme.styles['action-button-hover-color']};
    }
`;

const StyledDivider = styled(Divider)`
    margin-top: -2px;
    margin-bottom: -2px;
`;

const ControlsColumn = styled.div``;

type PanelType = 'filters' | 'timeRange';

export default function LineageControls() {
    const { rootUrn, hideTransformations, showDataProcessInstances, showGhostEntities } =
        useContext(LineageNodesContext);
    const { isTabFullsize, setTabFullsize } = useContext(TabFullsizedContext);
    const { isDefault: isLineageTimeUnchanged } = useGetLineageTimeParams();
    const { fitView } = useReactFlow();

    const [isExpanded, setIsExpanded] = useState(false);
    const [visiblePanel, setVisiblePanel] = useState<PanelType | null>(null);

    // showExpandedText is a delayed version of isExpanded by .3 seconds
    const [showExpandedText, setShowExpandedText] = useState(false);
    useEffect(() => {
        if (isExpanded) {
            setShowExpandedText(true);
            return () => {};
        }
        const timeout = setTimeout(() => {
            setShowExpandedText(false);
        }, TRANSITION_DURATION_MS);
        return () => clearTimeout(timeout);
    }, [isExpanded]);

    return (
        <StyledPanel position="top-left">
            <ControlsColumn>
                <StyledControlsPanel isExpanded={isExpanded}>
                    <StyledPanelButton type="text" onClick={() => setIsExpanded(!isExpanded)}>
                        {showExpandedText ? <CollapseLeftIcon /> : <ExpandRightIcon />}
                        {showExpandedText ? 'Hide Menu' : null}
                    </StyledPanelButton>
                    <StyledDivider />
                    <StyledPanelButton
                        type="text"
                        onClick={() => {
                            fitView({ duration: 1000, nodes: [{ id: rootUrn }], maxZoom: 1 });
                        }}
                    >
                        <HomeIcon />
                        {showExpandedText ? 'Focus on Home' : null}
                    </StyledPanelButton>
                    <StyledDivider />
                    <StyledPanelButton
                        type="text"
                        onClick={() =>
                            visiblePanel === 'filters' ? setVisiblePanel(null) : setVisiblePanel('filters')
                        }
                    >
                        <FilterIcon />
                        {showExpandedText ? 'Filter' : null}
                    </StyledPanelButton>
                    <StyledDivider />
                    <StyledPanelButton
                        type="text"
                        onClick={() =>
                            visiblePanel === 'timeRange' ? setVisiblePanel(null) : setVisiblePanel('timeRange')
                        }
                    >
                        <CalendarIcon />
                        {showExpandedText ? 'Time Range' : null}
                    </StyledPanelButton>
                    <StyledDivider />
                    <DownloadLineageScreenshotButton showExpandedText={showExpandedText} />
                </StyledControlsPanel>
                {setTabFullsize && (
                    <StyledExpandContractButton onClick={() => setTabFullsize((v) => !v)}>
                        {isTabFullsize ? (
                            <ReduceIcon />
                        ) : (
                            <EnlargeIcon />
                        )}
                    </StyledExpandContractButton>
                )}
            </ControlsColumn>
            {visiblePanel === 'filters' && <LineageSearchFilters />}
            {visiblePanel === 'timeRange' && <LineageTimeRangeControls />}
        </StyledPanel>
    );
}
