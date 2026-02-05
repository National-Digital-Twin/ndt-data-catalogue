/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

export enum LinkFormVariant {
    URL = 'url',
    UploadFile = 'uploadFile',
}

export interface LinkFormData {
    variant: LinkFormVariant;
    url: string;
    fileUrl: string;

    label: string;

    showInAssetPreview: boolean;
}

export interface GeneralizedLinkFormData {
    url: string;
    label: string;

    showInAssetPreview: boolean;
}
