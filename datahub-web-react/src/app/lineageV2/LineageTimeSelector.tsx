/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { CalendarOutlined, CaretDownOutlined } from '@ant-design/icons';
import { Tooltip } from '@components';
import { Button, DatePicker, Space, Typography } from 'antd';
import moment from 'moment';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import styled, { createGlobalStyle } from 'styled-components';

import { REDESIGN_COLORS } from '@app/entityV2/shared/constants';

const { RangePicker } = DatePicker;

export type Datetime = moment.Moment | null;

const ConfirmButtonWrapper = styled.div`
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
`;

const ConfirmButton = styled(Button)`
    border-radius: 6px;
    border: 1px solid ${props => props.theme.styles['outline-button-border-color']};
    color: ${props => props.theme.styles['outline-button-text-color']};

    position: absolute;
    right: 10px;
    bottom: 13px;
    text-align: right;

    :hover {
        border-color: ${REDESIGN_COLORS.BLUE};
        color: ${REDESIGN_COLORS.BLUE};
    }
`;

const StyledRangePicker = styled(RangePicker)`
`

const GlobalStyle = createGlobalStyle`
    .lineage-time-picker-popup {
        .ant-tag {
            border-color: ${props => props.theme.styles['action-chip-border-color']} !important;
            background-color: #ffffff !important;
            color: ${props => props.theme.styles['action-chip-text-color']} !important;
            border-radius: 8px !important;

            &:hover {
                border-color: ${props => props.theme.styles['action-chip-hover-border-color']} !important;
                background-color: ${props => props.theme.styles['action-chip-hover-bg-color']} !important;
            }
        }

        .ant-picker-cell::before {
            margin: 0 4px;
        }

        .ant-picker-cell-in-range > .ant-picker-cell-inner {
            background-color: ${props => props.theme.styles['action-chip-hover-bg-color']} !important;
        }

        .ant-picker-cell-range-end > .ant-picker-cell-inner,
        .ant-picker-cell-range-start > .ant-picker-cell-inner {
            background-color: ${props => props.theme.styles['filter-chip-bg-color']} !important;
            color: ${props => props.theme.styles['filter-chip-text-color']} !important;
        }

        .ant-picker-cell-today > .ant-picker-cell-inner::before {
            border-color: ${props => props.theme.styles['filter-chip-bg-color']} !important;
            border-radius: 50%;
        }

        .ant-picker-cell-range-hover-end,
        .ant-picker-cell-range-hover,
        .ant-picker-cell-range-hover-start {
            border-color: ${props => props.theme.styles['filter-chip-bg-color']} !important;
        }
    }
`;


export type Props = {
    onChange: (start: Datetime, end: Datetime) => void;
    startTimeMillis?: number;
    endTimeMillis?: number;
};

export default function LineageTimeSelector({ onChange, startTimeMillis, endTimeMillis }: Props) {
    const [startDate, setStartDate] = useState<Datetime>(startTimeMillis ? moment(startTimeMillis) : null);
    const [endDate, setEndDate] = useState<Datetime>(endTimeMillis ? moment(endTimeMillis) : null);
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const ref = useRef<any>(null);

    useEffect(() => {
        setStartDate(startTimeMillis ? moment(startTimeMillis) : null);
    }, [startTimeMillis]);

    useEffect(() => {
        setEndDate(endTimeMillis ? moment(endTimeMillis) : null);
    }, [endTimeMillis]);

    const handleOpenChange = useCallback(
        (open: boolean) => {
            setIsOpen(open);
            if (!open) {
                ref.current?.blur();
                onChange(startDate, endDate);
            }
        },
        [onChange, startDate, endDate],
    );

    const handleRangeChange = useCallback((dates: [Datetime, Datetime] | null) => {
        const [start, end] = dates || [null, null];

        start?.set({ hour: 0, minute: 0, second: 0, millisecond: 0 });
        end?.set({ hour: 23, minute: 59, second: 59, millisecond: 999 });

        setStartDate(start);
        setEndDate(end);
    }, []);

    const showText = !isOpen && (startDate === null || endDate === null);

    const [ranges] = useState<Array<[Datetime, Datetime]>>([
        [moment().subtract(7, 'days'), null],
        [moment().subtract(14, 'days'), null],
        [moment().subtract(28, 'days'), null],
        [null, null],
    ]);

    return (
        <>
            <GlobalStyle />
            {showText ? ( // Conditionally render All Time selection
                <Tooltip title="Filter lineage edges by observed date" placement="topLeft" showArrow={false}>
                    <Button type="text" onClick={() => handleOpenChange(true)}>
                        <CalendarOutlined style={{ marginRight: '4px' }} />
                        <Typography.Text>
                            <b>{getTimeRangeDescription(startDate, endDate)}</b>
                        </Typography.Text>
                        <CaretDownOutlined style={{ fontSize: '10px' }} />
                    </Button>
                </Tooltip>
            ) : (
                <Space direction="vertical" size={12}>
                    <StyledRangePicker
                        ref={ref}
                        open={isOpen}
                        allowClear
                        allowEmpty={[true, true]}
                        bordered={false}
                        value={[startDate, endDate]}
                        disabledDate={(current: any) => {
                            return current && current > moment().endOf('day');
                        }}
                        renderExtraFooter={() => (
                            <ConfirmButtonWrapper>
                                <ConfirmButton type="text" onClick={() => handleOpenChange(false)}>
                                    <b>Confirm</b>
                                </ConfirmButton>
                            </ConfirmButtonWrapper>
                        )}
                        format="ll"
                        ranges={Object.fromEntries(
                            ranges.map(([start, end]) => [getTimeRangeDescription(start, end), [start, end]]),
                        )}
                        onChange={handleRangeChange}
                        onOpenChange={handleOpenChange}
                        onCalendarChange={() => handleOpenChange(true)}
                        dropdownClassName='lineage-time-picker-popup'
                    />
                </Space>
            )}
        </>
    );
}

function getTimeRangeDescription(startDate: moment.Moment | null, endDate: moment.Moment | null): string {
    if (!startDate && !endDate) {
        return 'All Time';
    }

    if (!startDate && endDate) {
        return `Until ${endDate.format('ll')}`;
    }

    if (startDate && !endDate) {
        const dayDiff = moment().diff(startDate, 'days');
        if (dayDiff <= 30) {
            return `Last ${dayDiff} days`;
        }
        return `From ${startDate.format('ll')}`;
    }

    return 'Unknown time range';
}
