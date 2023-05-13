import React, { Suspense } from 'react';
import { Route, withRouter, Switch, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import AppLayout from 'layout/AppLayout';

const Cinema = React.lazy(() =>
  import(/* webpackChunkName: "viwes-gogo" */ './cinema')
);
const Nouvelle = React.lazy(() =>
  import(/* webpackChunkName: "viwes-second-menu" */ './nouvelle')
);


const App = ({ match }) => {
  return (
    <AppLayout>
      <div className="dashboard-wrapper">
        <Suspense fallback={<div className="loading" />}>
          <Switch>
            {/* redirects / to /<endpoint> */}
            <Redirect exact from={`${match.url}/`} to={`${match.url}/cinema`} />
            <Route
              path={`${match.url}/cinema`}
              render={(props) => <Cinema {...props} />}
            />
            <Route
              path={`${match.url}/nouvelle`}
              render={(props) => <Nouvelle {...props} />}
            />
            {/* if no route is matched, go to error.  */}
            <Redirect to="/error" />
          </Switch>
        </Suspense>
      </div>
    </AppLayout>
  );
};

const mapStateToProps = ({ menu }) => {
  const { containerClassnames } = menu;
  return { containerClassnames };
};

export default withRouter(connect(mapStateToProps, {})(App));
