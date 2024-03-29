import React, { Suspense } from 'react';
import { connect, useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
} from 'react-router-dom';
import { IntlProvider } from 'react-intl';
import { fetchActresses } from 'redux/actresses/actions';
import { fetchFilms } from 'redux/films/actions';

import AppLocale from './lang';
import ColorSwitcher from './components/common/ColorSwitcher';
import { NotificationContainer } from './components/common/react-notifications';
import { isMultiColorActive, adminRoot } from './constants/defaultValues';
import { getDirection } from './helpers/Utils';

const ViewApp = React.lazy(() =>
  import(/* webpackChunkName: "views-app" */ './views/app')
);

const ViewError = React.lazy(() =>
  import(/* webpackChunkName: "views-error" */ './views/error')
);

class App extends React.Component {
  constructor(props) {
    super(props);
    const completed = false;


    const direction = getDirection();
    if (direction.isRtl) {
      document.body.classList.add('rtl');
      document.body.classList.remove('ltr');
    } else {
      document.body.classList.add('ltr');
      document.body.classList.remove('rtl');
    }
  }

  componentDidMount() {
    const { FetchActresses, FetchFilms } = this.props;
    FetchActresses();
    FetchFilms();
    const intervalId = setInterval(async () => {
      if (document.hasFocus() && document.location.pathname === "/foutre/cinema/cin%C3%A9math%C3%A8que") {
        FetchActresses();
        FetchFilms();
      }
    }, 2500);
    this.intervalId = intervalId;

  }

  componentWillUnmount() {
    clearInterval(this.intervalId);
  }

  render() {
    const { locale } = this.props;
    const currentAppLocale = AppLocale[locale];
    return (
      <div className="h-100">
        <IntlProvider
          locale={currentAppLocale.locale}
          messages={currentAppLocale.messages}
        >
          <>
            <NotificationContainer />
            {isMultiColorActive && <ColorSwitcher />}
            <Suspense fallback={<div className="loading" />}>
              <Router>
                <Switch>
                  <Route
                    path={adminRoot}
                    render={(props) => <ViewApp {...props} />}
                  />
                  <Route
                    path="/error"
                    exact
                    render={(props) => <ViewError {...props} />}
                  />
                  {/* redirects / to cinema page */}

                  <Redirect exact from="/" to={`${adminRoot}/accueil`} />

                  <Redirect to="/error" />

                  <Redirect to="/error" />
                </Switch>
              </Router>
            </Suspense>
          </>
        </IntlProvider>
      </div>
    );
  }
}

const mapStateToProps = ({ settings }) => {
  const { locale } = settings;

  return { locale };
};
const mapActionsToProps = (dispatch) => {
  return {
    FetchActresses: () => dispatch(fetchActresses()),
    FetchFilms: () => dispatch(fetchFilms()),
  }
};

export default connect(mapStateToProps, mapActionsToProps)(App);
