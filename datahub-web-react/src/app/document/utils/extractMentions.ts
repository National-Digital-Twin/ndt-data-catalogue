/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

/**
 * Extracts @ mentions (URNs) from markdown text.
 * Searches for markdown link patterns like [@Entity](urn:li:entityType:id)
 *
 * @param content - The markdown content to extract mentions from
 * @returns An object containing arrays of document URNs and asset URNs
 */
export function extractMentions(content: string): { documentUrns: string[]; assetUrns: string[] } {
    if (!content) return { documentUrns: [], assetUrns: [] };

    // Match markdown link syntax: [text](urn:li:entityType:id)
    // Handle URNs with nested parentheses by matching everything between the markdown link's parens
    // The pattern matches: [text](urn:li:entityType:...) where ... can include nested parens
    // We match the URN prefix, then allow nested paren groups or non-paren characters (one or more)
    const urnPattern = /\[([^\]]+)\]\((urn:li:[a-zA-Z]+:(?:[^)(]+|\([^)]*\))+)\)/g;
    const matches = Array.from(content.matchAll(urnPattern));

    const documentUrns: string[] = [];
    const assetUrns: string[] = [];

    matches.forEach((match) => {
        const urn = match[2]; // URN is in the second capture group (inside parentheses)

        // Check if it's a document URN
        if (urn.includes(':document:')) {
            if (!documentUrns.includes(urn)) {
                documentUrns.push(urn);
            }
        } else if (!assetUrns.includes(urn)) {
            // Everything else is considered an asset
            assetUrns.push(urn);
        }
    });

    return { documentUrns, assetUrns };
}
