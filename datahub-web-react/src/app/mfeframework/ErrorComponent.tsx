/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div<{ isV2: boolean }>`
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 480px;
    background-color: ${(props) => (props.isV2 ? '#f5f5f5' : '#fafafa')};
    border: 2px dashed ${(props) => (props.isV2 ? '#d9d9d9' : '#e8e8e8')};
    border-radius: 8px;
    color: ${(props) => (props.isV2 ? '#595959' : '#666')};
    font-size: 16px;
    text-align: center;
    padding: 20px;
`;

export const ErrorComponent = ({ isV2, message }: { isV2: boolean; message: string }) => {
    return <ErrorContainer isV2={isV2}>{message}</ErrorContainer>;
};
