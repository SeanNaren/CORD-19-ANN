import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import ResultShow from './ResultShow'
import { getSearchResults } from './services/getSearchResults.js'

const useStyles = makeStyles((theme) => ({
    root: {
        padding: '2px 4px',
        width: '100%',
    },
    input: {
        marginLeft: theme.spacing(1),
        flex: 1,
    },
    iconButton: {
        padding: 10,
    },
    divider: {
        height: 28,
        margin: 4,
    },
    searchBar: {
        width: '100%',
        display: 'flex',
        alignItems: 'center',
    }
}));

export default function SearchBar() {
    const classes = useStyles();
    const [response, setResponse] = React.useState(null);

    const handleClick = event => {
        getSearchResults(event.target.value).then(res=>{
            setResponse(res.data);
        });
    }

    return (
        <div className={classes.root}>
            <Paper component="form" className={classes.searchBar}>
                <InputBase
                    className={classes.input}
                    placeholder="Enter sentence to search"
                    onChange={handleClick}
                />
                <IconButton className={classes.iconButton} aria-label="search">
                    <SearchIcon />
                </IconButton>
            </Paper>
            {response !== null && <ResultShow className={classes.resultShow} response={response} />}
        </div>
    );
}
