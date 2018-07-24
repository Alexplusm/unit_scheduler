const {showError, hideError} = require('./formValidationMsg');

const form = document.forms['mainForm'];

const subjectField = form['subject'];
const timeStartField = form['timeStart'];
const timeEndField = form['timeEnd'];

const noteTextArea = form['noteText'];

const distanceField = form['distance'];
const testerField = form['tester'];

const dateEndField = form['dateEnd'];

const formElements = [
  subjectField, timeStartField, timeEndField,
];
const formTimeElements = [timeStartField, timeEndField];
const formElementsForValidation = [noteTextArea, distanceField, testerField]
  .concat(formElements);

const setForm = ({ subject,
                  timeStart,
                  timeEnd,
                  noteText,
                  distance, 
                  tester, }) => {

  subjectField.value = (subject) ? subject : null;
  noteTextArea.value = (noteText ? noteText : null);
  timeStartField.value = (timeStart) ? timeStart : null;
  timeEndField.value = (timeEnd) ? timeEnd : null;

  testerField.selectedIndex = (tester) ? tester : null;
  distanceField.selectedIndex = (distance) ? distance : null;
};

const resetForm = () => {
  formElements.forEach(el => {
    el.value = null;
  });

  testerField.value = -1;
  distanceField.value = -1;
};

const resetFormValidation = () => {
  formElementsForValidation.forEach(el => {
    el.classList.remove('is-invalid');
    el.classList.remove('is-valid');
  })
}

const disabledForm = () => {
  formElements.forEach(el => {
    el.setAttribute("disabled", true);
  });

  noteTextArea.setAttribute("disabled", true);
  testerField.setAttribute("disabled", true);
  distanceField.setAttribute("disabled", true);
};

const abledForm = () => {
  formElements.forEach(el => {
    el.removeAttribute('disabled');
  });

  noteTextArea.removeAttribute('disabled');
  testerField.removeAttribute('disabled');
  distanceField.removeAttribute('disabled');
};

const retrieveForm = () => {
  const formObj = {
    subjectField: subjectField.value,
    noteTextArea: noteTextArea.value,
    timeStartField: timeStartField.value,
    timeEndField: timeEndField.value,

    testerField: testerField.value,
    distanceField: distanceField.value
  }
  console.log('-- FORM', formObj);
  return formObj;
}

const formValidation = () => {
  let validFlag = true;
  
  formElementsForValidation.forEach(el => {
    if (el.value === '' || el.value === '-1') {
      addIsInvalid(el);
      validFlag = false;
    } else { addIsValid(el); }
  });

  timeValidation();
  dateValidation();

  if (validFlag === false) {return validFlag;}

  console.log('befor return - validFlag', validFlag);
  return validFlag;
};

const timeValidation = () => {
  const start = timeStartField.value;
  const end = timeEndField.value;
  let flag = false;

  if (start && end) {

    const [startHourNum, startMinNum] = start.split(':');
    const [endHourNum, endMinNum] = end.split(':');

    // проверка на то, что событие "сначала начинается, а потом заканчивается"
    flag = (endHourNum < startHourNum) ? false 
      : ((startHourNum === endHourNum) && (endMinNum <= startMinNum)) ? false : true ;
    
    // показываем ошибки
    if (flag === false) {
      formTimeElements.forEach(el => addIsInvalid(el));
      showError('TSE');
    }
  }
  return flag;
};

const dateValidation = () => {
  console.log('dateEndField', dateEndField.value);
  const re = /\d{4}-\d{2}-\d{2}/;
  console.log('regexppp - test', re.test(dateEndField.value));

}

const initForm = () => {
  subjectField.addEventListener('focus', () => {
    subjectField.classList.remove('is-invalid');
  });

  timeStartField.addEventListener('focus', () => {
    timeStartField.classList.remove('is-invalid');
    hideError('TSE');
  });

  timeEndField.addEventListener('focus', () => {
    timeEndField.classList.remove('is-invalid');
    hideError('TSE');
  });


  noteTextArea.addEventListener('focus', () => {
    noteTextArea.classList.remove('is-invalid');
  });

  distanceField.addEventListener('focus', () => {
    distanceField.classList.remove('is-invalid');
  });

  testerField.addEventListener('focus', () => {
    testerField.classList.remove('is-invalid');
  });
}

const addIsValid = (el) => {
  el.classList.remove('is-invalid');
  el.classList.add('is-valid');
}
const addIsInvalid = (el) => {
  el.classList.remove('is-valid');
  el.classList.add('is-invalid');
}

module.exports = {
  disabledForm, abledForm, resetForm,
  setForm, retrieveForm,
  formValidation, initForm, resetFormValidation
};