---
description: "Use when creating or modifying Redux Toolkit stores, slices, selectors, thunks, RTK Query APIs, or React-Redux hooks. Covers store structure, immutable updates, async logic, and performance."
applyTo: ["**/{store,slices,features,redux}/**/*.{js,jsx,ts,tsx}", "**/*{Slice,slice,Store,store,Api,api}.{js,ts}"]
---

# Redux Guidelines

- Always use Redux Toolkit (`@reduxjs/toolkit`) instead of plain `redux`: `configureStore`, `createSlice`, `createAsyncThunk`, `createSelector`. Never use legacy `createStore`, `combineReducers` boilerplate, switch-case reducers, or hand-written action types and creators. Install `@reduxjs/toolkit` and `react-redux` only; do not add `redux-thunk`, `redux-saga`, or `redux-devtools-extension` (already built in or unnecessary).
- Pass reducers directly to `configureStore({ reducer: { feature: featureReducer } })`; keep the default middleware (thunk, immutability and serializability checks) and extend it with `getDefaultMiddleware().concat(...)` rather than replacing it.
- Export action creators and the reducer from each slice (`export const { added } = slice.actions; export default slice.reducer;`), and name actions as events that happened (`todoAdded`), not setters.
- Use `createListenerMiddleware` for reactive side effects, and `extraReducers` with the builder callback syntax for thunk and API actions.
- Export `RootState` and `AppDispatch` types from the store (`store.getState`, `store.dispatch`) and use them for typed hooks.
- Use Redux only for shared, app-wide state; keep local UI state in `useState` or `useReducer`, and server data in RTK Query or the project's existing data layer.
- Organize by feature: each feature folder holds its slice, selectors, and API in one place, and the store is configured in a single `store` module.
- Write reducers with Immer's mutating syntax inside `createSlice` only; never mutate state elsewhere, and keep state serializable (no functions, class instances, or promises).
- Keep state minimal and normalized (`createEntityAdapter` for collections), and derive values with selectors instead of storing them.
- Use typed hooks (`useAppDispatch`, `useAppSelector`) defined once, and select the smallest slice of state needed to avoid extra re-renders.
- Memoize derived selectors with `createSelector`, and never return new objects or arrays from `useSelector` without memoization.
- Handle async logic with `createAsyncThunk` or RTK Query using `async`/`await`; model `pending`, `fulfilled`, and `rejected` states, and handle errors explicitly.
- Use RTK Query (`createApi`) for all server data fetching and caching instead of manual fetch-and-store thunks or copying fetched data into slices.
- Define one API slice per base URL with `createApi` and `fetchBaseQuery`, and split endpoints across files with `injectEndpoints`; add the API `reducer` and `middleware` to the store.
- Use `builder.query` for reads and `builder.mutation` for writes, and use the generated hooks (`useGetItemsQuery`, `useAddItemMutation`) in components.
- Use `providesTags` and `invalidatesTags` for cache invalidation so lists refresh after mutations; prefer `onQueryStarted` optimistic updates (`updateQueryData`) with rollback on failure.
- Handle `isLoading`, `isFetching`, `isError`, and `error` states in the UI, and use `skip` or `skipToken` for conditional queries; use `selectFromResult` to limit re-renders.
- Read the base URL and auth headers from environment variables and `prepareHeaders`; never hard-code tokens.
- Set `keepUnusedDataFor`, `refetchOnFocus`/`refetchOnReconnect` (with `setupListeners`), and polling intervals deliberately for each endpoint.
- Use `transformResponse` to shape data once and `transformErrorResponse` for consistent errors, and add TypeScript generics for result and argument types when the project uses TypeScript.
- Do not duplicate RTK Query data in slices or `useState`; read it through hooks or selectors.
- Put side effects in thunks or listener middleware, not in reducers.
- Wrap the app in `<Provider store={store}>` once, near the root.
- Use Redux Toolkit in all large React projects (many routes, shared state across distant components, complex async data, multiple teams) so state, caching, and data flow stay predictable. Skip it in small apps where `useState`, `useReducer`, and `useContext` are enough; if a small app grows, migrate to Redux Toolkit rather than building a custom store.
- Always use the modern Redux Toolkit way, never plain Redux: no `createStore`, no `connect`/`mapStateToProps`, no `redux-thunk`/`redux-saga` setup, no manual `switch` reducers. Use `useSelector`/`useDispatch` through the typed hooks.
- When migrating existing plain Redux code, change one slice at a time with `createSlice`, keep the existing state shape and action type strings, and keep the app working between steps; do not rewrite the whole store at once.
- Define each slice with a `name`, `initialState`, and `reducers`; use `prepare` callbacks for actions that need generated payloads (ids, timestamps) so reducers stay pure.
- Create the store through a `makeStore()`/`setupStore(preloadedState)` function when tests or SSR need isolated stores, and export `RootState` from `ReturnType<typeof store.getState>`.
- Use `combineSlices` or the `reducer` object map to register slices, and use `createAsyncThunk` with `rejectWithValue` for typed failures plus `condition` to skip duplicate requests.
- Use `createEntityAdapter` selectors (`selectAll`, `selectById`) for normalized collections, and use `createSelector` with input selectors only for derived data.
- Use `createApi` `tagTypes` for every cached resource and keep tag names consistent; use `providesTags` with ids (`[{ type: 'Post', id }, { type: 'Post', id: 'LIST' }]`) for fine-grained invalidation.
- Prefer RTK Query `useQuery` hooks over `useEffect` fetching; use `usePrefetch` for likely next navigations and `lazy` query hooks for user-triggered requests.
- Use `fixedCacheKey` for mutations whose result is shared across components, and `.unwrap()` on mutation and thunk results inside `try`/`catch` for success and error handling.
- Use `baseQuery` wrappers for cross-cutting concerns such as re-auth on 401 and retry (`retry` from RTK Query), instead of repeating logic in each endpoint.
- Test slices as pure reducers, selectors as pure functions, and components with a fresh store from `setupStore`; mock the network at the boundary (MSW or the project's tool) for RTK Query.
- Add debugging for state: use Redux DevTools in development, log failed thunks and API errors with context (endpoint name, arguments without secrets), and never leave `console.log` calls inside reducers.
- Keep Redux DevTools enabled in development only, and do not log or persist secrets in state.
- Make focused changes that preserve existing state shape and action names.
