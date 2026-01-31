// src/store/slices/authSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
    token?: string;
}

const initialState: AuthState = {};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setToken(state, action: PayloadAction<string>) {
            state.token = action.payload;
            localStorage.setItem('access_token', action.payload);
        },
    },
});

export const { setToken } = authSlice.actions;
export default authSlice.reducer;
