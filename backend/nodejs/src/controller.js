const micropostService = require('./service');

/**
 * GET /api/v1/microposts
 * Retrieve all microposts.
 */
function getAllMicroposts(req, res) {
  const microposts = micropostService.getAllMicroposts();
  res.json(microposts);
}

/**
 * GET /api/v1/microposts/:id
 * Retrieve a single micropost by its id.
 */
function getMicropostById(req, res) {
  const id = parseInt(req.params.id, 10);
  const micropost = micropostService.getMicropostById(id);
  if (!micropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(micropost);
}

/**
 * POST /api/v1/microposts
 * Create a new micropost.
 * Request body must include 'title'.
 */
function createMicropost(req, res) {
  const { title } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Title is required' });
  }
  const newMicropost = micropostService.createMicropost(title);
  res.status(201).json(newMicropost);
}

/**
 * PUT /api/v1/microposts/:id
 * Update an existing micropost.
 * Request body should include 'title'.
 */
function updateMicropost(req, res) {
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
}

/**
 * DELETE /api/v1/microposts/:id
 * Delete a micropost.
 */
function deleteMicropost(req, res) {
  const id = parseInt(req.params.id, 10);
  const deletedMicropost = micropostService.deleteMicropost(id);
  if (!deletedMicropost) {
    return res.status(404).json({ error: 'Micropost not found' });
  }
  res.json(deletedMicropost);
}

module.exports = {
  getAllMicroposts,
  getMicropostById,
  createMicropost,
  updateMicropost,
  deleteMicropost
};