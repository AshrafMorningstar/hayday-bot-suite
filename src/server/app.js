const express = require('express');
const cors = require('cors');
const path = require('path');
const routes = require('./routes');

function createServer() {
  const app = express();

  app.use(cors());
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true }));

  // Static frontend
  const publicDir = path.join(__dirname, '../../public');
  app.use(express.static(publicDir));

  // REST API
  app.use('/api', routes);

  // Fallback to index.html for SPA
  app.get('*', (req, res) => {
    res.sendFile(path.join(publicDir, 'index.html'));
  });

  return app;
}

function startServer(port = 3000) {
  const app = createServer();
  return new Promise((resolve, reject) => {
    const server = app.listen(port, () => {
      resolve({ server, port });
    });
    server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        // Try next port
        startServer(port + 1).then(resolve).catch(reject);
      } else {
        reject(err);
      }
    });
  });
}

module.exports = { createServer, startServer };
