import { CHANGE_NUMBER } from '../constants';

// eslint-disable-next-line import/prefer-default-export
export const changeNumber = (number) => {
  return {
    type: CHANGE_NUMBER,
    payload: number,
  };
};
