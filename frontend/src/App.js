import React from 'react'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { CssBaseline } from '@material-ui/core'
import * as Themes from './themes'
import LandingPage from './components/LandingPage'
import TitleAppBar from './components/TitleAppBar'
function App() {
  return (
    <MuiThemeProvider theme={createMuiTheme(Themes['light'])}>
      <CssBaseline />
      <TitleAppBar />
      <LandingPage />
    </MuiThemeProvider>
  )
}

export default App
