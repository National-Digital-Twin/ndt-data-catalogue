/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import { BADGE } from '@geometricpanda/storybook-addon-badges';
import type { Meta, StoryObj } from '@storybook/react';
import React from 'react';

import { FileDragAndDropArea } from '.';

// Auto Docs
const meta = {
    title: 'Forms / FileDragAndDropArea',
    component: FileDragAndDropArea,

    // Display Properties
    parameters: {
        layout: 'centered',
        badges: [BADGE.STABLE],
        docs: {
            subtitle:
                'FileDragAndDropArea is a component that allows users to drag and drop files or click to upload files.',
        },
    },

    // Component-level argTypes
    argTypes: {
        onFilesUpload: {
            description: 'Function to call when files are uploaded',
            table: {
                defaultValue: { summary: 'undefined' },
            },
            action: 'filesUploaded',
        },
        className: {
            description: 'Additional CSS class name(s) to apply to the component',
            control: { type: 'text' },
        },
    },

    // Define defaults
    args: {
        onFilesUpload: (files: File[]) => {
            console.log('Files uploaded:', Array.from(files));
            // Simulate async operation
            return Promise.resolve();
        },
    },
} satisfies Meta<typeof FileDragAndDropArea>;

export default meta;

// Stories
type Story = StoryObj<typeof meta>;

// Basic story is what is displayed 1st in storybook & is used as the code sandbox
// Pass props to this so that it can be customized via the UI props panel
export const sandbox: Story = {
    tags: ['dev'],
    render: (props) => <FileDragAndDropArea {...props} />,
};

// Example story showing the basic usage
export const basic = () => (
    <FileDragAndDropArea
        onFilesUpload={(files) =>
            new Promise((resolve) => {
                console.log('Files:', files);
                resolve();
            })
        }
    />
);
