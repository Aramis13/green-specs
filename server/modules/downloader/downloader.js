const fs = require('fs');
const request = require('request');

export class Downloader {
    constructor(path) {
        this.savePath = path;
    }

    download(uri, filename, callback) {
        const savePath = this.savePath;
        request.head(uri, function (err, res, body) {
            console.log('content-type:', res.headers['content-type']);
            console.log('content-length:', res.headers['content-length']);

            const fileLocation = savePath + filename;

            request(uri).pipe(fs.createWriteStream(fileLocation))
                .on('close', callback(fileLocation));
        });
    }
}
