import grpc
from proto import users_pb2, users_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)

        # Create a new user
        response = stub.CreateUser(
            users_pb2.CreateUserRequest(name="Charlie", email="charlie@example.com")
        )
        print("Created User:", response)

        # Fetch an existing user
        user = stub.GetUser(users_pb2.UserRequest(id=1))
        print("Fetched User:", user)

if __name__ == "__main__":
    run()


