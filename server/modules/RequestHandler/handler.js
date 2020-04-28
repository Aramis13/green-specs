import {APIWrapper} from "../APIWrapper/wrapper";
import database from '../../firebase/firebase'

export class RequestHandler {
    constructor() {
        this.apiWrapper = new APIWrapper();
        this.ref = database.ref("/");
    }

    handleAnalyzeRequest(res, id, picUrl) {
        if (!id) res.json("Missing id param");
        else if (!picUrl) res.json("Missing pic_url param");
        else {
            this.apiWrapper.call(picUrl).then(response => {
                const svg = response.data;
                this.ref.once('value').then((snapshot) => {
                    const plants = [];
                    snapshot.forEach((childSnapshot) => {
                        plants.push({
                            id: childSnapshot.key,
                            ...childSnapshot.val()
                        });
                    });

                    const ans = {
                        svg,
                        plants
                    };

                    res.send(ans);
                });
            }).catch(error => {
                console.log(error);
            });
        }
    };
}
