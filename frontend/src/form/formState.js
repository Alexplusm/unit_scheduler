const {btnUpdate, btnApplyUpdates} = require('./formButtons');
const {abledForm} = require('./formFields');

const blankStateDiv = document.querySelector('.blank-form');
const eventStateDiv = document.querySelector('.event-form');
const eventOwnerDiv = document.querySelector('.event-owner');

class FormState {
    /*
  *   1 - blank state - при создании новой записи
  *   2 - event state - когда открыто окно с информацией об записи
  *   ------
  *   3 - update state - когда изменяем существующую запись
    */
  constructor() {
    this.formState = 1;
  }

  getFormState() { return this.formState; }

  setNewState(newState) { 
    this.formState = newState;
    this.changes();
  }

  changes() {
    switch (this.formState) {
      case 1:
        blankStateDiv.classList.remove('d-none');
        eventStateDiv.classList.add('d-none');
        eventOwnerDiv.classList.add('d-none');
        break;
      case 2:
        blankStateDiv.classList.add('d-none');
        eventStateDiv.classList.remove('d-none');
        eventOwnerDiv.classList.remove('d-none');

        btnApplyUpdates.setAttribute('disabled', true);
        btnUpdate.removeAttribute('disabled');
        break;
      case 3:
        blankStateDiv.classList.add('d-none');
        eventStateDiv.classList.remove('d-none');

        btnUpdate.setAttribute('disabled', true);
        btnApplyUpdates.removeAttribute('disabled');
        
        abledForm();

        break;
    }
  };
}

module.exports = {FormState};