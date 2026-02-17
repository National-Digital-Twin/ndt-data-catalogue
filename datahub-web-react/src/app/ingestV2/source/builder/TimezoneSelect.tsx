/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { SimpleSelect } from '@components';
import moment from 'moment-timezone';
import React from 'react';
import styled from 'styled-components';

const SelectContainer = styled.div`
    max-width: 300px;
`;

type Props = {
    value: string;
    onChange: (newTimezone: any) => void;
};

export const TimezoneSelect = ({ value, onChange }: Props) => {
    const timezones = moment.tz.names();
    const options = timezones.map((timezone) => {
        return {
            value: timezone,
            label: timezone,
        };
    });

    return (
        <SelectContainer>
            <SimpleSelect
                options={options}
                showSearch
                onUpdate={(values) => onChange(values[0])}
                initialValues={[value]}
                showClear={false}
                width="full"
            />
        </SelectContainer>
    );
};
