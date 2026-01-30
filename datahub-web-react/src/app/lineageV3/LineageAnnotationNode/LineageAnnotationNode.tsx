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

export const LINEAGE_ANNOTATION_NODE = 'lineage-annotation-node';

const Container = styled.div`
    background-color: ${colors.gray[1500]};
    border-radius: 200px;
    color: ${colors.gray[1700]};
    padding: 4px 6px;
`;

interface AnnotationNodeData {
    label: string;
}

interface Props {
    data: AnnotationNodeData;
}

export default function AnnotationNode({ data }: Props) {
    return <Container>{data.label}</Container>;
}
