const express = require('express');
const app = express();

// Use JSON middleware to parse application/json
app.use(express.json());

// In-memory storage for Microposts
let microposts = [];
let nextId = 1;

/**
 * GET /api/v1/microposts
 * Retrieve all microposts.
 */
app.get('/api/v1/microposts', (req, res) => {
  res.json(microposts);
});

/**
 * GET /api/v1/microposts/:id
 * Retrieve a single micropost by its id.
 */
app.get('/api/v1/microposts/:id', (req, res) => {
  const micropostId = parseInt(req.params.id, 10);
  const micropost = microposts.find(mp => mp.id === micropostId);
  if (!micropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(micropost);
});

/**
 * POST /api/v1/microposts
 * Create a new micropost.
 * Request body must include 'title'.
 */
app.post('/api/v1/microposts', (req, res) => {
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const newMicropost = { id: nextId++, title };
  microposts.push(newMicropost);
  res.status(201).json(newMicropost);
});

/**
 * PUT /api/v1/microposts/:id
 * Update an existing micropost.
 * Request body should include 'title'.
 */
app.put('/api/v1/microposts/:id', (req, res) => {
  const micropostId = parseInt(req.params.id, 10);
  const { title } = req.body;
  const micropost = microposts.find(mp => mp.id === micropostId);
  if (!micropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  micropost.title = title;
  res.json(micropost);
});

/**
 * DELETE /api/v1/microposts/:id
 * Delete a micropost.
 */
app.delete('/api/v1/microposts/:id', (req, res) => {
  const micropostId = parseInt(req.params.id, 10);
  const index = microposts.findIndex(mp => mp.id === micropostId);
  if (index === -1) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  const deletedMicropost = microposts.splice(index, 1)[0];
  res.json(deletedMicropost);
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Micropost API server is running on port 3000');
});