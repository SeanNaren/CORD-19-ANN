import React from 'react'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { CssBaseline } from '@material-ui/core'
import * as Themes from './themes'
import LandingPage from './components/LandingPage'

function App() {
  return (
    <MuiThemeProvider theme={createMuiTheme(Themes['light'])}>
      <CssBaseline />
      <LandingPage />
    </MuiThemeProvider>
  )
}

export default App
