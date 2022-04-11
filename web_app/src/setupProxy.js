//Creates a proxy to our backend server

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use('/auth/**', 
        createProxyMiddleware({ 
            target: 'http://localhost:5000'
        })
    );
};
