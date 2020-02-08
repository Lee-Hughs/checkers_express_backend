const express = require('express');
const util = require('util');
const app = express();
const port = process.env.PORT || 5000;


//consol.log that your sever is up and running
app.listen(port, () => console.log(`Listening on port ${port}`));

// create a GET route
app.get('/express_backend', (req, res) => {
	res.send({ express: 'YOUR EXPRESS BACKEND IS CONNECTED TO REACT' });
});

app.get('/checkers_bot', (req, res) => {
	console.log("req: ");
	console.log(req.query);
	board = req.query.board;
	console.log(board);
	player = req.query.player;
	console.log(player);
	const spawn = require('child_process').spawn;
	const pythonProcess = spawn('python', ["test.py",board, player]);
	pythonProcess.stdout.on('data', function(data) {
		console.log(data.toString());
		res.send( { express: data.toString() });
    		});
	});
