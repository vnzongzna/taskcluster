// THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.

import Client from '../Client';

export default class Object extends Client {
  constructor(options = {}) {
    super({
      serviceName: 'object',
      serviceVersion: 'v1',
      exchangePrefix: '',
      ...options,
    });
    this.ping.entry = {"args":[],"category":"Ping Server","method":"get","name":"ping","query":[],"route":"/ping","stability":"stable","type":"function"}; // eslint-disable-line
    this.createUpload.entry = {"args":["name"],"category":"Upload","input":true,"method":"put","name":"createUpload","output":true,"query":[],"route":"/upload/<name>","scopes":"object:upload:<projectId>:<name>","stability":"experimental","type":"function"}; // eslint-disable-line
    this.finishUpload.entry = {"args":["name"],"category":"Upload","input":true,"method":"post","name":"finishUpload","query":[],"route":"/finish-upload/<name>","scopes":"object:upload:<projectId>:<name>","stability":"experimental","type":"function"}; // eslint-disable-line
    this.startDownload.entry = {"args":["name"],"category":"Download","input":true,"method":"put","name":"startDownload","output":true,"query":[],"route":"/start-download/<name>","scopes":"object:download:<name>","stability":"experimental","type":"function"}; // eslint-disable-line
    this.download.entry = {"args":["name"],"category":"Download","method":"get","name":"download","query":[],"route":"/download/<name>","scopes":"object:download:<name>","stability":"experimental","type":"function"}; // eslint-disable-line
  }
  /* eslint-disable max-len */
  // Respond without doing anything.
  // This endpoint is used to check that the service is up.
  /* eslint-enable max-len */
  ping(...args) {
    this.validate(this.ping.entry, args);

    return this.request(this.ping.entry, args);
  }
  /* eslint-disable max-len */
  // Create a new object by initiating upload of its data.
  // This endpoint implements negotiation of upload methods.  It can be called
  // multiple times if necessary, either to propose new upload methods or to
  // renew credentials for an already-agreed upload.
  // The `uploadId` must be supplied by the caller, and any attempts to upload
  // an object with the same name but a different `uploadId` will fail.
  // Thus the first call to this method establishes the `uploadId` for the
  // object, and as long as that value is kept secret, no other caller can
  // upload an object of that name, regardless of scopes.  Object expiration
  // cannot be changed after the initial call, either.  It is possible to call
  // this method with no proposed upload methods, which hsa the effect of "locking
  // in" the `expiration` and `uploadId` properties.
  // Unfinished uploads expire after 1 day.
  /* eslint-enable max-len */
  createUpload(...args) {
    this.validate(this.createUpload.entry, args);

    return this.request(this.createUpload.entry, args);
  }
  /* eslint-disable max-len */
  // This endpoint marks an upload as complete.  This indicates that all data has been
  // transmitted to the backend.  After this call, no further calls to `uploadObject` are
  // allowed, and downloads of the object may begin.  This method is idempotent, but will
  // fail if given an incorrect uploadId for an unfinished upload.
  /* eslint-enable max-len */
  finishUpload(...args) {
    this.validate(this.finishUpload.entry, args);

    return this.request(this.finishUpload.entry, args);
  }
  /* eslint-disable max-len */
  // Start the process of downloading an object's data.  Call this endpoint with a list of acceptable
  // download methods, and the server will select a method and return the corresponding payload.
  // Returns a 406 error if none of the given download methods are available.
  // See [Download Methods](https://docs.taskcluster.net/docs/reference/platform/object/download-methods) for more detail.
  /* eslint-enable max-len */
  startDownload(...args) {
    this.validate(this.startDownload.entry, args);

    return this.request(this.startDownload.entry, args);
  }
  /* eslint-disable max-len */
  // Get the data in an object directly.  This method does not return a JSON body, but
  // redirects to a location that will serve the object content directly.
  // URLs for this endpoint, perhaps with attached authentication (`?bewit=..`),
  // are typically used for downloads of objects by simple HTTP clients such as
  // web browsers, curl, or wget.
  // This method is limited by the common capabilities of HTTP, so it may not be
  // the most efficient, resilient, or featureful way to retrieve an artifact.
  // Situations where such functionality is required should ues the
  // `startDownload` API endpoint.
  // See [Simple Downloads](https://docs.taskcluster.net/docs/reference/platform/object/simple-downloads) for more detail.
  /* eslint-enable max-len */
  download(...args) {
    this.validate(this.download.entry, args);

    return this.request(this.download.entry, args);
  }
}
