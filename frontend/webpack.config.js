const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.join(__dirname, '../nirsunitsrest/static/js/dist'),
    filename: 'bundle.js'
  }
};
