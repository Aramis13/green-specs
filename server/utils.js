import morgan from 'morgan';
import tracer from 'tracer';

const http = require('http');
const https = require('https');

export const log = (() => {
    const logger = tracer.colorConsole();
    logger.requestLogger = morgan('dev');
    return logger;
})();

export const normalizePort = (val) => {
    const port = parseInt(val, 10);
    if (Number.isNaN(port)) return val;
    if (port >= 0) return port;
    return false;
};

export const startServer = (app, port, options = {}) => {
    const server = port === 8080 ? http.createServer(app) : https.createServer(options, app);
    server.on('error', (error) => {
        if (error.syscall !== 'listen') throw error;
        log.error(`Failed to start server: ${error}`);
        process.exit(1);
    });

    server.on('listening', () => {
        const address = server.address();
        log.info(`Server listening ${address.address}:${address.port}`);
    });

    server.listen(port);
};
