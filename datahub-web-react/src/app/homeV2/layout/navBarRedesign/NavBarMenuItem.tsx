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
import { Menu, MenuItemProps, theme, Tooltip } from 'antd';
import React from 'react';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';

import { NavBarMenuBaseItem } from '@app/homeV2/layout/navBarRedesign/types';
import { Badge, Text } from '@src/alchemy-components';
import analytics, { EventType } from '@src/app/analytics';

const StyledMenuItem = styled(Menu.Item)<{ isCollapsed?: boolean }>`
    &&& {
        position: relative;
        padding: 4px 12px;
        margin-top: 8px;
        height: 56px;
        min-height: 36px;
        border-radius: 6px;
        border: 0;
        display: flex;
        align-items: center;
        ${(props) => props.isCollapsed && 'width: 56px;'}
        @media (max-height: 970px) {
            margin: 2px 0;
        }
        @media (max-height: 890px) {
            margin: 0;
        }
    }

    && svg {
        color: ${({ theme }) => theme.styles['icon-selected']};
        width: 20px;
        height: 20px;
    }

    && .ant-menu-title-content {
        width: 100%;
        color: ${({ theme }) => theme.styles['nav-item-text']};
        font-family: Mulish;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: 36px;
        display: flex;
        gap: 8px;
        align-items: center;
        height: 36px;
        line-height: 24px;
    }

    &:hover,
    &.ant-menu-item-active {
        background-color: ${({ theme }) => theme.styles['nav-item-hover']};
    }

    &&.ant-menu-item-selected {
        background-color: ${({ theme }) => theme.styles['nav-item-hover']};
        box-shadow: 0px 0px 0px 1px rgba(108, 71, 255, 0.08);
    }
`;

const Icon = styled.div<{ $isSelected?: boolean; $size?: number }>`
    width: ${(props) => props.$size ?? 20}px;
    height: ${(props) => props.$size ?? 20}px;

    && svg {
        ${(props) =>
            props.$isSelected
                ? `color: ${({ theme }) => theme.styles['icon-selected']};`
                : 'color: #ffffff;'}
        width: ${(props) => props.$size ?? 20}px;
        height: ${(props) => props.$size ?? 20}px;
    }
`;

const StyledText = styled(Text)<{ $isSelected?: boolean }>`
    ${(props) =>
        props.$isSelected &&
        `color: ${({ theme }) => theme.styles['nav-item-text']};`}
`;

const ItemTitleContentWrapper = styled.div`
    width: 100%;
    display: flex;
    justify-content: space-between;
`;

const PillDot = styled.div<{ $isSelected?: boolean }>`
    position: absolute;
    width: 10px;
    height: 10px;
    background: ${(props) => props.theme.styles['primary-color']};
    border-radius: 6px;
    border: 2px solid ${(props) => (props.$isSelected ? '#f9fafc' : '#f2f3fa')};
    top: 6px;
    left: 22px;
`;

type Props = {
    item: NavBarMenuBaseItem;
    isCollapsed?: boolean;
    isSelected?: boolean;
    iconSize?: number;
} & MenuItemProps;

export default function NavBarMenuItem({ item, isCollapsed, isSelected, iconSize, ...props }: Props) {
    const history = useHistory();

    const onClick = () => {
        analytics.event({ type: EventType.NavBarItemClick, label: item.title });
        if (item.onClick) item.onClick();
        if (item.link) return history.push(item.link);
        return null;
    };

    const component = (
        <Tooltip title={isCollapsed ? item.title : null} placement="right" showArrow={false}>
            <StyledMenuItem
                isCollapsed={isCollapsed}
                onClick={onClick}
                aria-label={item.title}
                {...props}
                data-testid={item.dataTestId}
            >
                {item.icon || item.selectedIcon ? (
                    <Icon $size={iconSize} $isSelected={isSelected}>
                        {isSelected ? item.selectedIcon || item.icon : item.icon}
                    </Icon>
                ) : null}
                {isCollapsed ? (
                    <>{item?.badge?.show && <PillDot />}</>
                ) : (
                    <ItemTitleContentWrapper>
                        <StyledText size="md" type="div" weight="normal" $isSelected={isSelected}>
                            {item.title}
                        </StyledText>
                        {item?.badge?.show && <Badge count={item.badge.count} clickable={false} color="primary" />}
                    </ItemTitleContentWrapper>
                )}
            </StyledMenuItem>
        </Tooltip>
    );

    if (item.href) {
        return <a href={item.href}>{component}</a>;
    }

    return component;
}
