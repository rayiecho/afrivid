import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# We need a service account for afrivid-studio
# For now let's use the REST API with the new project
# First let's create the rules via Firebase Console manually

print("""
Go to Firebase Console → afrivid-studio → Firestore → Rules
Replace with these rules:

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function isLoggedIn() {
      return request.auth != null;
    }
    function isOwner(userId) {
      return request.auth.uid == userId;
    }
    function isAdmin() {
      return request.auth != null && request.auth.token.email in 
        ['youngafricansn@gmail.com', 'r.ayiecho@alustudent.com'];
    }

    match /studio_users/{userId} {
      allow read, write: if isLoggedIn() && isOwner(userId);
      allow read: if isAdmin();
    }
    match /studio_videos/{docId} {
      allow create: if isLoggedIn();
      allow read: if isLoggedIn();
    }
    match /studio_feedback/{docId} {
      allow create: if isLoggedIn();
      allow read: if isAdmin();
    }
  }
}

Click Publish when done.
""")
