import moment from "moment";
import {DownloadClient} from "../DownloadClient/downloadClient";
import {Runner} from "../PythonRunner/runner";

export class RequestHandler {
    constructor() {
        this.downloader = new DownloadClient('downloaded_pictures/');
        this.pythonRunner = new Runner();
    }

    handleAnalyzeRequest(res, id, picUrl) {
        if (!id) res.json("Missing id param");
        else if (!picUrl) res.json("Missing pic_url param");
        else {
            // download & save pic from url
            const now = moment.now();
            const fileName = `${id}_${now}.jpg`;
            let pictureLocation;
            this.downloader.download(picUrl, fileName, function (fileLocation) {
                return function () {
                    console.log(`Download finished. saved to: ${fileLocation}`);
                    pictureLocation = fileLocation;
                };
            });

            // run dandan's script
            this.pythonRunner.run(pictureLocation, function (ans) {
                // parse scripts results

                // send to agam
                res.json(ans);
            });

        }
    };
}
