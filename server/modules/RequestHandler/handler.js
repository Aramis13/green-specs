import {APIWrapper} from "../APIWrapper/wrapper";

export class RequestHandler {
    constructor() {
        this.apiWrapper = new APIWrapper();
    }

    handleAnalyzeRequest(res, id, picUrl) {
        if (!id) res.json("Missing id param");
        else if (!picUrl) res.json("Missing pic_url param");
        else {
            this.apiWrapper.call(picUrl).then(response => {
                // let re = new RegExp(/<svg.*<\/svg>/, 'gms') ;
                // const rawSvg = response.data.match(re)[0];
                // const svg = parse(rawSvg);
                // console.log(response.data);
                // const paths = rest.forEach(path  => parseSvgPath(path));

                res.send(response.data);
            }).catch(error => {
                console.log(error);
            });
        }
    };
}
