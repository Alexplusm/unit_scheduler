const timeSeqErr = document.getElementsByName('time-sequence-error')[0];
const errors = [timeSeqErr];

const showError = (error) => {
  if (error = 'TSE') {
    console.log('error - TSE', timeSeqErr);
    timeSeqErr.style.display = 'block';
  }
}

const hideError = (error) => {
  if (error = 'TSE') {
    timeSeqErr.style.display = 'none';
  }
}

const hideErrors = () => {
  errors.forEach(el => {
    el.style.display = 'none';
  });
}

module.exports = {showError, hideErrors, hideError};