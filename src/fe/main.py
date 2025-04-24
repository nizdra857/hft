from fastapi import FastAPI
import time

# Prometheus metrics
from prometheus_client import start_http_server, Summary
from prometheus_client import Counter, Histogram

# OpenTelemetry tracing
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Setup Tracing
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "fe-app"})
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
)
tracer = trace.get_tracer(__name__)

# Setup FastAPI
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Prometheus Metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TRADE_COUNTER = Counter('trades_total', 'Total number of trades')
TRADE_LATENCY = Histogram('trade_latency_seconds', 'Latency for trade endpoint')

# Start Prometheus metrics server
start_http_server(8000)  # This exposes metrics at localhost:8000/metrics

@app.get("/")
@REQUEST_TIME.time()
def read_root():
    return {"status": "Python Trading App running."}

@app.get("/trade")
@TRADE_LATENCY.time()
def simulate_trade():
    with tracer.start_as_current_span("simulate_trade"):
        time.sleep(0.1)
        TRADE_COUNTER.inc()
        return {"result": "Trade executed"}