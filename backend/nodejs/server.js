const express = require('express');
const app = express();
// Import micropost service which handles db.json operations.
const micropostService = require('./service.js');

// Use JSON middleware to parse application/json
app.use(express.json());

/**
 * GET /api/v1/microposts
 * Retrieve all microposts.
 */
app.get('/api/v1/microposts', (req, res) => {
  const microposts = micropostService.getAllMicroposts();
  res.json(microposts);
});

/**
 * GET /api/v1/microposts/:id
 * Retrieve a single micropost by its id.
 */
app.get('/api/v1/microposts/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const micropost = micropostService.getMicropostById(id);
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
  const newMicropost = micropostService.createMicropost(title);
  res.status(201).json(newMicropost);
});

/**
 * PUT /api/v1/microposts/:id
 * Update an existing micropost.
 * Request body should include 'title'.
 */
app.put('/api/v1/microposts/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const updatedMicropost = micropostService.updateMicropost(id, title);
  if (!updatedMicropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(updatedMicropost);
});

/**
 * DELETE /api/v1/microposts/:id
 * Delete a micropost.
 */
app.delete('/api/v1/microposts/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const deletedMicropost = micropostService.deleteMicropost(id);
  if (!deletedMicropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(deletedMicropost);
});

// Start the server on port 3000
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Micropost API server is running on port ${PORT}`);
});