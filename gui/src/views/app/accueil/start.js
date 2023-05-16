import React from 'react';
import { Row } from 'reactstrap';
import IntlMessages from 'helpers/IntlMessages';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';
import { Card, CardBody, CardTitle, CardHeader } from 'reactstrap';
import { CircularProgressbar } from 'react-circular-progressbar';
import { useEffect } from 'react';

const RadialProgressCard = ({
  title = 'title',
  percent = 50,
  isSortable = false,
}) => {
  return (
    <Card style={{ boxShadow: "none" }} className='p-0'>
      {isSortable && (
        <CardHeader className="p-0 position-relative">
          <div className="position-absolute handle card-icon">
            <i className="simple-icon-shuffle" />
          </div>
        </CardHeader>
      )}
      <CardBody className="d-flex justify-content-between align-items-center">
        <CardTitle className="mb-0">{title}</CardTitle>
        <div className="progress-bar-circle">
          <CircularProgressbar
            strokeWidth={4}
            value={percent}
            text={`${percent}%`}
          />
        </div>
      </CardBody>
    </Card>
  );
};

const Start = ({ match }) => {
  const [percent, setPercent] = React.useState(0);
  useEffect(() => {
    fetch("/api/storage")
      .then(res => res.json())
      .then(data => { setPercent((data.used / data.total) * 100); })
  }, [])


  return (
    <>
      <Row>
        <Colxx xxs="12">
          <Breadcrumb heading="accueil" match={match} />
          <Separator className="mb-5" />
        </Colxx>
      </Row>
      <Row>
        <Colxx xxs="12" className="mb-4">
          <RadialProgressCard
            title='Storage Used'
            percent={percent}
          />

        </Colxx>
      </Row>
    </>
  )
};
export default Start;
