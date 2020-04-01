import axios from 'axios';

export function getSearchResults(sentence) {
    return axios({
      url: process.env.API_BASE_URL,
      method: 'post',
      data: sentence
    })
}