from concurrent import futures
from server import Server
from backend.client import Client
from backend.service import MESSAGE_TYPES
from backend.database import Database
import os
from os.path import exists
import time
import threading

class UnitTester:

    def __init__(self, db_filename = "test.db") -> None:
        # init db and servert
        self.db_filename = db_filename
        self.server = Server(dbname= self.db_filename, silent = True)
        self.PORT = self.server.PORT
        self.HOST = self.server.HOST
    
    # clear db for testing
    def reset_database(self):
        self.server.db.clear()
    
    # start ther server
    def run_server(self):
        self.server.run()
    
    # creating clients and connecting them to server
    def create_client(self):
        c = Client()
        c.connect(self.HOST, self.PORT)
        return c
    
    """
    Testing authentication services.
    """

    # login correctly
    def test_register_good(self, username: str, password: str, assert_message: str = "test_register_good: expected sucessful registration"):
        c1 = self.create_client()
        response = c1.register(username, password)
        assert response.success == True, assert_message

        return c1
    
    def test_login_good(self, username: str, password: str, assert_message: str = "test_login_good: expected sucessful login"):
        c1 = self.create_client()
        response = c1.login(username, password)
        assert response.success == True, assert_message

        return c1

    def test_bad_login(self, multiple: int = 1):
        # Case 1: Responds with failure for unregistered user
        self.reset_database()
        for i in range(multiple):
            c1 = self.create_client()
            response = c1.login("invalid_username", "invalid_password")
            assert response.success == False,  f"test_bad_login: expected login error for nonexistant user, attempt {i}"

    def test_register_good_and_bad(self):
        # Case 1: Responds with success for valid register
        self.reset_database()
        unames = ["test1", "test2"]

        for i in range(len(unames)):
            self.test_register_good(unames[i], "12345", f"test_register_good_and_bad: expected sucessful registration, attempt {i}")

        # Case 2: Responds with failure for duplicate register
        for i in range(len(unames)):
            c2 = self.create_client()
            response = c2.register(unames[i], "123456")
            assert response.success == False,  f"test_register_good_and_bad: expected unsucessful registration for same username, attempt {i}"


    def test_register_good_and_login_bad_and_login_good(self):
        # Case 1:  Responds with success for valid register
        self.reset_database()
        self.test_register_good("test1", "12345", f"test_register_good_and_login_bad_and_login_good: expected sucessful registration")

        # Case 2: user exists wrong password
        c2 = self.create_client()
        response = c2.login("test1", "wrong")
        assert response.success == False,  f"test_register_good_and_login_bad_and_login_good: expected failed login on wrong password"

        # Case 3: user exists right password
        self.test_login_good("test1", "12345", f"test_register_good_and_login_bad_and_login_good: expected successful login")

    # Testing the delete account feature
    def test_delete(self):
        self.reset_database()

        # constants
        username = "test1"
        password = "12345"

        # create an account
        c1 = self.test_register_good(username, password, f"test_delete: expected sucessful registration")

        # delete it
        c1.delete_account()
        message_type, response = c1.listen_for_updates()

        # Get a DeleteUserResponse message
        assert message_type == MESSAGE_TYPES.DeleteUserResponse,  f"test_delete: expected DeleteUserResponse message"

        # Get a deleted username in message
        assert response.username == username,  f"test_delete: expected deleted user's name"

        # Try delete again
        c1.delete_account()
        message_type, response = c1.listen_for_updates()

        # Get a Response message
        assert message_type == MESSAGE_TYPES.Response,  f"test_delete: expected Response message"

        # Should be failed
        assert response.success == False,  f"test_delete: expected failed second deletion"

        c1 = self.create_client()
        response = c1.login(username, password)

        # Failed login on deleted user
        assert response.success == False,  f"test_delete: expected login error for deleted user"

    """
    Testing chat services
    """
    # get user's stored messages
    def test_get_inbox(self, multiple = 1):
        self.reset_database()

        # Set up the user's credentials and message content
        username = "test"
        password = "12345"
        content = "Hello, world!"

        # Register the user and close the connection
        c1 = self.test_register_good(username, password, "test_get_inbox: expected successful registration 0")
        c1.close()

        # For each value in a specified range, register a new user and send them a message
        for i in range(multiple):
            c = self.test_register_good(f"test{i}", "blah", f"test_get_inbox: expected successful registration {i + 1}")
            c.send_message(username, content)

        # Log in to the user account and retrieve messages
        c1 =  self.test_login_good(username, password, "test_get_inbox: expected successful login")
        response = c1.get_messages()

        # Assert that the number of retrieved messages matches the expected number
        assert len(response) == multiple, f"test_get_inbox: expected to have {multiple} messages, found {len(response)}"

        # If messages were retrieved, assert that the first message is from the expected sender and contains the expected content
        if len(response) > 0:
            assert response[0].sender == "test0", f"test_get_inbox: expected to have first message from sender test0"
            assert response[0].content == content, f"test_get_inbox: expected message to be: {content}"



    def test_get_users(self, multiple = 1):
        self.reset_database()

        for i in range(multiple):
            c = self.test_register_good(f"test{i}", "blah", f"test_get_users: expected successful registration {i}")
            c.close()
        
        c1 = self.test_register_good("test", "12345", f"test_get_users: expected successful registration {multiple}")
        users = c1.get_users()

        # ensure the correct number of users are pulled
        assert len(users) == multiple, f"test_get_users: expected {multiple - 1} users in list"

        # ensure client doesn't pull their own name
        assert "test" not in users, f"test_get_users: expected user test not in list"

        # test to make sure usernames are correct
        if len(users) > 0:
            assert "test0" in users, f"test_get_users: expected user test0 in list"

        # register new account and ensure client 1 can detect this
        temp_username = "temp"
        temp_c = self.test_register_good(temp_username, "12345", f"test_get_users: expected successful registration for {temp_username}")

        message_type, response = c1.listen_for_updates()

        # Get a AddUserResponse message
        assert message_type == MESSAGE_TYPES.AddUserResponse,  f"test_get_users: expected AddUserResponse message"

        # Get a added username in message
        assert response.username == temp_username,  f"test_get_users: expected {temp_username}'s name"

        # delete new account and ensure client 1 can detect this
        temp_c.delete_account()
        message_type, response = c1.listen_for_updates()

        # Get a DeleteUserResponse message
        assert message_type == MESSAGE_TYPES.DeleteUserResponse,  f"test_get_users: expected DeleteUserResponse message"

        # Get a deleted username in message
        assert response.username == temp_username,  f"test_get_users: expected {temp_username}'s name"


    def test_messages_error(self):
        self.reset_database()

        invalid_user = "invalid_user"

        c1 = self.test_register_good("test", "12345", f"test_messages_error: expected successful registration")
        # send message to invalid username
        c1.send_message(invalid_user, "Doesn't matter")

        message_type, response = c1.listen_for_updates()

        # Get a Error message
        assert message_type == MESSAGE_TYPES.Error,  f"test_messages_error: expected Error message"

        # Get correct error message
        error_msg =  "Recipient user does not exist!"
        assert response.message == error_msg,  f"test_messages_error: expected '{error_msg}' error message"

        # make sure newly made invalid user has no messages 
        c2 = self.test_register_good(invalid_user, "12345", f"test_messages_error: expected successful registration 1")
        response = c2.get_messages()

        assert len(response) == 0, f"test_messages_error: expected to have 0 messages, found {len(response)}"
    
    def test_concurrent_messaging(self, multiple = 2):
        self.reset_database()

        for i in range(2):
            c = self.test_register_good(f"test{i}", "12345", f"test_concurrent_messaging: expected successful registration {i}")
            c.close()
            

        user0, user1 = "test0", "test1"
        msg0, msg1 = "foo", "bar"

        # log both users in
        c0 = self.test_login_good(user0, "12345", f"test_concurrent_messaging: expected successful login 0")
        c1 = self.test_login_good(user1, "12345", f"test_concurrent_messaging: expected successful login 1")

        # send messages
        c0.send_message(user1, msg0)
        c1.send_message(user0, msg1)

        message_type, response = c1.listen_for_updates()

        # Get a SingleMessageResponse message
        assert message_type == MESSAGE_TYPES.SingleMessageResponse,  f"test_concurrent_messaging: expected SingleMessageResponse message"

        # Get correct sender 
        assert response.sender == user0,  f"test_concurrent_messaging: expected sender to be {user0}"

        # Get correct content
        assert response.content == msg0,  f"test_concurrent_messaging: expected content to be {msg0}"

        # ignore the message received response
        _ = c0.listen_for_updates()
        message_type, response = c0.listen_for_updates()
        
        # Get a SingleMessageResponse message
        assert message_type == MESSAGE_TYPES.SingleMessageResponse,  f"test_concurrent_messaging: expected SingleMessageResponse message"

        # Get correct sender 
        assert response.sender == user1,  f"test_concurrent_messaging: expected sender to be {user1}"

        # Get correct content
        assert response.content == msg1,  f"test_concurrent_messaging: expected content to be {msg1}"



        
    def run_tests(self):
        self.test_bad_login()
        self.test_bad_login(multiple = 5)
        self.test_register_good_and_bad()
        self.test_register_good_and_login_bad_and_login_good()
        self.test_delete()
        self.test_get_inbox()
        self.test_get_inbox(multiple = 0)
        self.test_get_inbox(multiple = 5)
        self.test_get_users()
        self.test_get_users(multiple = 0)
        self.test_get_users(multiple = 5)
        self.test_messages_error()
        self.test_concurrent_messaging()



if __name__ == '__main__':
    tester = UnitTester()
    threading.Thread(target = tester.run_server, daemon= True).start()
    tester.run_tests()