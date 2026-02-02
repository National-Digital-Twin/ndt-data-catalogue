/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
import React from 'react';

export type StepKey = string;

export interface Step {
    label: string;
    subTitle?: React.ReactNode;
    key: StepKey;
    content: React.ReactNode;
    completedByDefault?: boolean;
}

export type OnNextHandler = () => void;

export interface MultiStepFormContextType<TState, TStep extends Step = Step, TSubmitOptions = any> {
    steps: TStep[];
    state: TState;
    updateState: (newState: Partial<TState>) => void;

    submit: (options?: TSubmitOptions) => void;
    cancel: () => void;

    totalSteps: number;
    currentStepIndex: number;
    getCurrentStep: () => TStep | undefined;

    canGoToNext: () => boolean;
    setOnNextHandler: (handler: OnNextHandler | undefined) => void;
    goToNext: () => void;
    canGoToPrevious: () => boolean;
    goToPrevious: () => void;
    goToStep: (key: StepKey) => void;
    isStepVisited: (key: StepKey) => boolean;
    isFinalStep: () => boolean;

    isStepCompleted: (stepKey: StepKey) => boolean;
    isCurrentStepCompleted: () => boolean;
    setCurrentStepCompleted: () => void;
    setCurrentStepUncompleted: () => void;

    isDirty: () => boolean;
}

export type OnCancelArguments = {
    isDirty?: boolean;
};

export interface MultiStepFormProviderProps<TState, TSubmitOptions = any> {
    steps: Step[];
    initialState?: TState;
    onSubmit?: (state: TState | undefined, options?: TSubmitOptions | undefined) => Promise<void>;
    onCancel?: (args: OnCancelArguments) => void;
    isDirtyChecker?: (initialState: TState | undefined, state: TState | undefined) => boolean;
}
