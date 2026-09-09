#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "decision-engine" / "engine.py"
AUDIT_PATH = Path(os.getenv("EVENT_AUDIT_PATH", "/tmp/greenops-events.jsonl"))
RECOMMENDATIONS: dict[str, dict[str, Any]] = {}


def _load_engine():
    spec = importlib.util.spec_from_file_location("greenops_decision_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Decision Engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = _load_engine()
POLICY = ENGINE.load_policy()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _correlation(headers: Any) -> str:
    return headers.get("X-Correlation-Id") or f"COR-{uuid.uuid4()}"


def _event(event_type: str, correlation_id: str, payload: dict[str, Any], causation_id: str | None = None) -> dict[str, Any]:
    return {
        "eventId": f"EVT-{uuid.uuid4()}",
        "eventType": event_type,
        "schemaVersion": "1.0",
        "occurredAt": _now(),
        "correlationId": correlation_id,
        "causationId": causation_id,
        "payload": payload,
    }


def _append_event(event: dict[str, Any]) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def _candidate_for_engine(payload: dict[str, Any]) -> dict[str, str]:
    required = {
        "candidate_id",
        "asset_id",
        "source_recommendation",
        "criticality",
        "data_quality",
        "ml_confidence",
        "security_clear",
        "budget_approved",
        "rto_rpo_compatible",
        "blocking_dependency",
    }
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"Missing fields: {','.join(missing)}")

    return {
        "candidate_id": str(payload["candidate_id"]),
        "asset_id": str(payload["asset_id"]),
        "source_recommendation": str(payload["source_recommendation"]),
        "criticality": str(payload["criticality"]),
        "data_quality": str(payload["data_quality"]),
        "ml_confidence": str(payload["ml_confidence"]),
        "security_clear": str(bool(payload["security_clear"])).lower(),
        "budget_approved": str(bool(payload["budget_approved"])).lower(),
        "rto_rpo_compatible": str(bool(payload["rto_rpo_compatible"])).lower(),
        "blocking_dependency": str(bool(payload["blocking_dependency"])).lower(),
    }


def evaluate(payload: dict[str, Any], correlation_id: str) -> dict[str, Any]:
    candidate = _candidate_for_engine(payload)
    result = ENGINE.decide(candidate, POLICY)
    recommendation_id = f"REC-{uuid.uuid4()}"
    response = {
        "recommendationId": recommendation_id,
        **result,
        "correlationId": correlation_id,
        "approvalStatus": "PENDING" if result["humanApprovalRequired"] else "NOT_REQUIRED",
    }
    RECOMMENDATIONS[recommendation_id] = response
    evt = _event("RecommendationGenerated", correlation_id, response)
    _append_event(evt)
    response["eventId"] = evt["eventId"]
    return response


def approve(recommendation_id: str, payload: dict[str, Any], correlation_id: str) -> dict[str, Any]:
    if recommendation_id not in RECOMMENDATIONS:
        raise KeyError("Recommendation not found")
    approved_by = str(payload.get("approvedBy", "")).strip()
    if not approved_by:
        raise ValueError("approvedBy is required")

    original = RECOMMENDATIONS[recommendation_id]
    approval = {
        "recommendationId": recommendation_id,
        "decision": original["decision"],
        "approvedBy": approved_by,
        "comment": str(payload.get("comment", "")),
        "approvalStatus": "APPROVED",
        "autoApplyAllowed": False,
        "changeApplied": False,
        "correlationId": correlation_id,
    }
    evt = _event("DecisionApproved", correlation_id, approval, causation_id=original.get("eventId"))
    _append_event(evt)
    approval["eventId"] = evt["eventId"]
    return approval


class Handler(BaseHTTPRequestHandler):
    server_version = "MayaBankGreenOpsAPI/0.1"

    def _write(self, status: int, body: dict[str, Any], correlation_id: str) -> None:
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("X-Correlation-Id", correlation_id)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        cid = _correlation(self.headers)
        if self.path == "/health/live":
            self._write(200, {"status": "UP"}, cid)
        elif self.path == "/health/ready":
            self._write(200, {"status": "READY", "policyVersion": POLICY["policyVersion"]}, cid)
        else:
            self._write(404, {"code": "NOT_FOUND", "correlationId": cid}, cid)

    def do_POST(self) -> None:
        cid = _correlation(self.headers)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size) or b"{}")
            if self.path == "/v1/recommendations/evaluate":
                self._write(200, evaluate(payload, cid), cid)
                return
            prefix = "/v1/recommendations/"
            suffix = "/approve"
            if self.path.startswith(prefix) and self.path.endswith(suffix):
                recommendation_id = self.path[len(prefix):-len(suffix)]
                self._write(200, approve(recommendation_id, payload, cid), cid)
                return
            self._write(404, {"code": "NOT_FOUND", "correlationId": cid}, cid)
        except KeyError as exc:
            self._write(404, {"code": "NOT_FOUND", "detail": str(exc), "correlationId": cid}, cid)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._write(400, {"code": "INVALID_REQUEST", "detail": str(exc), "correlationId": cid}, cid)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8090"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"MayaBank GreenOps Recommendation API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
