import json

from bson import ObjectId

from connect import connectDB
from dummy_data import dummy_data, dummy_data2
from pymongo import errors


def createCollection(db, collection_name):
    try:
        # If the collection doesn't exist, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        elif collection_name in db.list_collection_names():
            print("Collection already exists")
    except Exception as e:
        print("An error occured: ", e)


def insert_into_collection(db, collection_name, data, user_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        data["user_id"] = user_id

        # Insert the data into the collection
        result = collection.insert_one(data)

        # Print the inserted document ID
        print("Insertion successfully completed")
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_all_data(db, collection_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Use the find method to retrieve all documents
        result = collection.find()

        # Iterate through the documents and print them
        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")


def find_orders_containing_filter(db, collection_name, filter_type, complaint_type, user_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find orders containing the specified item
        query = {"user_id": int(user_id), filter_type: complaint_type}

        # Use the find method to retrieve matching documents
        cursor = collection.find(query)

        # Convert your cursor to a list to freely operate over it
        result = list(cursor)

        # Print the matching documents
        for document in result:
            print(document)

        # Return the whole result list
        return result

    except Exception as e:
        print(f"An error occurred: {e}")


def delete_record_by_id(db, collection_name, record_id, user_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Convert string to ObjectId
        record_object_id = ObjectId(record_id)

        # Define the query to find the document by its ID
        query = {"user_id" : int(user_id), "_id": record_object_id}

        # Use the delete_one method to delete the document
        result = collection.delete_one(query)

        # Check if the deletion was successful
        if result.deleted_count == 1:
            print(f"Successfully deleted record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id} for user with ID {user_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def update_item_by_id(db, collection_name, record_id, field_to_update, new_term, user_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Convert string to ObjectId
        record_object_id = ObjectId(record_id)

        # Define the query to find the document by its ID
        query = {"user_id" : int(user_id), "_id": record_object_id}

        # Use the update_one method to update the specific field (order_list)
        result = collection.update_one(query, {"$set": {field_to_update: new_term}})

        # Check if the update was successful
        if result.matched_count == 1:
            print(f"Successfully updated record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id} for user with ID {user_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def delete_record_by_item(db, collection_name, item="Pizza"):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"order_items.item_name": item}

        # Use the delete_one method to delete the document
        result = collection.delete_many(query)

        # Check if the deletion was successful
        if result.deleted_count >= 1:
            print(
                f"Successfully deleted {result.deleted_count} record that contains {item}"
            )
        else:
            print(f"No record found with {item}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def print_all_collections(db):
    all_collections = db.list_collection_names()

    for collection_index in range(len(all_collections)):
        print(f"{collection_index + 1}- {all_collections[collection_index]}")

    return all_collections


def portal_loop(user_id):

    print("Please pick the option that you want to proceed.\n"

          "1- Create a collection.\n"
          "2- Read all data in a collection.\n"
          "3- Read some part of the data while filtering.\n"
          "4- Insert data.\n"
          "5- Delete data.\n"
          "6- Update data.\n"
          )

    selected_option = input("Selected option: ")

    match int(selected_option):

        case 1:
            collection_name = input("name of your collection: ")
            createCollection(db, collection_name)

        case 2:
            all_collections = print_all_collections(db)

            selected_collection = int(input("Selected option: ")) - 1

            read_all_data(db, all_collections[selected_collection])

        case 3:
            all_collections = print_all_collections(db)

            selected_collection = int(input("Selected option: ")) - 1

            filter_type = input("search in: ")

            search_term = input("search for: ")

            find_orders_containing_filter(db, all_collections[selected_collection], filter_type, search_term, user_id)

        case 4:
            all_collections = print_all_collections(db)

            selected_collection = int(input("Selected option: ")) - 1

            data = input("enter data to be inserted:\n")

            data = json.loads(data)

            user_id = int(user_id)

            insert_into_collection(db, all_collections[selected_collection], data, user_id)

        case 5:
            all_collections = print_all_collections(db)

            selected_collection = int(input("Selected option: ")) - 1

            record_id = input("enter id of item to be deleted: ")

            delete_record_by_id(db, all_collections[selected_collection], record_id, user_id)

        case 6:
            all_collections = print_all_collections(db)

            selected_collection = int(input("Selected option: ")) - 1
            print("\n")

            field_to_update = input("enter field to update: ")

            new_term = input("enter new term: ")

            record_id = input("enter id of item to be updated: ")

            update_item_by_id(db, all_collections[selected_collection], record_id, field_to_update, new_term, user_id)

    return selected_option


def post_connection():
    if "complaints" not in db.list_collection_names():
        # Then create a collection
        createCollection(db, "complaints")

        # # Insert some dummy data into your collection
        for item in dummy_data:
            insert_into_collection(db, "complaints", item, item["user_id"])

    if "reports" not in db.list_collection_names():
        # Then create a collection
        createCollection(db, "reports")

        # # Insert some dummy data into your collection
        for item in dummy_data2:
            insert_into_collection(db, "reports", item, item["user_id"])


if __name__ == "__main__":
    # First create a connection
    db = connectDB()

    post_connection()

    print("Welcome to SQLchat Services Portal\n")

    user_id = input("Please enter your user id:\n")

    selected_option = portal_loop(user_id)

    while int(selected_option) != -1:
        print("What would you like to do next?\n")
        selected_option = portal_loop(user_id)



    #read_all_data(db, "complaints")
    # Try to find documents which contains a Pizza as an order item
    # found_documents = find_orders_containing_item(
    #     db, collection_name="orders", item_name="Pizza"
    # )

    # # Delete the first record which has a pizza in its order list
    # id_to_delete = found_documents[0]["_id"]
    # found_documents.pop(0)
    # delete_record_by_id(db, "orders", id_to_delete)

    # # Update the next item
    # id_to_update = found_documents[0]["_id"]
    # new_order_list = (
    #     [
    #         {"item_name": "Hamburger", "quantity": 1},
    #         {"item_name": "Fries", "quantity": 1},
    #         {"item_name": "Iced Tea", "quantity": 2},
    #     ],
    # )
    # update_order_list_by_id(db, "orders", id_to_update, new_order_list)
