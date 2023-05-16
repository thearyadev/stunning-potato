import { adminRoot } from './defaultValues';
// import { UserRole } from "helpers/authHelper"

const data = [
  {
    id: 'accueil',
    icon: 'iconsminds-home-1',
    label: 'accueil',
    to: `${adminRoot}/accueil`,
  },
  {
    id: 'films',
    icon: 'simple-icon-film',
    label: 'cinéma',
    to: `${adminRoot}/cinema`,
  },
  {
    id: 'catalogue',
    icon: 'simple-icon-map',
    label: 'nouvelle',
    to: `${adminRoot}/nouvelle`,
  },
  {
    id: 'actresses',
    icon: 'simple-icon-symbol-female',
    label: 'actrices',
    to: `${adminRoot}/actrices`,
  },
  
];
export default data;
