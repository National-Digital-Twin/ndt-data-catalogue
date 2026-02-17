/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

/* eslint-disable @typescript-eslint/naming-convention */
declare module 'virtual:__federation__' {
    interface IRemoteConfig {
        url: (() => Promise<string>) | string;
        format: 'esm' | 'systemjs' | 'var';
        from: 'vite' | 'webpack';
    }

    export function __federation_method_setRemote(name: string, config: IRemoteConfig): void;

    export function __federation_method_getRemote(name: string, exposedPath: string): Promise<unknown>;

    export function __federation_method_unwrapDefault(unwrappedModule: unknown): Promise<unknown>;

    export function __federation_method_ensure(remoteName: string): Promise<unknown>;

    export function __federation_method_wrapDefault(module: unknown, need: boolean): Promise<unknown>;
}
