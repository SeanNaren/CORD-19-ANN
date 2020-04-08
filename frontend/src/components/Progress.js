import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import LinearProgress from '@material-ui/core/LinearProgress';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    '& > * + *': {
      marginLeft: theme.spacing(2),
    },
  },
}));

export default function SearchLinearProgress() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <LinearProgress color="secondary"/>
    </div>
  );
}