import React, { Suspense } from 'react';
import { Container, Row } from 'reactstrap';
import IntlMessages from 'helpers/IntlMessages';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';
import ListPageListing from 'containers/pages/ListPageListing';
import ListPageHeading from 'containers/pages/ListPageHeading';
import { DropdownToggle, DropdownItem, DropdownMenu, ButtonDropdown } from 'reactstrap';
import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchActresses, setActresses } from 'redux/actresses/actions';
import { Button } from 'reactstrap';
import { setIn } from 'formik';


const Start = ({ match }) => {
  const [indexedFilms, setIndexedFilms] = useState([])
  const [loaded, setLoaded] = useState(false);
  setTimeout(async () => { document.querySelectorAll(".video-listing-card").forEach(element => { element.style.visibility = "visible" }) }, 1500)

  useEffect(() => {
    if (!loaded) {
      fetch("/api/indexed")
        .then(response => response.json())
        .then(data => {
          setIndexedFilms(data)
          setLoaded(true)
        }).catch(error => console.log(error))
    }
  })


  return <>
    <Row>
      <Colxx xxs="12">


        <Breadcrumb heading="nouvelle" match={match} style={{ display: "block" }} />


        <Separator className="mb-5" />

      </Colxx>
    </Row>

    <Row>
      <Colxx xxs="12" className="mb-4">

        {/* this is the video library  */}
        <ListPageListing
          items={indexedFilms}
          displayMode={"imagelist"}
          selectedItems={[]}
          onCheckItem={() => { }}
          currentPage={1}
          totalPage={10}
          onContextMenuClick={() => { }}
          onChangePage={() => { }}
        />
      </Colxx>
    </Row>
  </>
};
export default Start;
