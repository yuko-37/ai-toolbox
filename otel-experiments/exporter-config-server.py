import os

from random import randint
from flask import Flask
from dotenv import load_dotenv
from time import time

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor



load_dotenv(override=True)
app = Flask(__name__)


resource = Resource.create(attributes={
    SERVICE_NAME: "otel-experiments"
})

tracerProvider = TracerProvider(resource=resource)
print(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")))
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

tracer = trace.get_tracer("my.tracer.name")


@app.route("/rolldice")
def roll_dice():
    with tracer.start_as_current_span("span-name") as span:
        span.add_event("test-event", {"key1": "value1", "key2": "value2"})
        # do some work that 'span' will track
        print("doing some work...")
        result = str(roll())
        return result


def roll():
    result = randint(1, 6)
    return result


if __name__ == '__main__':
    app.run(port=8090)