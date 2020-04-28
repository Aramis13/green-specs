import * as firebase from 'firebase';
import config from 'config';

firebase.initializeApp(config.firebaseConfig);

const database = firebase.database();

export {database as default}
