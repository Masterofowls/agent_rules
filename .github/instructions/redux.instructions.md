---
description: "Use when creating or modifying Redux Toolkit stores, slices, selectors, thunks, RTK Query APIs, or React-Redux hooks. Covers store structure, immutable updates, async logic, and performance."
applyTo: ["**/{store,slices,features,redux}/**/*.{js,jsx,ts,tsx}", "**/*{Slice,slice,Store,store,Api,api}.{js,ts}"]
---

# Redux Guidelines

- Use Redux Toolkit (`configureStore`, `createSlice`, `createAsyncThunk`, `createSelector`), never legacy `createStore` or hand-written reducers and action types.
- Use Redux only for shared, app-wide state; keep local UI state in `useState` or `useReducer`, and server data in RTK Query or the project's existing data layer.
- Organize by feature: each feature folder holds its slice, selectors, and API in one place, and the store is configured in a single `store` module.
- Write reducers with Immer's mutating syntax inside `createSlice` only; never mutate state elsewhere, and keep state serializable (no functions, class instances, or promises).
- Keep state minimal and normalized (`createEntityAdapter` for collections), and derive values with selectors instead of storing them.
- Use typed hooks (`useAppDispatch`, `useAppSelector`) defined once, and select the smallest slice of state needed to avoid extra re-renders.
- Memoize derived selectors with `createSelector`, and never return new objects or arrays from `useSelector` without memoization.
- Handle async logic with `createAsyncThunk` or RTK Query using `async`/`await`; model `pending`, `fulfilled`, and `rejected` states, and handle errors explicitly.
- Use RTK Query (`createApi`) for data fetching and caching, with tags for invalidation, instead of manual fetch-and-store thunks.
- Put side effects in thunks or listener middleware, not in reducers.
- Wrap the app in `<Provider store={store}>` once, near the root.
- Keep Redux DevTools enabled in development only, and do not log or persist secrets in state.
- Make focused changes that preserve existing state shape and action names.
