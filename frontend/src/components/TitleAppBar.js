import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(() => ({
    appRoot: {
      flexGrow: 1,
    },
    appTitle: {
      flexGrow: 1,
    },
    appBar: {
      alignItems: 'center',
      backgroundColor: '#c13164',
    }
}));

export default function TitleAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.appRoot}>
      <AppBar position="static" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h6" className={classes.appTitle}>
            CORD-19-ANN
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
  );
}