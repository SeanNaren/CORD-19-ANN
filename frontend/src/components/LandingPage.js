import React from 'react'
import SearchBar from './SearchBar'
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  root: {
    padding: '32px 22px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  }
}));

function LandingPage() {
  const classes = useStyles();


  return (
    <div className={classes.root}>
      <h3 align='left'>Enter a sentence to query the index. Results include the title of the journal and the sentence that was found ordered by similarity. More details are shown if expanded.</h3>
      <SearchBar />
    </div>
  )
}
export default LandingPage;