const { 
  disabledForm,
  abledForm,
  resetForm,
  setForm,
  retrieveForm,
  resetFormValidation,
  formValidation,
} = require('./formFields');

const {
  setStartDateToTitle,
  setEventIDToUpdate,
} = require('./../utils');

const {
  ajaxRequest,
  addNewEventReq, updateEventReq, deleteEventReq,
} = require('./requests');

const {FormState} = require('./formState');
const formState = new FormState();

const changeFormStateToUpdate = () => {
  // при нажатии на кнопку 'изменить'
  // активируем кнопку 'применить' и блокируем кнопку 'изменитьэ
  // console.log('---- in --- changeFormStateToUpdate');
  formState.setNewState(3);
};

const openBlankForm = (data) => {
  resetForm();
  abledForm();
  resetFormValidation();
  formState.setNewState(1);
  
  const wrapData = moment(data);
  // console.log('%%% wrapData', wrapData);
  // const wrapData = moment(data).format('YYYY-MM-DD HH:mm');

  if (wrapData.isValid) {
    setStartDateToTitle(wrapData.format('YYYY-MM-DD'));
    pickTime = wrapData.format('HH:mm');

    // при клике на день выбирается 00:00 - пропускаем инициализацию времени!
    if (pickTime !== '00:00') { setForm({timeStart: pickTime}); }
  }
  openForm();
};

const openWithEventForm = (event) => {
  disabledForm();
  resetFormValidation();
  formState.setNewState(2);

  console.log('eventick', event);

  const timeStart = event['start'].format('HH:mm');
  const timeEnd = event['end'].format('HH:mm');
  setStartDateToTitle(event['start'].format('YYYY-MM-DD'));

  setEventIDToUpdate(event['id']);

  const dataFromEvent = {
    subject: event['test_object'],
    timeStart: timeStart,
    timeEnd: timeEnd,
    noteText: event['note_text'],
    distance: event['distance_num'],
    tester: event['tester_id'],
  }

  setForm(dataFromEvent);
  openForm();
};

const openForm = () => { $("#mainForm").modal('show'); };

// Обработка кнопок -!-!- Обработка кнопок
// Обработка кнопок -!-!- Обработка кнопок

const {btnDelete, btnUpdate, btnCreate,
  btnApplyUpdates, btnCancel} = require('./formButtons');

btnDelete.addEventListener('click', () => {
  console.log('btnDelete', btnDelete);

  deleteEventReq();
});

btnUpdate.addEventListener('click', () => {
  console.log('btnUpdate', btnUpdate);
  
  changeFormStateToUpdate();
});

btnCreate.addEventListener('click', () => {
  console.log('btnCreate', btnCreate);

  formValidation();
  const newEvent = retrieveForm();
  addNewEventReq(newEvent);
});

btnApplyUpdates.addEventListener('click', () => {
  console.log('btnApplyUpdates', btnApplyUpdates);
  
  formValidation();
  const newEvent = retrieveForm();
  updateEventReq(newEvent);
});

// Обработка кнопок -!-!- Обработка кнопок
// Обработка кнопок -!-!- Обработка кнопок


// test zone
// test zone

module.exports = {
  openBlankForm, openWithEventForm,
  changeFormStateToUpdate, formState
};