// src/app/store.ts
import { configureStore } from '@reduxjs/toolkit';
import { useDispatch, TypedUseSelectorHook, useSelector } from 'react-redux';
import workflowReducer from '../store/slices/workflowSlice';
import authReducer from '../store/slices/authSlice';
import dataReducer from '../store/slices/dataSlice';
import modelReducer from '../store/slices/modelSlice';
import serviceReducer from '../store/slices/serviceSlice';
import monitorReducer from '../store/slices/monitorSlice';
import systemReducer from '../store/slices/systemSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        data: dataReducer,
        workflow: workflowReducer,
        model: modelReducer,
        service: serviceReducer,
        monitor: monitorReducer,
        system: systemReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
