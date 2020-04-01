import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        padding: '10px 5px'
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        flexBasis: '33.33%',
        flexShrink: 0,
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
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
                        <Typography className={classes.heading} variant='h4'>{item.title === "" ? 'No Title' : item.title}</Typography>
                        <Typography className={classes.secondaryHeading}>{item.sentence}</Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails className={classes.expansionDetails}>
                        <div className={classes.authors}>
                            {item.authors.map((author, i) => {
                                return (
                                    <Typography variant='body2' key={i} display='initial'>
                                        {author.first} {author.last}{i === item.authors.length - 1 ? null : ','} &nbsp;</Typography>)
                            })}
                        </div>
                        <div>
                            <Typography variant='body1' >
                                {item.paragraph.text}
                            </Typography>
                            <Typography variant='overline' style={{fontSize:13, fontWeight:"bold"}} >
                                Cosine Distance: {Number((item.distance).toFixed(4))}
                            </Typography>
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