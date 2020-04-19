const path = require('path');
const BrotliPlugin = require('brotli-webpack-plugin');
const Dotenv = require('dotenv-webpack');
const HtmlWebPackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');

require('dotenv-defaults').config({
  path: __dirname + '/.env',
  encoding: 'utf8',
  defaults: __dirname + '/.env.defaults',
});

const commonConfig = {
  entry: './src/index.js',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader',
        {
            'loader': 'eslint-loader', options: {
                           emitWarning: true
            },
        }],
      },
      {
        test: /\.html$/,
        exclude: /template\.html$/,
        use: {
          loader: 'html-loader',
          options: {
            minimize: true,
            removeComments: false,
            collapseWhitespace: true,
          },
        }
      },
      {
        test: /\.(png|jpg|gif)$/,
        use: 'file-loader',
      },
      {
        test: /\.less$/,
        use: ['style-loader', 'css-loader', 'less-loader'],
      },
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(woff|woff2|ttf|eot|svg|otf)(\?v=\d+\.\d+\.\d+)?$/,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/',
          }
        }
      },
      {
        test: /\.geojson$/,
        loader: 'json-loader',
      },
    ]
  },
  plugins: [
    new Dotenv({
      defaults: __dirname + '/.env.defaults',
      path: __dirname + '/.env',
    }),
    new HtmlWebPackPlugin({
      template: './src/index.html',
      title: process.env.APP_TITLE,
      filename: 'index.html',
    }),
  ],
};

if (process.env.BABEL_USE_MATERIAL_UI_ES_MODULES) {
  commonConfig.resolve = {
    alias: {
      '@material-ui/core': '@material-ui/core/es',
    },
  }
}

module.exports = (env, argv = { mode: 'development' }) => {
  switch (argv.mode) {
    default:
    case 'development': {
      return {
        ...commonConfig,
        devServer: {
          compress: process.env.WEBPACK_DEV_SERVER_COMPRESS === 'true',
          historyApiFallback: true,
          host: process.env.WEBPACK_DEV_SERVER_HOST,
          open: process.env.WEBPACK_DEV_SERVER_OPEN === 'true',
          port: process.env.WEBPACK_DEV_SERVER_PORT,
        },
        devtool: 'eval-source-map',
      }
    }

    case 'production': {
      return {
        ...commonConfig,
        output: {
          path: path.resolve(__dirname, 'build'),
          filename: '[name].[contenthash].bundle.js',
        },
        optimization: {
          splitChunks: {
            cacheGroups: {
              commons: {
                test: /[\\/]node_modules[\\/]/,
                name: 'vendors',
                chunks: 'all',
              },
            },
          },
        },
        plugins: [
          new HtmlWebPackPlugin({
            template: './src/index.html',
            title: process.env.APP_TITLE,
            filename: 'index.html',
          }),
          new webpack.DefinePlugin({
            'process.env': {
              'API_BASE_URL': JSON.stringify(process.env.API_BASE_URL)
            }
          }),
          new BrotliPlugin({
            asset: '[path].br[query]',
            test: /\.(js|css|html|svg)$/,
            threshold: 10240,
            minRatio: 0.8,
          }),
        ],
      }
    }
  }
}
