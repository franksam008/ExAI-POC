// src/store/slices/workflowSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { WorkflowNode } from '../../api/workflowApi';

interface WorkflowState {
    nodes: WorkflowNode[];
}

const initialState: WorkflowState = {
    nodes: [],
};

const workflowSlice = createSlice({
    name: 'workflow',
    initialState,
    reducers: {
        setNodes(state, action: PayloadAction<WorkflowNode[]>) {
            state.nodes = action.payload;
        },
    },
});

export const { setNodes } = workflowSlice.actions;
export default workflowSlice.reducer;
