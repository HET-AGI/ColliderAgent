---
name: magnus
description: Execute HEP blueprints (FeynRules, MadGraph5, MadAnalysis5, micrOmegas) on the remote Magnus station through the `magnus` CLI, and inspect, reconnect to, or download the results of those jobs. Use whenever a pipeline stage needs remote computation or a job's status, logs, or outputs.
---

# Magnus CLI

Every compute stage of this pipeline runs as a **blueprint job** on the remote `zhustation` site. This skill owns the mechanics every other skill relies on: connection check, submission, file upload and download, result inspection, recovery. The stage skills describe only their own blueprint's parameters and outputs.

## Connection

`magnus config` must report `Current:  zhustation` with an HTTPS address before the first job. If it does not, run `magnus login` once; credentials persist in `~/.magnus/config.json` for every shell. Do not start a local station, point at localhost, or inline `MAGNUS_ADDRESS`/`MAGNUS_TOKEN` per command: harness comparisons need every run on the same backend, and inline variables are neither persisted nor auditable. Never print, copy, or commit the token.

## Submitting a job

```bash
magnus blueprint schema <id>          # parameter names, types, which ones take files
magnus run <id> -- --key value ...    # submit and wait; prints the job ID and MAGNUS RESULT
```

- `--` separates CLI options (left) from blueprint arguments (right); it is optional when you pass no CLI options.
- A parameter typed `file_secret` takes a local path; the CLI uploads that file or directory before the job starts. Nothing else is uploaded, so every input the blueprint needs is passed explicitly.
- Blueprints that produce files append a `magnus receive` action; `magnus run` executes it and downloads into the blueprint's `--output` path. The download **replaces** that path: an existing directory is deleted first. Point `--output` at a directory you still need only when you want the new files to land inside it (launch writing `Events/` into the compiled process directory is the normal case).
- Every result is JSON with at least `success` (bool) and `message`. Read `success` before consuming anything else, and compare the reported values (`nevents`, `cross_section`, `run_name`, output paths) with what you requested: a blueprint can finish with `success: true` after MG5 silently ignored a parameter.

## Jobs longer than the shell timeout

A Bash tool call is cut off after 10 minutes by default, and `magnus run` blocks until the job and its download finish, so a large event-generation or micrOmegas job started in the foreground gets interrupted client-side while the job keeps running. For anything that may take longer than a few minutes, start it detached with its output in a log file, read the job ID from that log, poll `magnus status <job-id>` with short calls, and treat the `[Magnus] Saved to …` line in the log as the signal that the download is complete:

```bash
nohup magnus run madgraph-launch -- … > events/pp_x/launch.log 2>&1 &
grep -m1 "Job submitted" events/pp_x/launch.log     # job ID
until grep -q "Saved to\|Error" events/pp_x/launch.log; do sleep 300; done   # one call, ~9 min max per call
tail -3 events/pp_x/launch.log
```

Poll inside a single tool call with a `sleep 300` loop (a call may run up to 10 minutes), then repeat the same call until the log shows `Saved to` (downloaded) or an error. Dozens of short status calls in a row cost far more tokens than they save: every call re-reads the whole context, and the job does not finish sooner.

## Inspecting and recovering

```bash
magnus status <job-id>      # queued / running / completed
magnus logs <job-id>        # stdout + stderr of the cloud run
magnus job result <job-id>  # the MAGNUS RESULT JSON again
magnus jobs                 # recent jobs with IDs
magnus kill <job-id>        # free the cluster when the parameters were wrong
```

Use the absolute job ID printed at submission. Negative indices (`-1` = most recent) are scoped to the account, not the session, so they shift whenever another agent submits a job.

A job keeps running server-side when the client disconnects. After a timeout, a network drop, or an interrupted `magnus run`, do not resubmit: check `magnus status <job-id>` (wait 30 s and retry if the station itself is unreachable), then `magnus job result <job-id>`, and run the printed `magnus receive` command to download the outputs. If the station is unreachable twice in a row 20 s apart, stop the stage and report the outage with the job IDs; the run manifest and the finished upstream artifacts let the run resume without repeating successful jobs. Do not paste a large HTML error page into the conversation.

## Evidence for lessons

When a job fails, is retried, or completes with a parameter silently ignored, keep the job ID: the stage's lesson record (run-lessons skill) cites it as evidence.
