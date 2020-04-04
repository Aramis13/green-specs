const {spawn} = require('child_process');

export class Runner {
    run(pathToScript, callback) {
        let returnedValue;
        const python = spawn('python', ['mocks/mock_script.py', 'arg1', 'arg2']);

        // collect data from script
        python.stdout.on('data', function (data) {
            console.log('Pipe data from python script ...');
            returnedValue = data.toString();
        });

        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => {
            console.log(`child process close all stdio with code ${code}`);
            // send data to browser
            return callback(returnedValue);
        });
    }
}
