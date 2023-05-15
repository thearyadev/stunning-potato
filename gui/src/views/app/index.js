import React, { Suspense } from 'react';
import { Route, withRouter, Switch, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { useSelector } from 'react-redux';
import AppLayout from 'layout/AppLayout';
import { adminRoot } from 'constants/defaultValues';
import {useState, useEffect} from 'react';

const Cinema = React.lazy(() =>
  import(/* webpackChunkName: "viwes-gogo" */ './cinema')
);
const Nouvelle = React.lazy(() =>
  import(/* webpackChunkName: "viwes-second-menu" */ './nouvelle')
);

const Actrices = React.lazy(() =>
  import(/* webpackChunkName: "viwes-second-menu" */ './actrices')
);


const App = ({ match }) => {
  const films = useSelector((state) => state.films.films);
  const [showRoutes, setShowRoutes] = useState(false);

  useEffect(() => {
    // Show the routes after 2 seconds
    const timerId = setTimeout(() => {
      setShowRoutes(true);
    }, 1);

    // Clear the timer if the component is unmounted before it finishes
    return () => clearTimeout(timerId);
  }, []);

  return (
    <AppLayout>
      <div className="dashboard-wrapper">
        {showRoutes ? (
          <Suspense fallback={<div className="loading" />}>
            <Switch>
              {/* redirects / to /<endpoint> */}
              <Route
                path={`${match.url}/cinema`}
                render={(props) => <Cinema {...props} />}
              />
              <Route
                path={`${match.url}/nouvelle`}
                render={(props) => <Nouvelle {...props} />}
              />
              <Route
              path={`${match.url}/actrices`}
              render={(props) => <Actrices {...props} />}
              />
              {/* if no route is matched, go to error.  */}
            </Switch>
          </Suspense>
        ) : (
          <div className="loading" />
        )}
      </div>
    </AppLayout>
  );
};


const mapStateToProps = ({ menu }) => {
  const { containerClassnames } = menu;
  return { containerClassnames };
};

export default withRouter(connect(mapStateToProps, {})(App));
