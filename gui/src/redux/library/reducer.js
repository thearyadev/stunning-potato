import { CHANGE_NUMBER } from '../constants';

const INIT_STATE = {
  number: 12
};

export default (state = INIT_STATE, action) => {
  switch (action.type) {
    case CHANGE_NUMBER:
      return { ...state, locale: action.payload };
    
    default:
      return { ...state };
  }
};
