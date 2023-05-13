import React from 'react';
import { Row } from 'reactstrap';
import IntlMessages from 'helpers/IntlMessages';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';
import ListPageListing from 'containers/pages/ListPageListing';
import ListPageHeading from 'containers/pages/ListPageHeading';
import { DropdownToggle, DropdownItem, DropdownMenu, ButtonDropdown } from 'reactstrap';
import { useState } from 'react';

const items = [
  {
    "uuid": 18,
    "title": "sexy time 1",
    // this is temp
    "img": "http://xxx.elfie.local/films/ts?id=159",
    "actresses": ["Aria Valencia", "Kenzie Love"],
    "date": "May 5, 2023",
    "watched": false,
    "state": "COMPLETE",
    "rating": 9.7
  },

]

for (let i = 0; i < 5; i += 1) {
  items.push(...items)
}


const Start = ({ match }) => {
  const [sortingDropdownOpen, setSortingDropdownOpen] = useState(false);
  const toggleSortingDropdown = () => setSortingDropdownOpen(!sortingDropdownOpen)

  const [actressFilterDropdownOpen, setActressFilterDropdownOpen] = useState(false);
  const toggleActressFilterDropdown = () => setActressFilterDropdownOpen(!actressFilterDropdownOpen)

  return <>
    <Row>
      <Colxx xxs="12">
        <ButtonDropdown
          className="mr-1 mb-3"
          isOpen={sortingDropdownOpen}
          toggle={toggleSortingDropdown}

        >
          <DropdownToggle caret size="xs" outline>
            <IntlMessages id="classement" />
          </DropdownToggle>
          <DropdownMenu>
            <DropdownItem>
              <IntlMessages id="dropdowns.another-action" />
            </DropdownItem>
            <DropdownItem>
              <IntlMessages id="dropdowns.another-action" />
            </DropdownItem>
          </DropdownMenu>
        </ButtonDropdown>

        <Separator className="mb-5" />

      </Colxx>
    </Row>

    <Row>
      <Colxx xxs="12" className="mb-4">

        {/* this is the video library  */}
        <ListPageListing
          items={items}
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
