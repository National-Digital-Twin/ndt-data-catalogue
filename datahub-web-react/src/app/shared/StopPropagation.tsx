/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React, { PropsWithChildren } from 'react';

/**
 * Unstyled Component that prevents event propagation. Useful for preventing clicks from propagating to parent elements.
 */
export const StopPropagation = (props: PropsWithChildren<any>) => (
    <span
        aria-hidden="true"
        onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
        }}
        {...props}
    />
);
