import React from 'react';
import { Row } from 'reactstrap';
import IntlMessages from 'helpers/IntlMessages';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';
import { Card, CardBody, CardTitle, CardHeader } from 'reactstrap';
import { CircularProgressbar } from 'react-circular-progressbar';
import { useEffect } from 'react';
import data from 'data/iconCards';
import IconCard from 'components/cards/IconCard';
import GradientWithRadialProgressCard from 'components/cards/GradientWithRadialProgressCard';



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
  const [diagnosticData, setDiagnosticData] = React.useState([]);
  const [downloadersStatus, setDownloadersStatus] = React.useState([]);

  const [loading, setLoading] = React.useState(true);
  useEffect(() => {
    fetch("/api/diagnostics")
      .then(res => res.json())
      .then(d => { setDiagnosticData(d) })
      .then(() => fetch("/api/downloaders")
        .then(res => res.json())
        .then(d => { setDownloadersStatus(d) })
        .then(() => setLoading(false))
        )
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
        <Colxx xxs="12" className="">
          <Row className="icon-cards-row mb-2">
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Cache Size', icon: "iconsminds-arrow-refresh", value: `${Math.round(diagnosticData?.cache_size/1000/1000)} MB` }} className="mb-4 w-100" />
            </Colxx>
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Database Size', icon: "iconsminds-arrow-refresh", value: `${diagnosticData?.database?.size} MB` }} className="mb-4 w-100" />
            </Colxx>
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Database Query Time', icon: "iconsminds-arrow-refresh", value: `${Math.round(diagnosticData?.database?.query_time * 1000)} MS` }} className="mb-4 w-100" />
            </Colxx>
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Storage Total', icon: "iconsminds-arrow-refresh", value: `${diagnosticData?.disk?.total} GB`}} className="mb-4 w-100" />
            </Colxx>
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Storage Used', icon: "iconsminds-arrow-refresh", value: `${diagnosticData?.disk?.used} GB`}} className="mb-4 w-100" />
            </Colxx>
            <Colxx xxs="6" sm="4" md="3" lg="2">
              <IconCard {...{ title: 'Storage Free', icon: "iconsminds-arrow-refresh", value: `${diagnosticData?.disk?.free} GB`}} className="mb-4 w-100" />
            </Colxx>
          </Row>
        </Colxx>
      </Row>
      <Row>
        {downloadersStatus.map((d, i) => {
          return (
            <Colxx lg="4" md="6" className="mb-4" key={i}>
              <GradientWithRadialProgressCard
                
                icon="simple-icon-cloud-download"
                title={`${d.aliases[0]}`}
                detail={`Container ID: ${d.aliases[d.aliases.length - 1]}`}
                percent={100}
                progressText="Online"
                net={`Network: ${d.ip_address} ${d.mac_address}`}
              />
        </Colxx>
          )
        })}

    
      </Row>
    </>
  )
};
export default Start;
