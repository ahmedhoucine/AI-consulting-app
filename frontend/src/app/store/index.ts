import { ActionReducerMap } from "@ngrx/store";
import { AuthenticationState, authenticationReducer } from "./Authentication/authentication.reducer";
import { LayoutState, layoutReducer } from "./layouts/layouts.reducer";
import { defaultDayOfMonthOrdinalParse } from "ngx-bootstrap/chronos/locale/locale.class";


export interface RootReducerState {
    layout: LayoutState;
    auth: AuthenticationState;

}

export const rootReducer: ActionReducerMap<RootReducerState> = {
    layout: layoutReducer,
    auth: authenticationReducer,

}