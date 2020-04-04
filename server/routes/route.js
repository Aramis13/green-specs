import express from 'express';
import {Downloader} from "../modules/downloader/downloader";
import moment from 'moment';
import {PythonRunner} from "../modules/pythonRunner/pythonRunner";

const router = new express.Router();

const downloader = new Downloader('downloaded_pictures/');
const pythonRunner = new PythonRunner();

router.get('/healthcheck', function (req, res) {
    res.json("OK");
});

router.get('/analyze', function (req, res) {
    const id = req.query.id;
    const picUrl = req.query.pic_url;
    handleAnalyzeRequest(res, id, picUrl)
});

router.post('/analyze', function (req, res) {
    const id = req.body.id;
    const picUrl = req.body.pic_url;
    handleAnalyzeRequest(res, id, picUrl)
});

function handleAnalyzeRequest(res, id, picUrl) {
    if (!id) res.json("Missing id param");
    else if (!picUrl) res.json("Missing pic_url param");
    else {
        // download & save pic from url
        const now = moment.now();
        const fileName = `${id}_${now}.jpg`;
        let pictureLocation;
        downloader.download(picUrl, fileName, function (fileLocation) {
            return function () {
                console.log(`Download finished. saved to: ${fileLocation}`);
                pictureLocation = fileLocation;
            };
        });

        // run dandan's script
        pythonRunner.run(pictureLocation, function (ans) {
            // parse scripts results

            // send to agam
            res.json(ans);
        });

    }
};

export default router;
