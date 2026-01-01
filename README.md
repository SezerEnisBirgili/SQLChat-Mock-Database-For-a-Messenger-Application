# SQLChat

**SQLChat** is a hypothetical messenger application designed to demonstrate **database modeling**, **data management**, and **CRUD-based application logic**.  
The project focuses on both **relational database design (MySQL)** and a **collection-based moderation module** for handling user complaints and reports.

---

## Project Overview

SQLChat is a basic messaging platform that allows users to communicate through conversations, exchange text messages, and share file attachments.  
In addition to core messaging functionality, the system includes a **Complaints and Reports module** that allows users to submit feedback and report disruptive behavior.

The project is divided into two main parts:

- **Backend – Relational Database Design (MySQL)**
- **Backend – Complaints & Reports Management (Collection-Based CRUD System)**

---

## Backend – Relational Database Design (MySQL)

This part of the project defines the **core data model** of the SQLChat messenger using a relational database approach.

### Key Features

- User registration and contact management  
- One-to-one and group conversations  
- Message exchange through conversations  
- File attachments stored via cloud URLs  
- Referential integrity using foreign keys  
- Cascading updates and deletes  

---

### Database Tables

#### Users
Stores registered user accounts.

- `user_id` (PK)  
- `name`  
- `email` (unique)  
- `password`  

---

#### Contacts
Represents relationships between users.

- `contact_id` (PK)  
- `user_id_1` (FK → Users)  
- `user_id_2` (FK → Users)  

---

#### Conversations
Stores conversation metadata.

- `conversation_id` (PK)  
- `creator_id`  
- `title`  

---

#### Participates
Maps users to conversations.

- `participant_id` (PK)  
- `user_id` (FK → Users)  
- `conv_id` (FK → Conversations)  

---

#### Messages
Stores message content.

- `message_id` (PK)  
- `text`  
- `file_url` (optional)  

---

#### Sender
Assigns ownership of a message.

- `sender_id` (PK)  
- `message_id` (FK → Messages)  
- `user_id` (FK → Users)  

---

#### Receiver
Defines the destination user of a message.

- `receiver_id` (PK)  
- `message_id` (FK → Messages)  
- `user_id` (FK → Users)  

---

#### Exchanges
Links messages to conversations and timestamps.

- `exchange_id` (PK)  
- `conv_id` (FK → Conversations)  
- `message_id` (FK → Messages)  
- `date`  

---

#### Files
Stores metadata for uploaded files.

- `file_id` (PK)  
- `filename`  
- `file_url`  

---

#### Attachments
Links messages to their files.

- `attachment_id` (PK)  
- `message_id` (FK → Messages)  
- `file_id` (FK → Files)  

---

## Backend – Complaints & Reports Module

This module represents a **moderation and feedback system** implemented using a **collection-based (NoSQL-style) design**.

---

### Collections

#### Complaints Collection
Stores user complaints and feature suggestions.

- `user_id`  
- `complaint_type`  
- `complaint_text`  
- `complaint_time`  

---

#### Reports Collection
Stores reports about disruptive users.

- `user_id`  
- `complaint_type`  
- `complaint_text`  
- `complaint_time`  

Each record is tied to the user who created it, and users may only modify or delete their own entries.

---

## Application Logic (CRUD Main Loop)

The system includes a **console-based interface** that allows users to interact with collections using CRUD operations.

### Available Operations

1. **Create a Collection**  
   Users can create a new empty collection with a unique name.

2. **Read All Data**  
   Displays all records in a collection.

3. **Read with Filtering**  
   Displays records belonging only to the current user based on a specified attribute.

4. **Insert Data**  
   Adds a new record tied to the current user ID.

5. **Delete Data**  
   Allows users to delete only their own records.

6. **Update Data**  
   Allows users to update attributes of their own records.

Access control is enforced using `user_id`.

---

## Constraints & Rules

- Users do not need to participate in conversations to exist in the system  
- Messages **must** belong to a conversation  
- Conversations **must** have at least one participant  
- Files cannot exist without being attached to a message  
- A file can only belong to **one** message  
- Users can only modify or delete data they own  

---

## Technologies & Concepts

- MySQL  
- Relational Database Design  
- NoSQL Collection Modeling  
- CRUD Operations  
- Entity-Relationship (ER) Modeling  
- Data Integrity & Constraints  
- Access Control via User Ownership 
