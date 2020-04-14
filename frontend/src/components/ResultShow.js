import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import MuiExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import MuiExpansionPanel from '@material-ui/core/ExpansionPanel';
import MuiExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import CustomizedTabs from './ResultCard'

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        padding: '10px 5px'
    },
    heading: {
        fontSize: theme.typography.pxToRem(18),
        fontWeight: 500,
        flexBasis: '33.33%',
        flexShrink: 0,
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(13),
        color: theme.palette.text.secondary,
    },
    searchTitle: {
        padding: '28px 5px'
    },
    authors: {
        display: 'flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        paddingBottom: '16px'
    },
    expansionDetails: {
        display: 'flex',
        flexDirection: 'column',
    }
}));

const ExpansionPanel = withStyles({
  root: {
    marginBottom: '10px',
  },
  expanded: {},
})(MuiExpansionPanel);

const ExpansionPanelSummary = withStyles({
  content: {
    'display': 'initial',
    'padding': '0px 24px 0px 24px'
  }
})(MuiExpansionPanelSummary);

const ExpansionPanelDetails = withStyles({
  root: {
    'padding': '8px 49px 24px',
  }
})(MuiExpansionPanelDetails);

export default function ResultShow(props) {
    const classes = useStyles();
    const [expanded, setExpanded] = React.useState(false);
    // const index = 0;

    const handleChange = (panel) => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);
    };

    return (
        <div className={classes.root}>
            {props.response.hits.map((item, index) => {
                return (<ExpansionPanel key={index} expanded={expanded === index} onChange={handleChange(index)}>
                    <ExpansionPanelSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1bh-content"
                        id="panel1bh-header"
                    >
                        <Typography className={classes.heading} variant='h1'>{item.metadata.title === "" ? 'No Title' : item.metadata.title}</Typography>
                        <Typography className={classes.secondaryHeading} variant='body1'>Matching Sentence: {item.sentence}</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails className={classes.expansionDetails}>
                        <div className={classes.authors}>
                            {item.metadata.authors.map((author, i) => {
                                return (
                                    <Typography variant='body2' key={i} display='initial'>
                                        {author.first} {author.last}{i === item.metadata.length - 1 ? null : ','} &nbsp;</Typography>)
                            })}
                        </div>
                        <div>
                        {CustomizedTabs(item)}
                        </div>
                    </ExpansionPanelDetails>
                </ExpansionPanel>)
            })}
        </div>
    );
}



ResultShow.propTypes = {
    response: PropTypes.object,
}