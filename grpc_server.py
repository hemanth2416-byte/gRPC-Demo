import grpc
from concurrent import futures
from proto import users_pb2, users_pb2_grpc

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}
next_id = 3

class UserService(users_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = users_db.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UserReply()
        return users_pb2.UserReply(**user)

    def CreateUser(self, request, context):
        global next_id
        user = {"id": next_id, "name": request.name, "email": request.email}
        users_db[next_id] = user
        next_id += 1
        return users_pb2.UserReply(**user)

    # NEW: Bi-directional streaming chat
    def Chat(self, request_iterator, context):
        for chat_msg in request_iterator:
            print(f"[{chat_msg.user}] {chat_msg.text}")
            # Echo it back to all
            yield users_pb2.ChatMessage(user=chat_msg.user, text=f"Echo: {chat_msg.text}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

