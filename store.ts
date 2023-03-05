import {applyMiddleware, createStore, Store} from 'redux';
import {createWrapper, Context} from 'next-redux-wrapper';
import reducer from './reducers';
import { composeWithDevTools } from 'redux-devtools-extension';
import thunk from "redux-thunk";

// create a makeStore function
export const store = createStore(reducer, {}, composeWithDevTools(applyMiddleware(thunk)));
const initStore = (context: Context) => store;
// export an assembled wrapper
export const wrapper = createWrapper<Store<any>>(initStore, {debug: true});