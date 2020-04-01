# CORD-19-ANN

Below are instructions on how to setup the front-end for the search capabilities.

## Table of Contents:
  - [Table of Contents:](#Table-of-Contents)
  - [Prerequisites](#Prerequisites)
  - [Setup](#Setup)
  - [Babel & Webpack Configuration](#Babel--Webpack-Configuration)
    - [Configuration using Environment Variables](#Configuration-using-Environment-Variables)
    - [Babel Configuration](#Babel-Configuration)
    - [Development and Production Build Modes](#Development-and-Production-Build-Modes)
      - [Development Builds](#Development-Builds)
      - [Production Build](#Production-Build)
  - [Docker Deployment](#Docker-Deployment)

## Prerequisites
The following tools are required to set up or run this template:
- [node](https://nodejs.org/) v12.4.0
- [npm](https://www.npmjs.com/) v6.9.0 **or** [Yarn](https://yarnpkg.com/) v1.16.0 

## Setup
1. Clone the repo 
2. Navigate to the root directory of this new repo and run either of the commands below:
```shell
npm install
```
3. You'll need to modify the `.env.defaults` file to point to the URL of the search index. We've assumed you've ran the `index_server.py` on the appropriate node as explained in the README.
 
A blank *.env* file is also created in the root directory (more on environment variables [here](#configuration-using-environment-variables)).

## Babel & Webpack Configuration

### Configuration using Environment Variables
The *webpack.config.js* uses the [dotenv-webpack](https://www.npmjs.com/package/dotenv-webpack) plugin alongside [dotenv-defaults](https://www.npmjs.com/package/dotenv-defaults) to expose any environment variables set in the *.env* or *.env.defaults* file in the root directory. These variables are available within the webpack configuration itself and also anywhere within the application in the format `process.env.[VARIABLE]`.

The root *.env.defaults* file must only contain non-sensitive configuration variables and should be considered safe to commit to any version control system.

Any sensitive details, such as passwords or private keys, should be stored in the root *.env* file. This file should **never** be committed and accordingly is already listed within the root *.gitignore* file. The *.env* file also serves to overwrite any non-sensitive variables defined within the root *.env.defaults* file.

### Babel Configuration
This project uses [Babel](https://babeljs.io/) to convert, transform and polyfill ECMAScript 2015+ code into a backwards compatible version of JavaScript.

As with *webpack.config.js* the environmental variables defined in *.env.defaults* and *.env* are available within the *babel.config.js* where Babel's configuration is programmatically created. 

### Development and Production Build Modes
In *webpack.config.js* there's a common configuration object for both `development` and `production` builds called `commonConfig` which mainly handles loading for various file types. Extend this object with any modules or plugins which apply to both build modes.

Within a switch statement after the `commonConfig` object individual properties for both the `development` and `production` builds can be defined separately as needed.

Webpack will use the `--mode` flag it recieves when run to determine which build to bundle. This flag defaults to `development`.

#### Development Builds
A `development` build can be run in the following ways:
```shell
// with npm
npm run dev
// or
npm run dev:hot

// with yarn
yarn run dev
// or
yarn run dev:hot
```
Both the `dev` and `dev:hot` scripts use [webpack-dev-server](https://webpack.js.org/configuration/dev-server/) to serve a `development` build locally. Some options are configured already in the root *.env.defaults* and can be overriden in the root *.env* file or within the root *webpack.config.js* itself as required.

#### Production Build
A `production` build can be run by the following command:
```
// with npm
npm run build

// with yarn
yarn run build
```
The `build` script will write an optimized and compressed build to the 'build' directory. If a different directory is required it will mean changing the *.package.json*'s `clean` script as well as the `output.path` property of the *webpack.config.json* accordingly.


## Docker Deployment
In order to run the project locally on Docker, first you need to run the backend. Please follow the instruction below to run the backend.
Once your backend is up and running, you need to open a new tab on your terminal and navigate to the root of the project and run `docker-compose up` in your terminal (you need to have Docker installed on your machine before running this script). If the command is succesfully executed then you should be able to navigate to the project in your browser on `localhost:8080`.
