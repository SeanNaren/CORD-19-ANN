module.exports = (api) => {
  api.cache(false);

  const conditionalPresets = [];
  
  const presets = [
    [
      "@babel/env", {
        "useBuiltIns": "usage",
        "corejs": { 
          "version": "@3",
          "proposals": true,
        },
        "targets": {
          "browsers": process.env.BABEL_SUPPORTED_BROWSERS || "",
        },
      },
    ],
    "@babel/react",
    ...conditionalPresets,
  ];

  const conditionalPlugins = (process.env.BABEL_USE_MATERIAL_UI_ES_MODULES === 'true')
    ? [
        [
          "import", {
            "libraryName": "@material-ui/icons",
            "libraryDirectory": "",
            "camel2DashComponentName": false,
          },
        ],
      ]
    : [
        [
          "import", {
            "libraryName": "@material-ui/core",
            "libraryDirectory": "",
            "camel2DashComponentName": false,
          },
          "@material-ui/core",
        ],
        [
          "import", {
            "libraryName": "@material-ui/core/colors",
            "libraryDirectory": "",
            "camel2DashComponentName": false,
          },
          "@material-ui/core/colors"
        ],
        [
          "import", {
            "libraryName": "@material-ui/core/styles",
            "libraryDirectory": "",
            "camel2DashComponentName": false,
          },
          "@material-ui/core/styles"
        ],
        [
          "import", {
            "libraryName": "@material-ui/icons",
            "libraryDirectory": "",
            "camel2DashComponentName": false,
          },
          "@material-ui/icons"
        ],
      ]
  ;

  const plugins = [
    "@babel/proposal-class-properties",
    "@babel/syntax-dynamic-import",
    "@babel/transform-runtime",
    ...conditionalPlugins,
  ];

  return {
    presets,
    plugins,    
  }
}
