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
import React, { useContext } from 'react';
import styled from 'styled-components';

import { useEntityData } from '@app/entity/shared/EntityContext';
import { CompactLineageTab } from '@app/entityV2/shared/tabs/Lineage/CompactLineageTab';
import { LineageColumnView } from '@app/entityV2/shared/tabs/Lineage/LineageColumnView';
import { useLineageViewState } from '@app/entityV2/shared/tabs/Lineage/hooks';
import { TabRenderType } from '@app/entityV2/shared/types';
import LineageExplorer from '@app/lineage/LineageExplorer';
import LineageGraph from '@app/lineageV2/LineageGraph';
import { useLineageV2 } from '@app/lineageV2/useLineageV2';
import TabFullsizedContext from '@app/shared/TabFullsizedContext';

import { LineageDirection } from '@types';

const LINEAGE_SWITCH_WIDTH = 140;

const LineageTabWrapper = styled.div`
    display: flex;
    flex-direction: column;
    height: 100%;
`;

const LineageSwitchWrapper = styled.div`
    border: 1px solid ${(props) => props.theme.styles['border-button-disabled']};
    border-radius: 8px;
    display: flex;
    margin: 13px 11px;
    width: ${LINEAGE_SWITCH_WIDTH * 2}px;
`;

const LineageViewSwitch = styled.div<{ selected: boolean, left: boolean }>`
    background: ${({ selected, theme }) => (selected ? `${theme.styles['tab-control-selected']}` : '#fff')};
    color: ${({ selected, theme }) => (selected ? '#fff' : `${theme.styles['tab-control']}`)};
    cursor: pointer;
    border-radius: ${({ left }) => (left ? '8px 0 0 8px' : '0 8px 8px 0')};
    display: flex;
    font-size: 14.2px;
    justify-content: center;
    line-height: 38px;
    height: 38px;
    width: ${LINEAGE_SWITCH_WIDTH}px;
`;

const VisualizationWrapper = styled.div`
    display: flex;
    height: 100%;
`;

const LineageTabHeader = styled.div`
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid ${(props) => props.theme.styles['border-button-disabled']};
`;

interface Props {
    properties?: { defaultDirection: LineageDirection };
    renderType: TabRenderType;
}

export function LineageTab({ properties, renderType }: Props) {
    const defaultDirection = properties?.defaultDirection || LineageDirection.Downstream;

    if (renderType === TabRenderType.COMPACT) {
        return <CompactLineageTab defaultDirection={defaultDirection} />;
    }
    return <WideLineageTab defaultDirection={defaultDirection} />;
}

function WideLineageTab({ defaultDirection }: { defaultDirection: LineageDirection }) {
    const { isTabFullsize } = useContext(TabFullsizedContext);
    const { urn, entityType } = useEntityData();
    const isLineageV2 = useLineageV2();
    const { isVisualizeView, setVisualizeView, setVisualizeViewInEditMode } = useLineageViewState();

    return (
        <LineageTabWrapper>
            {!isTabFullsize && (
                <LineageTabHeader>
                    <LineageSwitchWrapper>
                        <LineageViewSwitch selected={isVisualizeView} onClick={() => setVisualizeView(true)} left>
                            Explorer View
                        </LineageViewSwitch>
                        <LineageViewSwitch selected={!isVisualizeView} onClick={() => setVisualizeView(false)} left={false}>
                            Impact Analysis
                        </LineageViewSwitch>
                    </LineageSwitchWrapper>
                </LineageTabHeader>
            )}
            {!isVisualizeView && (
                <LineageColumnView
                    defaultDirection={defaultDirection}
                    setVisualizeViewInEditMode={setVisualizeViewInEditMode}
                />
            )}
            {isVisualizeView && !isLineageV2 && <LineageExplorer urn={urn} type={entityType} />}
            {isVisualizeView && isLineageV2 && (
                <VisualizationWrapper>
                    <LineageGraph />
                </VisualizationWrapper>
            )}
        </LineageTabWrapper>
    );
}
