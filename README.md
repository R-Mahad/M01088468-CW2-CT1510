# Week 7: Secure Authentication System

**Student Name:** [Rayaan Mahad]  
**Student ID:** [M001088468]  
**Course:** CST1510 - CW2 
## Project Description

This project is a command-line authentication system that implements secure password hashing using `bcrypt`.  
Users can register new accounts and log in with their credentials. Passwords are **never** stored in plaintext; instead, they are hashed with automatic salting before being written to a local file (`users.txt`).   

## Features

- Secure password hashing using `bcrypt` with automatic salt generation  
- User registration with duplicate-username prevention  
- User login with password verification using bcrypt  
- Input validation for usernames and passwords  
- File-based user data persistence in `users.txt`

## Technical Implementation

- **Hashing Algorithm:** `bcrypt` (adaptive, salted, one-way hashing)  
- **Data Storage:** Plain text file (`users.txt`) with comma-separated values:
  - `username,hashed_password`
- **Password Security:**  
  - No plaintext storage  
  - Automatic salting  
  - Verification via `bcrypt.checkpw()` rather than decryption :contentReference[oaicite:4]{index=4}
- **Validation Rules:**
  - Username: 3–20 characters, alphanumeric only  
  - Password: 6–50 characters

## How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
