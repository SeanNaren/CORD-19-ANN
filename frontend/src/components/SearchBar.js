import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import ResultShow from './ResultShow'
import SearchLinearProgress from './Progress'
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
    const [sentence, setSentence] = React.useState(null);
    const [loading, setLoading] = React.useState(false);

    const handleClick = ev => {
      setLoading(true);
      getSearchResults(ev.target.value).then(res=>{
        setResponse(res.data);
        setLoading(false);
      });
    }

    const handleSearch = ev => {
        if (ev.key === 'Enter') {
          setLoading(true);
          getSearchResults(sentence).then(res=>{
            setResponse(res.data);
            setLoading(false);
          });
          ev.preventDefault();
        }
    }

    return (
        <div className={classes.root}>
            <Paper component="form" type="submit" className={classes.searchBar} onKeyPress={handleSearch}>
                <InputBase
                    className={classes.input}
                    placeholder="Enter sentence to search"
                    onInput={e=>setSentence(e.target.value)}
                />
                <IconButton className={classes.iconButton} aria-label="search" onClick={handleClick}>
                    <SearchIcon />
                </IconButton>
            </Paper>
            {loading == true && <SearchLinearProgress/>}
            {response !== null && <ResultShow className={classes.resultShow} response={response} />}
        </div>
    );
}
