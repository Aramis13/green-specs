const axios = require('axios');

export class APIWrapper {
    constructor() {
        const apiHost = '127.0.0.1';
        const apiPort = 5000;
        const queryString = {
            image_url: '{{IMG_URL}}'
        };

        this.url = `http://${apiHost}:${apiPort}/?${Object.keys(queryString).map(key => `${key}=${queryString[key]}`).join("&")}`;
    }

    call(imgUrl) {
        const modifiedUrl = this.getOptionsPostPlaceholdersReplacement(imgUrl);
        // console.log(modifiedUrl);
        return axios.get(modifiedUrl)
    }

    getOptionsPostPlaceholdersReplacement(imgUrl) {
        return this.url.replace('{{IMG_URL}}', imgUrl);
    }
}
