// Called when the user clicks on the browser action.
var HEADERS_TO_STRIP_LOWERCASE = [
  'content-security-policy',
  'x-frame-options',
];

chrome.webRequest.onHeadersReceived.addListener(
  function(details) {
    return {
      responseHeaders: details.responseHeaders.filter(function(header) {
        return HEADERS_TO_STRIP_LOWERCASE.indexOf(header.name.toLowerCase()) < 0;
      })
    };
  }, {
    urls: ["http://localhost:8210/*","https://accounts.infusionsoft.com/*","http://127.0.0.1:8210/*","https://signin.infusionsoft.com/*"]
  }, ["blocking", "responseHeaders"]);
