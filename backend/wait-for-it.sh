#!/usr/bin/env bash
# wait-for-it.sh by vishnubob: https://github.com/vishnubob/wait-for-it

host="$1"
shift
port="$1"
shift

timeout=15
until pg_isready -h "$host" -p "$port"; do
  echo "⏳ Waiting for $host:$port to be ready..."
  sleep 1
  timeout=$((timeout - 1))
  if [ $timeout -le 0 ]; then
    echo "❌ Timed out waiting for $host:$port"
    exit 1
  fi
done

echo "✅ $host:$port is ready. Starting service..."
exec "$@"
