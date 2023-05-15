import React from 'react';
import { Row, Card, CardBody, CardTitle, Button } from 'reactstrap';
import { NavLink } from 'react-router-dom';
import LinesEllipsis from 'react-lines-ellipsis';
import responsiveHOC from 'react-lines-ellipsis/lib/responsiveHOC';
import Breadcrumb from 'containers/navs/Breadcrumb';
import { Separator, Colxx } from 'components/common/CustomBootstrap';
import SingleLightbox from 'components/pages/SingleLightbox';
import VideoPlayer from 'components/common/VideoPlayer';
import { blogData, blogCategories } from 'data/blog';
import IntlMessages from 'helpers/IntlMessages';
import { useState, useEffect } from 'react';
import { SliderTooltip, RangeTooltip } from 'components/common/SliderTooltips';

const Video = ({ poster, video }) => {
  return (
    <video poster={poster} controls className='card-img-top'>
      <source src={video} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  )
}

const formatTime = (totalSeconds) => {
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const formattedHours = hours.toString().padStart(2, '0');
  const formattedMinutes = minutes.toString().padStart(2, '0');
  const formattedSeconds = seconds.toString().padStart(2, '0');

  return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
}

const Player = ({ match, uuid }) => {

  const [film, setFilm] = useState(null);
  const [rating, setRating] = useState(null);
  const [userRating, setUserRating] = useState(null);

  const updateUserRating = (newValue, key) => {
    setUserRating({ ...userRating, [key]: newValue });
  }

  const saveUserRating = () => {
    fetch("/api/set_rating", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userRating)
    })
      .then(res => res.json())
      .then(data => setRating(data))
      .catch(err => {

      })
  }


  useEffect(() => {
    fetch(`/api/film?uuid=${uuid}`)
      .then(res => {
        if (res.ok) {
          return res.json();
        }
        throw new Error(`Failed to fetch film: ${res.status}`);
      })
      .then(data => {
        setFilm(data);
        return fetch(`/api/rating?uuid=${data.rating}`);
      })
      .then(res => {
        if (res.ok) {
          return res.json();
        }
        throw new Error(`Failed to fetch rating: ${res.status}`);
      })
      .then(ratingData => {
        setRating(ratingData);
        setUserRating(ratingData)
      })
      .catch(err => {
        console.error(err);
        setFilm(null);
        setRating(null);
        setUserRating(null);
      });
  }, []);


  return (<>
    {(film !== null && rating !== null) ? <Row>
      <Colxx xxs="12" md="12" xl="8" className="col-left">
        <Card className="mb-4">
          <Video
            poster={`/api/poster?uuid=${film.uuid}`}
            video={'http://xxx.elfie.local/films/v?id=863'}
          />
          <CardBody>
            <div className="d-flex justify-content-between">
              <h5 className="card-title">{film.title}</h5>
              <div>
                <Button size={'xs'} color={'secondary'} className='mr-5 ml-1'>éliminer</Button>
                <Button size={'xs'} color={'primary'} className='mr-1 ml-1' outline>télécharger</Button>
              </div>
            </div>
            <div className='separator' />
            <div className='pt-3'>
              <div className='d-flex justify-content-between'>
                <i>actrices: </i>
                <i>{film.actresses.join(", ").split(" ").map((item, key) => {
                  return <a key={key} href={`https://google.com/search?q=${item.split(" ").join("%20")}%20porn`} target="_blank" rel='noreferrer'>{item} </a>
                })}</i>
              </div>
              <div className='d-flex justify-content-between'>
                <i>Durée: </i>
                <i>{formatTime(film.duration)}</i>
              </div>
              <div className='d-flex justify-content-between'>
                <i>Date d’ajout: </i>
                <i>{film.date_added}</i>
              </div>
              <div className='d-flex justify-content-between'>
                <i>identificateur: </i>
                <i>{film.uuid}</i>
              </div>
              <div className='d-flex justify-content-between'>
                <i>évaluation: </i>
                <i>{film.rating}</i>
              </div>
            </div>
          </CardBody>
        </Card>
      </Colxx>

      <Colxx xxs="12" md="12" xl="4" className="col-left">

        <Card className="mb-4">
          <CardBody>
            <CardTitle>
              <div className='d-flex justify-content-between'>
                <h3>évaluation</h3>
                <div className="d-flex align-items-center">
                  <span className="font-weight-bold mr-2">{rating.average}</span>
                  <span className='simple-icon-star' />

                </div>
              </div>
            </CardTitle>
            {Object.entries(rating)
              .filter(([key, value]) => !["average", "uuid"].includes(key))
              .map(([key, value]) => (
                <div className="pb-3 slider-container" key={key}>
                  <p>{key}</p>
                  <SliderTooltip
                    min={0}
                    max={10}
                    defaultValue={value}
                    className="mb-5"
                    step={1}
                    toolTipInnerClassName="rating-tooltip"
                    onChange={(newValue) => updateUserRating(newValue, key)}
                  />
                </div>
              ))}
            <div className='d-flex justify-content-center'>
              <Button size={'xs'} color={'primary'} className='mr-1 ml-1' outline onClick={saveUserRating}>enregistrer</Button>
            </div>
          </CardBody>
        </Card>
      </Colxx>
    </Row> : <div className="loading" />}
  </>)
};
export default Player;
