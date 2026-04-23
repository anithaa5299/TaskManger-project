import pika
import json

print("🔥 WORKER STARTING...", flush=True)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )

    channel = connection.channel()
    channel.queue_declare(queue="tasks")

    print("[WORKER] Connected to RabbitMQ", flush=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"[WORKER] Received task: {data}", flush=True)

    print("[WORKER] Waiting for messages...", flush=True)

    channel.basic_consume(
        queue="tasks",
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

except Exception as e:
    print("❌ WORKER ERROR:", e, flush=True)