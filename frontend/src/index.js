const {fullCalendar} = require('./calendar');
const {initForm} = require('./form/formFields');
const {dateTimePickerSetup} = require('./form/formInit');

const {
    csrfSafeMethod, unit_js, unit_name_js, logined_user
  } = require('./utils');

// global test
// global test

// запуск календаря
document.addEventListener("DOMContentLoaded", () => {
    dateTimePickerSetup();
    fullCalendar();
    initForm();
});
// $(document).ready(fullCalendar());
// запуск календаря


function confirmDelete() {
    $("#eventInfo").modal('hide');
    $("#confirmDelete").modal('show');
}


function eventList(){
    $.ajax({

        type: "GET",

        url: "../../unit_schedule/",

        data: {"unit": unit_js},
            
        cache: false,

        success: function(data){
                console.log(data);                  
            },
        color: 'yellow',
        textColor: 'black'
    },)
}

Notify = {              
    TYPE_INFO: 0,               
    TYPE_SUCCESS: 1,                
    TYPE_WARNING: 2,                
    TYPE_DANGER: 3,                             

    generate: function (aText, aOptHeader, aOptType_int) {                  
        var lTypeIndexes = [this.TYPE_INFO, this.TYPE_SUCCESS, this.TYPE_WARNING, this.TYPE_DANGER];                    
        var ltypes = ['alert-info', 'alert-success', 'alert-warning', 'alert-danger'];                                      
        var ltype = ltypes[this.TYPE_INFO];                 

        if (aOptType_int !== undefined && lTypeIndexes.indexOf(aOptType_int) !== -1) {                      
            ltype = ltypes[aOptType_int];                   
        }                                       

        var lText = '';                 
        if (aOptHeader) {                       
            lText += "<h4>"+aOptHeader+"</h4>";                 
        }                   
        lText += "<p>"+aText+"</p>";                                        
        var lNotify_e = $("<div class='alert "+ltype+"'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>×</span></button>"+lText+"</div>");                    

        setTimeout(function () {                        
            lNotify_e.alert('close');                   
        }, 3000);                   
        lNotify_e.appendTo($("#notifies"));             
    }           
};  

function check_user(user_full_name) {

    let ownerOrNot = document.getElementById('ownerOrNot');
    if (user_full_name == logined_user) {
        ownerOrNot.style.cssText = "display: none";
        $('#updateButton').prop('disabled',false);
        $('#deleteButton').prop('disabled',false);
        // $('#updateButton').removeClass('disabled').addClass('active');
    } else {
        ownerOrNot.style.cssText = "display: block";
        $('#updateButton').prop('disabled',true);
        $('#deleteButton').prop('disabled',true);
    }
}