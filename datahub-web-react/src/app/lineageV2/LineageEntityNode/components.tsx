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
import styled from 'styled-components';

export const ExpandContractButton = styled.div<{ expandOnHover?: boolean }>`
    background-color: white;
    border: 1px solid ${(props) => props.theme.styles['lineage-arrow-border-color']};
    border-radius: 50%;
    color: ${(props) => props.theme.styles['lineage-arrow-icon-color']};
    cursor: pointer;
    padding: 3px;
    display: flex;
    font-size: 18px;
    position: absolute;
    top: 50%;

    max-width: 25px;
    overflow: hidden;

    :hover {
        ${(props) => props.expandOnHover && `max-width: 50px;`}
        ${(props) => props.expandOnHover && `border-radius: 4px;`}
    }
`;

export const UpstreamWrapper = styled(ExpandContractButton)`
    right: calc(100% - 5px);
    transform: translateY(-50%) rotate(180deg);
`;

export const DownstreamWrapper = styled(ExpandContractButton)`
    left: calc(100% - 5px);
    transform: translateY(-50%);
`;

export const Button = styled.span`
    border-radius: inherit;
    line-height: 0;

    :hover {
        background-color: ${(props) => props.theme.styles['lineage-arrow-hover-bg-color']};
    }
`;
