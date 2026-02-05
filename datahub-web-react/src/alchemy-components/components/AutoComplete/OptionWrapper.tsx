/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React, { useEffect, useRef } from 'react';

interface Props {
    children: React.ReactNode;
}

export function OptionWrapper({ children }: Props) {
    const wrapperRef = useRef<HTMLDivElement>(null);

    // FYI: This effect overrides a default behavior of antd autocomplent of selecting option by hovering
    // Antd handles mouse move to select option but doesn't unselect option by mouse leave
    useEffect(() => {
        const targetElement = wrapperRef?.current?.closest('.ant-select-item-option');

        if (targetElement) {
            const handleMouseMove = (event: Event) => {
                event.stopPropagation();
            };

            const handleMouseEnterNative = () => {
                targetElement.classList.add('ant-select-item-option-active');
            };

            const handleMouseLeaveNative = () => {
                targetElement.classList.remove('ant-select-item-option-active');
            };

            targetElement.addEventListener('mousemove', handleMouseMove);
            targetElement.addEventListener('mouseenter', handleMouseEnterNative);
            targetElement.addEventListener('mouseleave', handleMouseLeaveNative);

            return () => {
                targetElement.removeEventListener('mousemove', handleMouseMove);
                targetElement.removeEventListener('mouseenter', handleMouseEnterNative);
                targetElement.removeEventListener('mouseleave', handleMouseLeaveNative);
            };
        }

        return undefined;
    }, []);

    return <div ref={wrapperRef}>{children}</div>;
}
