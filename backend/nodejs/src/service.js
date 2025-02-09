const fs = require('fs');
const path = require('path');

// Path to the db.json file. Adjust the path if needed.
const DB_PATH = path.join(__dirname, '../database/db.json');

/**
 * Reads the db.json file.
 * If the file does not exist or is empty/fails parsing, returns a default structure.
 */
function readDb() {
  if (!fs.existsSync(DB_PATH)) {
    return { microposts: [] };
  }
  const data = fs.readFileSync(DB_PATH, 'utf-8');
  // Check if file is empty or contains only whitespace
  if (!data.trim()) {
    return { microposts: [] };
  }
  try {
    return JSON.parse(data);
  } catch (error) {
    console.error("Error parsing db.json:", error);
    return { microposts: [] };
  }
}

/**
 * Writes the provided database object to db.json.
 */
function writeDb(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2), 'utf-8');
}

/**
 * Retrieve all microposts from the database.
 */
function getAllMicroposts() {
  const db = readDb();
  return db.microposts;
}

/**
 * Retrieve a micropost by its id.
 */
function getMicropostById(id) {
  const db = readDb();
  return db.microposts.find(mp => mp.id === id);
}

/**
 * Create a new micropost with the given title.
 * Next id is computed dynamically.
 */
function createMicropost(title) {
  const db = readDb();
  const microposts = db.microposts;
  // Compute nextId: If micropost list is empty, start at 1; otherwise, use max id + 1.
  const nextId = microposts.length > 0 ? Math.max(...microposts.map(mp => mp.id)) + 1 : 1;
  const newMicropost = { id: nextId, title };
  microposts.push(newMicropost);
  writeDb(db);
  return newMicropost;
}

/**
 * Update an existing micropost by its id.
 */
function updateMicropost(id, title) {
  const db = readDb();
  const micropost = db.microposts.find(mp => mp.id === id);
  if (!micropost) {
    return null;
  }
  micropost.title = title;
  writeDb(db);
  return micropost;
}

/**
 * Delete a micropost by its id.
 */
function deleteMicropost(id) {
  const db = readDb();
  const index = db.microposts.findIndex(mp => mp.id === id);
  if (index === -1) {
    return null;
  }
  const deletedMicropost = db.microposts.splice(index, 1)[0];
  writeDb(db);
  return deletedMicropost;
}

module.exports = {
  getAllMicroposts,
  getMicropostById,
  createMicropost,
  updateMicropost,
  deleteMicropost
};