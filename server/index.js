import 'babel-polyfill';
import config from 'config';
import express from 'express';

import bootstrap from './bootstrap';
import {log, normalizePort, startServer} from './utils';


const fs = require('fs');
const options = {
    key: fs.existsSync('server.key') ? fs.readFileSync('server.key') : fs.readFileSync('key.pem'),
    cert:fs.existsSync('server.crt') ? fs.readFileSync('server.crt') : fs.readFileSync('cert.pem')
};

const app = express();

app.start = async () => {

    log.info('Starting Server...');

    const port = normalizePort(config.get('port'));
    const securePort = normalizePort(config.get('securePort'));

    app.set('port', port);

    bootstrap(app);

    startServer(app, securePort, options);
    startServer(app, port);
};

app.start().catch((err) => {
    log.error(err);
});

export default app;
