const path = require('path');const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry:'./src/index.js', //This property defines where the application starts
  output: {
    path: path.join(__dirname, '/dist'),
    filename: 'bundle.js' }, //This property defines the file path and the file name which will be used for deploying the bundled file
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  }, //Setup loaders
  plugins: [
    new HtmlWebpackPlugin({ template: './src/index.html' })
  ]
}

