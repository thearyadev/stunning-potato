import { combineReducers } from 'redux';
import settings from './settings/reducer';
import menu from './menu/reducer';
import library from './library/reducer';

const reducers = combineReducers({
  menu,
  settings,
  library
});

export default reducers;
