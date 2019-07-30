let express = require('express');
let _ = require('lodash');
let debug = require('debug')('base:app');
let assert = require('assert');
let morganDebug = require('morgan-debug');
let http = require('http');
let sslify = require('express-sslify');
let hsts = require('hsts');
let csp = require('content-security-policy');
let uuidv4 = require('uuid/v4');

/** Create server from app */
let createServer = function() {
  let that = this;

  // 404 Error handler
  that.use(function(req, res, next) {
    res.setHeader('Content-Type', 'application/json');
    res.status(404).json({error: 'Not found'});
  });

  return new Promise(function(accept, reject) {
    // Launch HTTP server
    let server = http.createServer(that);

    // Add a little method to help kill the server
    server.terminate = function() {
      return new Promise(function(accept, reject) {
        server.close(function() {
          accept();
        });
      });
    };

    // Handle errors
    server.once('error', reject);

    // Listen
    server.listen(that.get('port'), function() {
      debug('Server listening on port ' + that.get('port'));
      accept(server);
    });
  });
};

/** Create express application.  See the README for docs.
 */
let app = async function(options) {
  assert(options, 'options are required');
  _.defaults(options, {
    contentSecurityPolicy: true,
    robotsTxt: true,
  });
  assert(typeof options.port === 'number', 'Port must be a number');
  assert(options.env === 'development' ||
         options.env === 'production', 'env must be production or development');
  assert(options.forceSSL !== undefined, 'forceSSL must be defined');
  assert(options.trustProxy !== undefined, 'trustProxy must be defined');
  assert(options.apis, 'Must provide an array of apis');
  assert(!options.rootDocsLink, '`rootDocsLink` is no longer allowed');
  assert(!options.docs, '`docs` is no longer allowed');

  // Create application
  let app = express();
  app.set('port', options.port);
  app.set('env', options.env);
  app.set('json spaces', 2);

  // ForceSSL if required suggested
  if (options.forceSSL) {
    app.use(sslify.HTTPS({
      trustProtoHeader: options.trustProxy,
    }));
  }

  // When we force SSL, we also want to set the HSTS header file correctly.  We
  // also want to allow testing code to check for the HSTS header being
  // generated correctly without having to generate an SSL cert and key and
  // have express listen on ssl
  if (options.forceSSL || options.forceHSTS) {
    app.use(hsts({
      maxAge: 1000 * 60 * 60 * 24 * 90,
      force: true,
    }));
  }

  if (options.contentSecurityPolicy) {
    // if you're loading HTML from an API, you're doing it wrong..
    app.use(csp.getCSP({
      'default-src': csp.SRC_NONE,
      'frame-ancestors': csp.SRC_NONE,
      'base-uri': csp.SRC_NONE,
      'report-uri': '/__cspreport__',
    }));
  }

  if (options.trustProxy) {
    app.set('trust proxy', true);
  }

  // keep cheap security vuln scanners happy..
  app.disable('x-powered-by');
  app.use((req, res, next) => {
    res.setHeader('x-content-type-options', 'nosniff');
    next();
  });

  // attach request-id to request object and response
  app.use((req, res, next) => {
    let reqId = req.headers['x-request-id'] || uuidv4();
    req.requestId = reqId;
    res.setHeader('x-for-request-id', reqId);
    next();
  });

  // output user-agent and referrer in production, which can be useful when debugging API (ab)use
  const format = app.get('env') === 'development' ?
    'dev' : '[:date[clf]] :method :url -> :status; ip=:remote-addr referrer=":referrer" ua=":user-agent"';
  app.use(morganDebug('app:request', format));

  if (options.robotsTxt) {
    app.use('/robots.txt', function(req, res) {
      res.header('Content-Type', 'text/plain');
      res.send('User-Agent: *\nDisallow: /\n');
    });
  }

  options.apis.forEach(api => {
    api.express(app);
  });

  // Add some auxiliary methods to the app
  app.createServer = createServer;

  return app.createServer();
};

// Export app creation utility
module.exports = app;
