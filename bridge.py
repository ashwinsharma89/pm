#!/usr/bin/env python3
"""
Arsenal Transfer War Room - Live Bridge Server
================================================
Lightweight WebSocket server that connects the browser dashboard
to Claude Code for real-time two-way communication.

Usage:
    python3 bridge.py

The browser connects via ws://localhost:8765
Messages from the browser are written to bridge_inbox.jsonl
Responses can be sent back via the WebSocket.
"""

import asyncio
import json
import os
import time
from pathlib import Path

import websockets

INBOX = Path(__file__).parent / "bridge_inbox.jsonl"
OUTBOX = Path(__file__).parent / "bridge_outbox.jsonl"
PORT = 8765
CONNECTIONS = set()


async def handler(websocket):
    CONNECTIONS.add(websocket)
    remote = websocket.remote_address
    print(f"[BRIDGE] Client connected: {remote}")
    try:
        # Send any pending outbox messages on connect
        await flush_outbox(websocket)

        async for raw in websocket:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                msg = {"type": "raw", "content": raw}

            msg["_received_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            msg["_from"] = str(remote)

            # Append to inbox file
            with open(INBOX, "a") as f:
                f.write(json.dumps(msg) + "\n")

            print(f"[BRIDGE] Received: {msg.get('type', 'unknown')} from {remote}")

            # Acknowledge
            await websocket.send(json.dumps({
                "type": "ack",
                "message": "Received by Claude Code bridge. Processing...",
                "timestamp": msg["_received_at"],
            }))

    except websockets.ConnectionClosed:
        pass
    finally:
        CONNECTIONS.discard(websocket)
        print(f"[BRIDGE] Client disconnected: {remote}")


async def flush_outbox(websocket):
    """Send any queued outbox messages to the client."""
    if not OUTBOX.exists():
        return
    lines = OUTBOX.read_text().strip().split("\n")
    if not lines or lines == [""]:
        return
    for line in lines:
        if line.strip():
            await websocket.send(line.strip())
    # Clear outbox after sending
    OUTBOX.write_text("")


async def outbox_watcher():
    """Watch for new outbox messages and broadcast to all connected clients."""
    last_size = 0
    while True:
        await asyncio.sleep(1)
        if not OUTBOX.exists():
            continue
        current_size = OUTBOX.stat().st_size
        if current_size > last_size and current_size > 0:
            lines = OUTBOX.read_text().strip().split("\n")
            for line in lines:
                if line.strip():
                    for ws in CONNECTIONS.copy():
                        try:
                            await ws.send(line.strip())
                        except websockets.ConnectionClosed:
                            CONNECTIONS.discard(ws)
            OUTBOX.write_text("")
            last_size = 0
        else:
            last_size = current_size


async def main():
    print(f"[BRIDGE] Arsenal Transfer War Room Bridge Server")
    print(f"[BRIDGE] Listening on ws://localhost:{PORT}")
    print(f"[BRIDGE] Inbox: {INBOX}")
    print(f"[BRIDGE] Outbox: {OUTBOX}")
    print(f"[BRIDGE] Waiting for browser connection...")

    async with websockets.serve(handler, "localhost", PORT):
        await outbox_watcher()


if __name__ == "__main__":
    asyncio.run(main())
