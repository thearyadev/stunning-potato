import { Row } from 'reactstrap';
import { Colxx, Separator } from 'components/common/CustomBootstrap';
import Breadcrumb from 'containers/navs/Breadcrumb';


import React, { createRef, useState } from 'react';
import {
  Card, CardBody, FormGroup, Label, Spinner, InputGroup,
  InputGroupAddon, CustomInput
} from 'reactstrap';
import { Wizard, Steps, Step } from 'react-albus';
import { injectIntl } from 'react-intl';
import { Formik, Form, Field } from 'formik';
import IntlMessages from 'helpers/IntlMessages';
import BottomNavigation from 'components/wizard/BottomNavigation';
import TopNavigation from 'components/wizard/TopNavigation';



const validatePopulated = (value) => {
  let error;
  if (!value) {
    error = 'Please fill out this field';
  }
  return error;
};

const validateDuration = (value) => {
  let error;
  if (!value) {
    error = 'Please enter a duration';

  } else if (value.length < 8) {
    error = 'This input is malformed.';
  }
  return error;
};


const Validation = ({ intl }) => {
  const forms = [createRef(null), createRef(null), createRef(null)];
  const [bottomNavHidden, setBottomNavHidden] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fields, setFields] = useState({
    title: '',
    duration: '',
    actresses: '',
    film_poster: '',
    film_file: '',
  });

  const onClickNext = (goToNext, steps, step) => {
    if (steps.length - 1 <= steps.indexOf(step)) {
      return;
    }
    const formIndex = steps.indexOf(step);
    const form = forms[formIndex].current;

    form.submitForm().then(() => {
      if (!form.isDirty && form.isValid) {
        const newFields = { ...fields, ...form.values };
        setFields(newFields);




        if (steps.length - 2 <= steps.indexOf(step)) {
          // done
          setBottomNavHidden(true);
          setLoading(true);
          console.log(newFields);
          // do api call

          const formData = new FormData();
          Object.keys(newFields).forEach(key => {
            formData.append(key, newFields[key]);
          });

          fetch("/api/upload", {
            method: "POST",
            body: formData,
          })
          .then(response => {
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          })

          setTimeout(() => {
            setLoading(false);
          }, 3000);
        }
        goToNext();
        step.isDone = true;
      }
    });
  };

  const onClickPrev = (goToPrev, steps, step) => {
    if (steps.indexOf(step) <= 0) {
      return;
    }
    goToPrev();
  };

  return (
    <Card>
      <CardBody className="wizard wizard-default">
        <Wizard onStepChange={() => {console.log("balls")}}>
          <TopNavigation className="justify-content-center" disableNav />
          <Steps>
            <Step
              id="step1"
              name="Step 1"
              desc="Film Details"
            >
              <div className="wizard-basic-step">
                <Formik
                  innerRef={forms[0]}
                  initialValues={{
                    title: fields.title,
                    duration: fields.duration,
                    actresses: fields.actresses,
                  }}
                  validateOnMount
                  onSubmit={() => { }}
                >
                  {({ errors, touched }) => (
                    <Form className="av-tooltip tooltip-label-right">
                      <FormGroup>
                        <Label>Title</Label>
                        <Field
                          className="form-control"
                          name="title"
                          validate={validatePopulated}
                        />
                        {errors.name && touched.name && (
                          <div className="invalid-feedback d-block">
                            {errors.name}
                          </div>
                        )}
                      </FormGroup>

                      <FormGroup>
                        <Label>Duration</Label>
                        <Field
                          className="form-control"
                          name="duration"
                          validate={validateDuration}
                        />
                        {errors.name && touched.name && (
                          <div className="invalid-feedback d-block">
                            {errors.name}
                          </div>
                        )}
                      </FormGroup>
                      <FormGroup>
                        <Label>Actresses</Label>
                        <Field
                          className="form-control"
                          name="actresses"

                        />
                        {errors.name && touched.name && (
                          <div className="invalid-feedback d-block">
                            {errors.name}
                          </div>
                        )}
                      </FormGroup>


                    </Form>
                  )}
                </Formik>
              </div>
            </Step>
            <Step
              id="step2"
              name="Step 2"
              desc="Artwork"
            >
              <div className="wizard-basic-step">
                <Formik
                  innerRef={forms[1]}
                  initialValues={{
                    
                  }}
                  onSubmit={() => { }}
                  validateOnMount
                >
                  {({ errors, touched }) => (
                    <Form className="av-tooltip tooltip-label-right">
                      <FormGroup>
                        <InputGroup className="mb-3">
                          <InputGroupAddon addonType="prepend">Artwork</InputGroupAddon>
                          <CustomInput
                            type="file"
                            id="posterFileBrowser"
                            name="film_poster"
                            accept=".png, .jpg, .jpeg"
                            onChange={(event) => {
                              const file = event.target.files[0];
                              setFields((prevState) => ({
                                ...prevState,
                                film_poster: file,
                              }))
                            }}
                          />
                        </InputGroup>
                      </FormGroup>
                    </Form>
                  )}
                </Formik>
              </div>
            </Step>
            <Step
              id="step3"
              name="Step 3"
              desc="Upload File"
            >
              <div className="wizard-basic-step">
                <Formik
                  innerRef={forms[2]}
                  initialValues={{
                  }}
                  onSubmit={() => { }}
                  validateOnMount
                >
                  {({ errors, touched }) => (
                    <Form className="av-tooltip tooltip-label-right error-l-75">
                      <FormGroup>
                      <InputGroup className="mb-3">
                          <InputGroupAddon addonType="prepend">Film File</InputGroupAddon>
                          <CustomInput
                            type="file"
                            id="posterFileBrowser"
                            name="film_poster"
                            accept=".mp4"
                            onChange={(event) => {
                              const file = event.target.files[0];
                              setFields((prevState) => ({
                                ...prevState,
                                film_file: file,
                              }))
                            }}
                          />
                        </InputGroup>
                      </FormGroup>
                    </Form>
                  )}
                </Formik>
              </div>
            </Step>
            <Step id="step4" hideTopNav>
              <div className="wizard-basic-step text-center pt-3">
                {loading ? (
                  <div>
                    <Spinner color="primary" className="mb-1" />
                    <p>
                      <IntlMessages id="Adding Film To Library" />
                    </p>
                  </div>
                ) : (
                  <div>
                    <h2 className="mb-2">
                      <IntlMessages id="Successfully Added Film" />
                    </h2>
                  </div>
                )}
              </div>
            </Step>
          </Steps>
          <BottomNavigation
            onClickNext={onClickNext}
            onClickPrev={onClickPrev}
            className={`justify-content-center ${bottomNavHidden && 'invisible'
              }`}
            prevLabel="Previous"
            nextLabel="Next"
          />
        </Wizard>
      </CardBody>
    </Card>
  );
};

const Start = ({ match }) => {


  return (
    <>
      <Row>
        <Colxx xxs="12">
          <Breadcrumb heading="Upload" match={match} />
          <Separator className="mb-5" />
        </Colxx>
      </Row>
      <Row>
        <Colxx xxs="12" className="">
          <Validation />
        </Colxx>
      </Row>
    </>
  )
};
export default Start;
