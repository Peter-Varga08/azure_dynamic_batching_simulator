# Global variables
import asyncio
import threading
import time
from queue import Empty, Queue

import torch
from transformers import BertForSequenceClassification, BertTokenizer

request_queue = Queue()
BATCH_SIZE = 8
TIMEOUT_MS = (
    10000  # Change this value to set the timeout in milliseconds for dynamic batching
)
model = None
tokenizer = None


def init():
    global model, tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
    model.eval()


def process_batch(batch):
    inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.logits.tolist()


def batch_processing_loop():
    while True:
        batch = []
        start_time = time.time()

        while len(batch) < BATCH_SIZE:
            # Timeout reached, process current batch
            if (time.time() - start_time) * 1000 > TIMEOUT_MS:
                print("Timeout has been reached.")
                break

            try:
                # Wait for a request to come in
                request = request_queue.get(timeout=TIMEOUT_MS / 1000)
                batch.append(request)
            except Empty:
                # No requests in the queue
                continue

        # Process the batch if we have requests
        if batch:
            texts = [req["text"] for req in batch]
            print(f"Processing {len(batch)} requests.")
            predictions = process_batch(texts)

            # Send back predictions to original requesters
            for i, request in enumerate(batch):
                request["future"].set_result(predictions[i])


def run(data):
    # Receive new requests
    future = asyncio.Future()
    request_queue.put({"text": data["text"], "future": future})

    # Wait for the batch processing loop to fulfill the request
    return future


init()
threading.Thread(target=batch_processing_loop, daemon=True).start()
