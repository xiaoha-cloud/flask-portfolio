#!/bin/bash

BASE_URL="http://localhost:5000/api/timeline"

NAME="TestUser_$RANDOM"
EMAIL="test_$RANDOM@example.com"
CONTENT="Test post content $RANDOM"

echo "[INFO] Creating a timeline post..."
# Create a new post
POST_RESPONSE=$(curl -s -X POST "$BASE_URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")


POST_ID=$(echo "$POST_RESPONSE" | grep -oP '"id":\s*\K\d+')

if [[ -z "$POST_ID" ]]; then
  echo "[ERROR] Failed to create post."
  exit 1
fi

echo "[SUCCESS] Post created with ID: $POST_ID"

# Fetch the post to confirm creation
echo "[INFO] Fetching timeline posts..."
GET_RESPONSE=$(curl -s "$BASE_URL")

# Check if the created post is in the response
if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "[SUCCESS] Post found in GET /api/timeline."
else
  echo "[ERROR] Post NOT found in GET /api/timeline."
  exit 1
fi

# Delete the post
echo "[INFO] Deleting post with ID: $POST_ID"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$POST_ID")

# Confirm deletion
echo "[INFO] Confirming deletion..."
CONFIRM_RESPONSE=$(curl -s "$BASE_URL")

if echo "$CONFIRM_RESPONSE" | grep -q "$CONTENT"; then
  echo "[ERROR] Post was NOT deleted."
  exit 1
else
  echo "[SUCCESS] Post successfully deleted."
fi
