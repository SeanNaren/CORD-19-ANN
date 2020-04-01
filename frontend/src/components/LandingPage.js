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
      <h1>CORD-19-ANN</h1>
      <h3 align='left'>Enter a sentence to query the nmslib search index. Results include the title of the journal and the sentence that was found ordered by similarity. If expanded the authors and the paragraph containing the sentence are shown.</h3>
      <SearchBar />
    </div>
  )
}
export default LandingPage;