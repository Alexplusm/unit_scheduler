const {openBlankForm, openWithEventForm} = require('./form/form');
const {
  csrfSafeMethod, unit_js, unit_name_js, logined_user
} = require('./utils');

// setup params
const minTime = '09:00:00';
const maxTime = '22:30:00';
// setup params

const fullCalendar = function() {

  $('#calendar').fullCalendar({

      locale: 'ru',
      minTime: minTime,
      maxTime: maxTime,

      defaultView: 'agendaWeek',

      events: {
        // type: "GET",

        // * old version
        // url: "../../unit_schedule/",
        // data: {"unit": unit_js},

        // * new version
        url: `../../event_list/${unit_js}`,

        // cache: false,
        success: function(data){
            console.log('init data', data);                
        },
        textColor: 'black',
      },

      header: {
          left: 'prev next',
          center: 'title',
          right: 'month,agendaWeek,agendaDay'
      },

      eventClick:  function(event) {
        // существующий эвент - event
        openWithEventForm(event);
      },

      dayClick: function(date) {
        // прокидываем дату и время клетки, по которой кликнули
        openBlankForm(date.format());
      },
  });
}  

module.exports = {fullCalendar};