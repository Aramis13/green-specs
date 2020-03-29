import express from 'express';

const router = new express.Router();

router.get('/healthcheck', function (req, res) {
    res.json("OK");
});

export default router;
