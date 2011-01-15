// A simple CLI driver to Arc 90's Readability. Please note that it
// requires readability to either honour readability.debugging, or to
// be patched not to barf profiling data into stdout.

// It is expecting to be run as node readability.js URL, and to
// recieve the actual HTML on standard input.

var readability = require('readability');
var stdin = process.openStdin();
url = process.argv[2]

html = '';

stdin.on('data', function (chunk) {

  html += chunk;
});

readability.debugging = false;

stdin.on('end', function () {

  readability.parse(html, url , function(result) {
    process.stdout.write(result.content)
  });
});
