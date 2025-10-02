import grpc
import threading
from proto import users_pb2, users_pb2_grpc

def generate_messages(username):
    while True:
        text = input(f"{username}> ")
        yield users_pb2.ChatMessage(user=username, text=text)

def run(username="hemanth"):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        responses = stub.Chat(generate_messages(username))
        try:
            for resp in responses:
                print(f"[{resp.user}] {resp.text}")
        except grpc.RpcError as e:
            print("Chat ended:", e)

if __name__ == "__main__":
    name = input("Enter your username: ")
    run(name)
