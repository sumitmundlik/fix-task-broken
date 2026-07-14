There is an Apache-style access log at `/app/access.log`.

Write and run a program (any language available in the environment) that parses
this log file and produces a JSON summary report at `/app/report.json`.

`/app/report.json` must contain a single JSON object with exactly these three
fields:

1. `total_requests` (integer) — the total number of non-empty lines in
   `/app/access.log`.
2. `unique_ips` (integer) — the number of distinct client IP addresses, taken
   as the first whitespace-separated token on each log line.
3. `top_path` (string) — the request path that appears most often among all
   HTTP requests (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `PATCH`) in the log.
   Extract the path from the quoted request portion of the line, e.g.
   `"GET /index.html HTTP/1.1"` → `/index.html`.

Your submission is graded correct if and only if all of the following hold:

1. `/app/report.json` exists and contains valid JSON.
2. The JSON object has the three fields above (`total_requests`, `unique_ips`,
   `top_path`), with `total_requests`/`unique_ips` as integers and `top_path`
   as a string.
3. The value of every field exactly matches what a correct parse of
   `/app/access.log` produces.