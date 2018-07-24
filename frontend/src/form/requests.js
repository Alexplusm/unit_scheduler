const {
  beforeAjaxSend,
  unit_js, returnDistanceID,
  getStartDateFromTitle, getEventID,
} = require('./../utils');

const addNewEventReq = (newEvent) => {
  $.ajax({
    beforeSend: beforeAjaxSend,
    
    type: "POST",
    // url: "../../unit_schedule/",
    url: `../../event_list/${unit_js}`,

    data: preparationDataToSend(newEvent),

    success: function(data){
      console.log(data);
      location.reload();
      Notify.generate('Вы записались!', 'Успех', 1)
    },

    error: function(data){
      console.log(data.responseText);
      Notify.generate(data.responseText, 'Error', 3)
    }
  });
}

const updateEventReq = (eventToUpdate) => {

  $.ajax({
    beforeSend: beforeAjaxSend,
    type: "PUT",
    url: "../../unit_schedule/" + getEventID() + "/",

    data: dataToUpdate(eventToUpdate),

    success: function(){
      console.log("update success");
      // location.reload();
    },

    error: function(){
      console.log("update error");
      location.reload();
    }
  });
}

const deleteEventReq = () => {
  $.ajax({
    beforeSend: beforeAjaxSend,
    type: "DELETE",

    url: `../../event_detail/${getEventID()}`,
    // url: "../../unit_schedule/" + getEventID() + "/",
    
    success: function(){
      // $("#confirmDelete").modal('hide');
      console.log("успешный Delete (new version)");
      location.reload();
    },

    error: function(){
      console.error("delete error");
      location.reload();
    }
  });
}


const preparationDataToSend = (event) => {
  return {
    "unit": unit_js,
    // "start_work": "2018-01-05 14:00"
    "start_work": getStartDateFromTitle() + ' ' + event['timeStartField'],
    // нужен конец испытания конец
    "end_work": getStartDateFromTitle() + ' ' + event['timeEndField'],
    "tester": event['testerField'],
    "distance": returnDistanceID(event['distanceField']),
    "test_object": event['subjectField'],
    "note_text": event['noteTextArea'],
  };
}

const dataToUpdate = (event) => {
  const dataObj = preparationDataToSend(event);
  dataObj['event_id'] = getEventID();
  return dataObj;

}

module.exports = {
  addNewEventReq, updateEventReq, deleteEventReq
};