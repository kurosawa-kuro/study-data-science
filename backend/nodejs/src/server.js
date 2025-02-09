const express = require('express');
const app = express();
// Import micropost controller which handles request processing.
const micropostController = require('./controller');

// Use JSON middleware to parse application/json
app.use(express.json());

/**
 * GET /api/v1/microposts
 * Retrieve all microposts.
 */
app.get('/api/v1/microposts', micropostController.getAllMicroposts);

/**
 * GET /api/v1/microposts/:id
 * Retrieve a single micropost by its id.
 */
app.get('/api/v1/microposts/:id', micropostController.getMicropostById);

/**
 * POST /api/v1/microposts
 * Create a new micropost.
 * Request body must include 'title'.
 */
app.post('/api/v1/microposts', micropostController.createMicropost);

/**
 * PUT /api/v1/microposts/:id
 * Update an existing micropost.
 * Request body should include 'title'.
 */
app.put('/api/v1/microposts/:id', micropostController.updateMicropost);

/**
 * DELETE /api/v1/microposts/:id
 * Delete a micropost.
 */
app.delete('/api/v1/microposts/:id', micropostController.deleteMicropost);

// Start the server on port 3000
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Micropost API server is running on port ${PORT}`);
});