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
import { ConsoleSqlOutlined, HomeOutlined, LoadingOutlined } from '@ant-design/icons';
import { Tooltip } from '@components';
import { Skeleton, Spin } from 'antd';
import React, { useContext } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';
import styled from 'styled-components';

import { LINEAGE_COLORS } from '@app/entityV2/shared/constants';
import { LoadingWrapper } from '@app/lineageV2/LineageEntityNode/NodeContents';
import LineageVisualizationContext from '@app/lineageV2/LineageVisualizationContext';
import {
    FetchStatus,
    LineageDisplayContext,
    LineageEntity,
    LineageNodesContext,
    isGhostEntity,
    useIgnoreSchemaFieldStatus,
} from '@app/lineageV2/common';
import { useEntityRegistryV2 } from '@app/useEntityRegistry';

import { useGetQueryQuery } from '@graphql/query.generated';
import { EntityType, LineageDirection } from '@types';

import HomeIcon from '@images/dt-home-white.svg?react';

export const LINEAGE_TRANSFORMATION_NODE_NAME = 'lineage-transformation';
export const TRANSFORMATION_NODE_SIZE = 48;

// TODO: Share with LineageEntityNode
const HomeNodeBubble = styled.div`
    align-items: center;
    background-color: ${props => props.theme.styles['lineage-home-badge-bg-color']};
    border-radius: 12px;
    color: ${props => props.theme.styles['lineage-home-badge-text-color']};
    display: flex;
    font-size: 13.33px;
    font-weight: 400;
    height: 24px;
    width: 78px;
    left: -39px
    padding: 6px;
    padding-left: 5px;
    position: absolute;
    top: -26px;
`;

const NodeWrapper = styled.div<{
    selected: boolean;
    dragging: boolean;
    opacity: number;
    isGhost: boolean;
    isSearchedEntity: boolean;
    type: EntityType;
}>`
    background-color: white;
    border: 1px solid;
    border-color: ${({ selected, theme }) => (selected ? theme.styles['lineage-node-selected-border-color'] : theme.styles['lineage-node-border-color'])};
    border-radius: 4px;
    box-shadow: ${({ isSearchedEntity, theme }) =>
        isSearchedEntity ? `0 0 3px 3px ${theme.styles['primary-color']}95` : 'none'};
    opacity: ${({ opacity }) => opacity};

    align-items: center;
    display: flex;
    justify-content: center;
    height: ${TRANSFORMATION_NODE_SIZE}px;
    width: ${TRANSFORMATION_NODE_SIZE}px;
    cursor: ${({ isGhost, dragging, type }) => {
        if (isGhost) return 'not-allowed';
        if (dragging) return 'grabbing';
        if (type === EntityType.SchemaField) return 'grab';
        return 'pointer';
    }};
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.16);
    margin-top: 10px;
`;

const IconWrapper = styled.div<{ isGhost: boolean }>`
    display: flex;
    opacity: ${({ isGhost }) => (isGhost ? 0.5 : 1)};
`;

const CustomHandle = styled(Handle)<{ position: Position; $onEdge: boolean }>`
    background: initial;
    border: initial;
    top: 50%;
    left: 50%;

    ${({ position, $onEdge }) => {
        if ($onEdge && position === Position.Left) return 'left: 0;';
        if ($onEdge && position === Position.Right) return 'right: 0;';
        return '';
    }};
`;

const CustomIcon = styled.img`
    height: 24px;
    width: 24px;
`;

export default function LineageTransformationNode(props: NodeProps<LineageEntity>) {
    const { data, selected, dragging } = props;
    const { urn, type, entity, fetchStatus } = data;
    const entityRegistry = useEntityRegistryV2();
    const isQuery = type === EntityType.Query;
    const isDataProcessInstance = type === EntityType.DataProcessInstance;

    const { rootUrn } = useContext(LineageNodesContext);
    const { cllHighlightedNodes, setHoveredNode } = useContext(LineageDisplayContext);
    const { searchedEntity } = useContext(LineageVisualizationContext);

    // TODO: Support ghost queries and schema fields, once they are supported in the backend
    const ignoreSchemaFieldStatus = useIgnoreSchemaFieldStatus();
    const isGhost = isGhostEntity(entity, ignoreSchemaFieldStatus);
    const isSearchedEntity = searchedEntity === urn;

    const name = type === EntityType.SchemaField ? entity?.expandedName : entity?.name;
    const backupLogoUrl = useFetchQuery(urn); // TODO: Remove when query nodes not instantiated on column select
    const icon = entity?.icon || backupLogoUrl;

    const { selectedColumn } = useContext(LineageDisplayContext);
    const opacity = selectedColumn && !cllHighlightedNodes.has(urn) ? 0.3 : 1;

    // TODO: Combine home node code with LineageEntityNode
    const contents = (
        <NodeWrapper
            opacity={opacity}
            selected={selected}
            dragging={dragging}
            onMouseEnter={() => setHoveredNode(urn)}
            onMouseLeave={() => setHoveredNode(null)}
            data-testid={`lineage-node-${urn}`}
            isGhost={isGhost}
            isSearchedEntity={isSearchedEntity}
            type={type}
        >
            {urn === rootUrn && (
                <HomeNodeBubble>
                    <HomeIcon height={'15px'}/>
                    Home
                </HomeNodeBubble>
            )}
            <IconWrapper isGhost={isGhost}>
                {icon && <CustomIcon src={icon} />}
                {!icon && isDataProcessInstance && entityRegistry.getIcon(EntityType.DataProcessInstance, 18)}
                {!icon && isQuery && <ConsoleSqlOutlined />}
                {!icon && !isQuery && !isDataProcessInstance && (
                    <Skeleton.Avatar active shape="circle" size={TRANSFORMATION_NODE_SIZE} />
                )}
            </IconWrapper>
            {fetchStatus[LineageDirection.Upstream] === FetchStatus.LOADING && (
                <LoadingWrapper className="nodrag" style={{ left: -30 }}>
                    <Spin delay={urn === rootUrn ? undefined : 500} indicator={<LoadingOutlined />} />
                </LoadingWrapper>
            )}
            {fetchStatus[LineageDirection.Downstream] === FetchStatus.LOADING && (
                <LoadingWrapper className="nodrag" style={{ right: -30 }}>
                    <Spin delay={urn === rootUrn ? undefined : 500} indicator={<LoadingOutlined />} />
                </LoadingWrapper>
            )}
            <CustomHandle type="target" position={Position.Left} isConnectable={false} $onEdge={!isQuery} />
            <CustomHandle type="source" position={Position.Right} isConnectable={false} $onEdge={!isQuery} />
        </NodeWrapper>
    );

    if (isQuery) {
        return contents;
    }
    return <Tooltip title={name || urn}>{contents}</Tooltip>;
}

function useFetchQuery(urn: string) {
    const { nodes } = useContext(LineageNodesContext);
    const { data } = useGetQueryQuery({
        skip: nodes.has(urn),
        variables: { urn },
    });

    return data?.entity?.__typename === 'QueryEntity' && data.entity.platform?.properties?.logoUrl;
}
