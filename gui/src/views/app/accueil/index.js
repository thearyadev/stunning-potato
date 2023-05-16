import React, { Suspense } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

const Start = React.lazy(() =>
  import(/* webpackChunkName: "second" */ './start')
);
const Accueil = ({ match }) => (
  <Suspense fallback={<div className="loading" />}>
    <Switch>
      <Redirect exact from={`${match.url}/`} to={`${match.url}/accueil`} />
      <Route
        path={`${match.url}/accueil`}
        render={(props) => <Start {...props} />}
      />
      <Redirect to="/error" />
    </Switch>
  </Suspense>
);
export default Accueil;
