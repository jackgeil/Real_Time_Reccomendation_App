var SingleStoreClient = require('@singlestore/http-client');
var instance = SingleStoreClient.ApiClient.instance;

var BasicAuth = instance.authentications['BasicAuth'];
BasicAuth.username = process.env.SINGLESTORE_WORKSPACE_USERNAME;
BasicAuth.password = process.env.SINGLESTORE_WORKSPACE_PASSWORD;

instance.basePath = 'https://' + process.env.SINGLESTORE_WORKSPACE_HOST;

var api = new SingleStoreClient.HttpApi();

export default function handler(req, res) {
    api.rows({
        queryInput: {
            database: 'r2_d2_db',  // Replace with your actual database name
            sql: 'SELECT * FROM purchases LIMIT 200;'  // Replace with your actual SQL query
        }
    }).then(dbResponse => {
        res.status(200).json(dbResponse.results[0].rows);
    }).catch(err => {
        res.status(500).json({ error: err.message });
    });
}
