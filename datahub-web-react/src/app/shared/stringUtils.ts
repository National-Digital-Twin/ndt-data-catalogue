/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

/**
 * Converts kebab-case string to PascalCase
 * @example convertToPascalCase("magnifying-glass") → "MagnifyingGlass"
 * @example convertToPascalCase("user-profile") → "UserProfile"
 */
export function convertToPascalCase(str: string): string {
    return str
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join('');
}

/**
 * Converts kebab-case string to camelCase
 * @example convertToCamelCase("magnifying-glass") → "magnifyingGlass"
 * @example convertToCamelCase("user-profile") → "userProfile"
 */
export function convertToCamelCase(str: string): string {
    const parts = str.split('-');
    if (parts.length === 0) return str;

    return (
        parts[0] +
        parts
            .slice(1)
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join('')
    );
}

/**
 * Converts PascalCase or camelCase string to kebab-case
 * @example convertToKebabCase("MagnifyingGlass") → "magnifying-glass"
 * @example convertToKebabCase("userProfile") → "user-profile"
 */
export function convertToKebabCase(str: string): string {
    return str
        .replace(/([a-z])([A-Z])/g, '$1-$2')
        .replace(/([A-Z])([A-Z][a-z])/g, '$1-$2')
        .toLowerCase();
}
