import React, { memo } from 'react';
import IntlMessages from 'helpers/IntlMessages';
import { useSelector } from 'react-redux';
import { useState, useEffect } from 'react';


import {
  Row,
  Card,
  CardBody,
  Nav,
  NavItem,
  Button,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownItem,
  DropdownMenu,
  TabContent,
  TabPane,
  Badge,
  CardTitle,
  CardSubtitle,
  CardText,
  CardImg,
} from 'reactstrap';
import { NavLink } from 'react-router-dom';
import classnames from 'classnames';
import Breadcrumb from 'containers/navs/Breadcrumb';
import { Colxx } from 'components/common/CustomBootstrap';
import SingleLightbox from 'components/pages/SingleLightbox';
import recentPostsData from 'data/recentposts';
import RecentPost from 'components/common/RecentPost';
import productData from 'data/products';
import UserCardBasic from 'components/cards/UserCardBasic';
import friendsData from 'data/follow';
import { useHistory } from 'react-router-dom/cjs/react-router-dom';
import LazyLoad from 'react-lazyload';
import { RadarChart } from 'components/charts';
import { ThemeColors } from 'helpers/ThemeColors';
import { act } from 'react-dom/test-utils';
import RadialProgressCard from 'components/cards/RadialProgressCard';
import { Separator } from 'components/common/CustomBootstrap';
import { Container, Col } from 'reactstrap';

const ActressDetail = ({ match, actress }) => {
  const actresses = useSelector(state => state.actresses.actresses);
  const films = useSelector(state => state.films.films);
  const [actressData, setActressData] = useState(null);
  const [actressFilms, setActressFilms] = useState(null);

  useEffect(() => {
    setActressData(actresses.find(actressS => actressS.name === actress));
    setActressFilms(films.filter(film => film.actresses.includes(actress)));

  }, [null])

  const history = useHistory();
  return (
    <>
      {actressData && actressFilms && <Row>

        <Colxx xxs="12">
          <Row>
            <Colxx xxs="12">
              <Breadcrumb heading={actressData.name} match={match} />
              <Separator className="mb-5" />
            </Colxx>
          </Row>

          <Row>
            <Colxx xxs="12" lg="4" className="mb-4 col-left">
              <Card className="mb-4">
                <CardBody>
                  <CardTitle>
                    <IntlMessages id="performance" />
                  </CardTitle>
                  <div className="remove-last-border remove-last-margin remove-last-padding">
                    <RadialProgressCard
                      className=""
                      title="average"
                      percent={actressData.average}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="story"
                      percent={actressData.story}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="positions"
                      percent={actressData.positions}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="pussy"
                      percent={actressData.pussy}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="shots"
                      percent={actressData.shots}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="boobs"
                      percent={actressData.boobs}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="face"
                      percent={actressData.face}
                      isSortable={false}
                    />
                    <RadialProgressCard
                      className=""
                      title="rearview"
                      percent={actressData.rearview}
                      isSortable={false}
                    />
                  </div>
                </CardBody>
              </Card>
            </Colxx>

            <Colxx xxs="12" lg="8" className="mb-4 col-right">
              {/* PRODS */}
              <Container style={{ height: '77vh', overflowY: 'scroll' }} className='of-style-none'>
                <Row>
                  {actressFilms.map((film) => {
                    return (
                      <Colxx
                        xxs="12"
                        lg="6"
                        xl="4"
                        className="mb-4"
                        key={film.uuid}
                      >
                        <Card onClick={() => { history.replace(`../cinema/cinémathèque/${film.uuid}`) }}>
                          <div className="position-relative">
                            <NavLink
                              to="#"
                              location={{}}
                              className="w-40 w-sm-100"
                            >
                                <CardImg
                                  top
                                  alt={film.title}
                                  src={`/api/thumbnail?uuid=${film.uuid}`}
                                />
                            </NavLink>
                          </div>
                          <CardBody>
                            <NavLink
                              to="#"
                              location={{}}
                              className="w-40 w-sm-100"
                            >
                              <CardSubtitle>{film.title}</CardSubtitle>
                            </NavLink>
                            <CardText className="text-muted text-small mb-0 font-weight-light">
                              {film.date_added}
                            </CardText>
                          </CardBody>
                        </Card>
                      </Colxx>
                    );
                  })}
                </Row>
              </Container>


            </Colxx>
          </Row>


        </Colxx>
      </Row>}
    </>
  );
};
export default memo(ActressDetail);
