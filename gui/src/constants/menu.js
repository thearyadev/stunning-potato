import { adminRoot } from './defaultValues';
// import { UserRole } from "helpers/authHelper"

const data = [
  {
    id: 'films',
    icon: 'simple-icon-film',
    label: 'cinéma',
    to: `${adminRoot}/cinema`,
  },
  {
    id: 'catalogue',
    icon: 'simple-icon-map',
    label: 'Nouvelle',
    to: `${adminRoot}/nouvelle`,
  },
];
export default data;
