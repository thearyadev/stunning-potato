import React from 'react';
import { Row } from 'reactstrap';
import Pagination from './Pagination';
import ContextMenuContainer from './ContextMenuContainer';
import DataListView from './DataListView';
import ImageListView from './ImageListView';
import ThumbListView from './ThumbListView';

function collect(props) {
  return { data: props.data };
}

const ListPageListing = ({
  items,
  selectedItems,
  onCheckItem,

}) => {
  return (
    <Row>
      {items.map((film) => {
        return (
          <ImageListView
            key={film.id}
            film={film}
            isSelect={selectedItems.includes(film.id)}
            collect={collect}
            onCheckItem={onCheckItem}
          />
        );
      })}
      
    </Row>
  );
};

export default React.memo(ListPageListing);
