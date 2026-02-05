/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

/**
 * Get icon to show based on file extension
 * @param extension - the extension of the file
 * @returns string depicting the phosphor icon name
 */
export const getFileIconFromExtension = (extension: string) => {
    switch (extension.toLowerCase()) {
        case 'pdf':
            return 'FilePdf';
        case 'doc':
        case 'docx':
            return 'FileWord';
        case 'txt':
        case 'md':
        case 'rtf':
        case 'log':
        case 'json':
            return 'FileText';
        case 'xls':
        case 'xlsx':
            return 'FileXls';
        case 'ppt':
        case 'pptx':
            return 'FilePpt';
        case 'svg':
            return 'FileSvg';
        case 'jpg':
        case 'jpeg':
            return 'FileJpg';
        case 'png':
            return 'FilePng';
        case 'gif':
        case 'webp':
        case 'bmp':
        case 'tiff':
            return 'FileImage';
        case 'mp4':
        case 'wmv':
        case 'mov':
            return 'FileVideo';
        case 'mp3':
            return 'FileAudio';
        case 'zip':
        case 'rar':
        case 'gz':
            return 'FileZip';
        case 'csv':
            return 'FileCsv';
        case 'html':
            return 'FileHtml';
        case 'py':
            return 'FilePy';
        case 'java':
            return 'FileCode';
        default:
            return 'FileArrowDown';
    }
};
