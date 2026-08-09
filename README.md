# Distributed Rate Limiter with Redis

A Flask-based distributed API rate limiter using Redis.

## Features

- Redis-based rate limiting
- Client-specific limits
- Atomic Lua script
- HTTP 429 responses
- Retry-After header
- Docker Compose setup

## Technologies

- Python
- Flask
- Redis
- Docker
- Lua

## Installation

```bash
docker compose up --build
```

## Test

```bash
curl -H "X-Client-ID: kunal" http://localhost:5000/
```

## Rate Limit

100 requests per minute per client.

## Endpoints

GET /

GET /health

## Purpose

Day 296 demonstrates distributed API rate limiting using Redis.
