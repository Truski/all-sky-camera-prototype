const bodyParser = require('body-parser');
const express = require('express');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());

const port = 80;

app.get('/', (req, res) => res.send('Hello World!'));
app.put('/upload', function(req, res) {
	var buf = Buffer.from(req.body.image, 'base64');
	console.log("Time: " + req.body.time);
	console.log("Lat: " + req.body.lat);
	console.log("Long: " + req.body.long);
	var filename = "./meteor.jpg";
	fs.writeFile(filename, buf, (err) => {
		if (err) throw err;
		console.log(`The file has been saved as ${filename} `);
	});
	res.send('Hello Putter!');
});

app.listen(port, () => console.log(`All-Sky-Camera upload server listening on port ${port}!`));