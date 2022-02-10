var fs = require('fs');

var file = process.argv[2]

const dat = fs.readFileSync(file,'utf8')
console.log(dat)
