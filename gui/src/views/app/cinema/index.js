import React, { Suspense } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

const Start = React.lazy(() =>
  import(/* webpackChunkName: "start" */ './start')
);
const Gogo = ({ match }) => (
  <Suspense fallback={<div className="loading" />}>
    <Switch>
      <Redirect exact from={`${match.url}/`} to={`${match.url}/cinémathèque`} />
      <Route
        path={`${match.url}/cinémathèque`}
        render={(props) => <Start {...props} />}
      />
      {/* add another route here for the player  */}
      <Redirect to="/error" />
    </Switch>
  </Suspense>
);
export default Gogo;
