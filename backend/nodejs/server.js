const express = require('express');
const app = express();

// Use JSON middleware to parse application/json
app.use(express.json());

// In-memory storage for Microposts
let microposts = [];
let nextId = 1;

/**
 * Data Access Functions
 * Single-responsibility functions for managing microposts in the in-memory storage.
 */

// Get all microposts
function getAllMicroposts() {
  return microposts;
}

// Get a micropost by its id
function getMicropostById(id) {
  return microposts.find(mp => mp.id === id);
}

// Create a new micropost with the given title
function createMicropost(title) {
  const newMicropost = { id: nextId++, title };
  microposts.push(newMicropost);
  return newMicropost;
}

// Update an existing micropost's title by its id
function updateMicropost(id, title) {
  const micropost = getMicropostById(id);
  if (micropost) {
    micropost.title = title;
  }
  return micropost;
}

// Delete a micropost by its id
function deleteMicropost(id) {
  const index = microposts.findIndex(mp => mp.id === id);
  if (index === -1) {
    return null;
  }
  return microposts.splice(index, 1)[0];
}

/**
 * Route Handler Functions
 * Request handling functions which utilize the data access functions.
 */

// Handle GET /api/v1/microposts
function handleGetAllMicroposts(req, res) {
  res.json(getAllMicroposts());
}

// Handle GET /api/v1/microposts/:id
function handleGetMicropostById(req, res) {
  const id = parseInt(req.params.id, 10);
  const micropost = getMicropostById(id);
  if (!micropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(micropost);
}

// Handle POST /api/v1/microposts
function handleCreateMicropost(req, res) {
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const newMicropost = createMicropost(title);
  res.status(201).json(newMicropost);
}

// Handle PUT /api/v1/microposts/:id
function handleUpdateMicropost(req, res) {
  const id = parseInt(req.params.id, 10);
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const updatedMicropost = updateMicropost(id, title);
  if (!updatedMicropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(updatedMicropost);
}

// Handle DELETE /api/v1/microposts/:id
function handleDeleteMicropost(req, res) {
  const id = parseInt(req.params.id, 10);
  const deletedMicropost = deleteMicropost(id);
  if (!deletedMicropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(deletedMicropost);
}

/**
 * Routing
 */
app.get('/api/v1/microposts', handleGetAllMicroposts);
app.get('/api/v1/microposts/:id', handleGetMicropostById);
app.post('/api/v1/microposts', handleCreateMicropost);
app.put('/api/v1/microposts/:id', handleUpdateMicropost);
app.delete('/api/v1/microposts/:id', handleDeleteMicropost);

/**
 * Start the server on port 3000
 */
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Micropost API server is running on port ${PORT}`);
});