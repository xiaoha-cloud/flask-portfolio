#!/bin/bash

# Test GET endpoint, should return an empty list initially
echo "Testing GET /api/timeline_post (should be empty):"
curl -s http://localhost:5000/api/timeline_post | jq

# Create a random timeline post using POST endpoint
RANDOM_ID=$RANDOM
NAME="TestUser$RANDOM_ID"
EMAIL="test$RANDOM_ID@example.com"
CONTENT="This is a test post with random id $RANDOM_ID"

echo "Creating a new timeline post with POST /api/timeline_post:"
RESPONSE=$(curl -s -X POST -d "name=$NAME" -d "email=$EMAIL" -d "content=$CONTENT" http://localhost:5000/api/timeline_post)
echo $RESPONSE | jq

# Extract the id of the created post
POST_ID=$(echo $RESPONSE | jq '.id')

# Test GET endpoint again, should include the new post
echo "Testing GET /api/timeline_post (should include the new post):"
curl -s http://localhost:5000/api/timeline_post | jq

# Bonus: Delete the test post
echo "Deleting the test post with DELETE /api/timeline_post/$POST_ID:"
curl -s -X DELETE http://localhost:5000/api/timeline_post/$POST_ID | jq

# Final GET to confirm deletion
echo "Final GET /api/timeline_post (should not include the deleted post):"
curl -s http://localhost:5000/api/timeline_post | jq
