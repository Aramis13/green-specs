import express from 'express';
import {RequestHandler} from "../modules/RequestHandler/handler";

const router = new express.Router();

const requestHandler = new RequestHandler();

router.get('/healthcheck', function (req, res) {
    res.json("OK");
});

router.get('/analyze', function (req, res) {
    const id = req.query.id;
    const picUrl = req.query.pic_url;
    requestHandler.handleAnalyzeRequest(res, id, picUrl)
});

router.post('/analyze', function (req, res) {
    const id = req.body.id;
    const picUrl = req.body.pic_url;
    requestHandler.handleAnalyzeRequest(res, id, picUrl)
});

export default router;
