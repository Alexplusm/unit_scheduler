function dateTimePickerSetup () {
  $(function () {

    $('#timepickerStart').datetimepicker({
        format: 'HH:mm',
        stepping: 15,
    });

    $('#timepickerEnd').datetimepicker({
      format: 'HH:mm',
      stepping: 15,
    });

    $('#datepickerEnd').datetimepicker({
      format: 'YYYY-MM-DD',
      minDate: moment(),
      defaultDate: moment(),
      useStrict: true,
    });
  });
};
module.exports = {dateTimePickerSetup};