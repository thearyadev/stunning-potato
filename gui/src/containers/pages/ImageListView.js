import React from 'react';
import {
  Row,
  Card,
  CardBody,
  CardSubtitle,
  CardImg,
  CardText,
  CustomInput,
  Badge,
  CardHeader,
} from 'reactstrap';
import { NavLink } from 'react-router-dom';
import classnames from 'classnames';
import { ContextMenuTrigger } from 'react-contextmenu';
import { Colxx } from 'components/common/CustomBootstrap';

const ImageListView = ({ film }) => {
  return (
    <Colxx sm="6" lg="4" xl="3" className="mb-3" key={film.uuid}>
      <Card
        onClick={(event) => { }}
      >
        <div className="position-relative">
          <NavLink to={`?p=${film.uuid}`} className="w-40 w-sm-100">
            <CardImg top alt={film.title} src={film.img} />
          </NavLink>
          <Badge
            color={film.state === 'COMPLETE' ? (film.watched === true ? "success" : "danger") : (film.state === 'DOWNLOADING' ? "warning" : "secondary")}
            pill
            className="position-absolute badge-top-left"
          >
            {film.state === 'COMPLETE' ? (film.watched === true ? "WATCHED" : "UNWATCHED") : (film.state) }
          </Badge>
        </div>
        <CardBody className="p-3 pb-0">
          <Row>
            <Colxx xxs="12" className="mb-3">
              <CardText className="text-muted text-small mb-0 font-weight-light text-truncate">{film.actresses.join(", ")}</CardText>
              <CardSubtitle className="font-weight-bold pt-3 text-truncate">{film.title}</CardSubtitle>
              <div className='d-flex justify-content-between'>
                <CardText className="text-muted text-small mb-0 mt-0 pt-0 font-weight-light">
                  {film.date}
                </CardText>
                <div className="d-flex align-items-center">
                  <span className="font-weight-bold mr-2">{film.rating}</span>
                  <span className='simple-icon-star' />

                </div>
              </div>
            </Colxx>
          </Row>
        </CardBody>
      </Card>
    </Colxx>
  );
};

/* React.memo detail : https://reactjs.org/docs/react-api.html#reactpurecomponent  */
export default React.memo(ImageListView);
