#!/bin/bash

NAME="Test_$RANDOM"
EMAIL="test_${RANDOM}@example.com"
CONTENT="This is a test, for $(date)"

echo 'POST test...'

RESPONSE=$(curl -s -X POST http://localhost:5001/api/timeline_post \
    -d "name=$NAME" -d "email=$EMAIL" -d "content=$CONTENT")

POST_ID=$(echo "$RESPONSE" | jq -r '.id')

echo "-------------"
echo "Response: $RESPONSE"

echo ""
echo "GET test to verify POST worked..."

GET_RESPONSE=$(curl -s -X GET http://localhost:5001/api/timeline_posts)

echo "-------------"
echo ""
echo "All posts: $GET_RESPONSE"

if echo "$GET_RESPONSE" | grep -q "$NAME"; then
    echo "POST request successful - Posted data found in timeline"
else
    echo "POST request may have failed - Posted data not found in timeline"
fi

echo ""
echo "-------------"
echo ""

DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:5001/api/timeline_post/$POST_ID)

echo "Deleting post with ID $POST_ID..."
echo "Delete response: $DELETE_RESPONSE"

echo ""
echo "-------------"
echo ""

GET_RESPONSE=$(curl -s -X GET http://localhost:5001/api/timeline_posts)

echo "Getting all posts after deletion..."
echo "All posts: $GET_RESPONSE"

if echo "$GET_RESPONSE" | grep -q "$NAME"; then
    echo "POST request successful - Posted data found in timeline"
else
    echo "POST request may have failed - Posted data not found in timeline"
fi