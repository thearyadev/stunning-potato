import React from 'react';
import { Row } from 'reactstrap';
import IntlMessages from 'helpers/IntlMessages';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';
import { ActressTable } from 'containers/ui/ReactTableCards';
import { useSelector } from 'react-redux';
import { useState } from 'react';
import { useEffect } from 'react';

const CreateDataSet = (actresses, films) => {
  const actressDataset = [];

  actresses.forEach(actress => {
    const filmsByActress = films.filter(film => film.actresses.includes(actress));
    const watchedFilmsByActress = filmsByActress.filter(film => film.watched);
    const filmCount = watchedFilmsByActress.length;
    const totalRating = watchedFilmsByActress.reduce((sum, film) => sum + film.average, 0);
    const averageRating = (filmCount > 0 ? totalRating / filmCount : 0).toFixed(2);

    actressDataset.push({
      name: actress,
      filmCount,
      averageRating
    });
  });
  return actressDataset;
};



const Start = ({ match }) => {
  const films = useSelector(state => state.films.films);
  const actresses = useSelector(state => state.actresses.actresses);
  const [actressData, setActressData] = useState([]);
  useEffect(() => {
    setActressData(CreateDataSet(actresses, films));
  }, [films, actresses]);
  


  return (
    <>
      <Row>
        <Colxx xxs="12" className="mb-4">
          <ActressTable data={actressData} />
        </Colxx>
      </Row>
    </>
  )
};
export default Start;
