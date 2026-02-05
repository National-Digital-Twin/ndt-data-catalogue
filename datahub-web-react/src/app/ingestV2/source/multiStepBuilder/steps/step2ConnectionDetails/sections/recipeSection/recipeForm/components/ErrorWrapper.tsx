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

export const Wrapper = styled.div`
    color: ${colors.red[500]};
    margin-top: 5px;
`;

interface Props {
    errors: React.ReactNode[];
}

export function ErrorWrapper({ errors }: Props) {
    return <Wrapper>{errors}</Wrapper>;
}
