import React, { Suspense } from 'react';
import { Row } from 'reactstrap';
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

const sortingOptions = [
  { value: "DANF", label: "Date Added (Newest First)" },
  { value: "DAOF", label: "Date Added (Oldest First)" },
  { value: "UW", label: "Unwatched" },
  { value: "W", label: "Watched" },
  { value: "RATING", label: "Rating" },
  { value: "STORY", label: "Story" },
  { value: "POSITIONS", label: "Positions" },
  { value: "PUSSY", label: "Pussy" },
  { value: "SHOTS", label: "Shots" },
  { value: "HAIR", label: "Hair" },
  { value: "BOOBS", label: "Boobs" },
  { value: "BUTT", label: "Butt" },
  { value: "FACE", label: "Face" },
  { value: "REAR", label: "Rear View" },
  { valueL: "DL", label: "Downloading" }
]




const Start = ({ match }) => {
  const [sortingDropdownOpen, setSortingDropdownOpen] = useState(false);
  const toggleSortingDropdown = () => setSortingDropdownOpen(!sortingDropdownOpen)
  const films = useSelector(state => state.films.films);
  setTimeout(async () => { document.querySelectorAll(".video-listing-card").forEach(element => { element.style.visibility = "visible" }) }, 1500)
  const sort = (method) => {

  }
  return <>

    <Row>
      <Colxx xxs="12">


        <Breadcrumb heading="cinéma" match={match} style={{display: "block"}} />

        <ButtonDropdown
          className="mr-1 mb-3"
          isOpen={sortingDropdownOpen}
          toggle={toggleSortingDropdown}
          style={{display: "block"}}

        >
          <DropdownToggle caret size="xs" outline>
            <IntlMessages id="classement" />
          </DropdownToggle>
          <DropdownMenu>
            {sortingOptions.map((item) => (
              <DropdownItem key={item.value}>
                <IntlMessages id={item.label} />
              </DropdownItem>
            ))}
          </DropdownMenu>
        </ButtonDropdown>

        <Separator className="mb-5" />

      </Colxx>
    </Row>

    <Row>
      <Colxx xxs="12" className="mb-4">

        {/* this is the video library  */}
        <ListPageListing
          items={films}
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
