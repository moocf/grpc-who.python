from concurrent import futures
import time
import grpc
import who_pb2
import who_pb2_grpc
import sys
import optparse
import subprocess


class Unit(who_pb2_grpc.WhoServicer):
  def Call(self, request, context):
    args = request.args.split('|')
    out = subprocess.check_output(["who", *args]).decode("utf-8") 
    print("\n$ who "+" ".join(args)+"\n"+out)
    return who_pb2.CallReply(out=out)


parser = optparse.OptionParser()
parser.set_defaults(address="[::]:50051")
parser.add_option("--address", dest="address", help="set server address")
parser.usage = "python server.py [--address <address>]"
(options, args) = parser.parse_args()

address = options.address
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
who_pb2_grpc.add_WhoServicer_to_server(Unit(), server)
server.add_insecure_port(address)
server.start()
print("Server started on "+address)
try:
    while True:
        time.sleep(1000)
except KeyboardInterrupt:
    server.stop(0)
