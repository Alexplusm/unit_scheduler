const csrfSafeMethod = (method) => {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

const beforeAjaxSend = (xhr, settings) => {
  console.log('robit');
  let csrftoken = Cookies.get('csrftoken');
  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
  }
}


const unit_js = document.getElementById("unitId").value;
const unit_name_js = document.getElementById("unitName").value;
const logined_user = document.getElementById("loginedUser").value;

const startDate = document.getElementsByName('pick-start-date')[0];

const setStartDateToTitle = (newDate) => {
  startDate.textContent = newDate;
}

const getStartDateFromTitle = () => {
  return startDate.textContent;
}

const returnDistanceID = (distance) => {
  if (distance === 'Большое') {return 3;}
  if (distance === 'Среднее') {return 2;}
  if (distance === 'Малое') {return 1;}
}

let eventID = null;

const setEventIDToUpdate = (newID) => {
  eventID = newID;
}

const getEventID = () => {
  return eventID;
}


module.exports = {
  beforeAjaxSend,
  unit_js, unit_name_js, logined_user,
  returnDistanceID,
  setStartDateToTitle, getStartDateFromTitle,
  setEventIDToUpdate, getEventID,
}