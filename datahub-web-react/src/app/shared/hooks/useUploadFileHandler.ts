/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import { notification } from '@components';
import { useCallback } from 'react';

import { validateFile } from '@components/components/Editor/extensions/fileDragDrop';
import { FileUploadFailureType } from '@components/components/Editor/types';

import useFileUpload from '@app/shared/hooks/useFileUpload';
import useFileUploadAnalyticsCallbacks from '@app/shared/hooks/useFileUploadAnalyticsCallbacks';

import { UploadDownloadScenario } from '@types';

interface Props {
    scenario: UploadDownloadScenario;
    assetUrn?: string;
    schemaField?: string;
}

export function useUploadFileHandler(props: Props) {
    const { uploadFile: onFileUpload } = useFileUpload(props);
    const analyticsCallbacks = useFileUploadAnalyticsCallbacks(props);

    const handleFileUpload = useCallback(
        async (file: File) => {
            try {
                analyticsCallbacks.onFileUploadAttempt?.(file.type, file.size, 'button');

                const validation = validateFile(file);

                if (!validation.isValid) {
                    console.error(validation.error);
                    analyticsCallbacks.onFileUploadFailed?.(
                        file.type,
                        file.size,
                        'button',
                        validation.failureType || FileUploadFailureType.UNKNOWN,
                    );
                    notification.error({
                        message: 'Upload Failed',
                        description: validation.displayError || validation.error,
                    });

                    return null; // Skip invalid file
                }

                // Upload file if handler exists
                if (onFileUpload) {
                    try {
                        const finalUrl = await onFileUpload(file);
                        analyticsCallbacks.onFileUploadSucceeded?.(file.type, file.size, 'button');
                        return finalUrl;
                    } catch (uploadError) {
                        console.error(uploadError);
                        analyticsCallbacks.onFileUploadFailed?.(
                            file.type,
                            file.size,
                            'button',
                            FileUploadFailureType.UNKNOWN,
                            `${uploadError}`,
                        );
                        notification.error({
                            message: 'Upload Failed',
                            description: 'Something went wrong',
                        });
                        return null;
                    }
                }

                return null;
            } catch (error) {
                console.error(error);
                analyticsCallbacks.onFileUploadFailed?.(
                    file.type,
                    file.size,
                    'button',
                    FileUploadFailureType.UNKNOWN,
                    `${error}`,
                );
                notification.error({
                    message: 'Upload Failed',
                    description: 'Something went wrong',
                });

                return null;
            }
        },
        [analyticsCallbacks, onFileUpload],
    );

    return handleFileUpload;
}
