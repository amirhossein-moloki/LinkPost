#!/bin/bash
set -e

# Function to update task status in JSON file
update_task_status() {
  local task_id=$1
  local status=$2
  local log_file=$3
  local temp_file=$(mktemp)
  jq ".tasks[($task_id - 1)].status = \"$status\" | .tasks[($task_id - 1)].logs = \"$log_file\"" ".ci/tasks-status.json" > "$temp_file" && mv "$temp_file" ".ci/tasks-status.json"
}

# Get the total number of tasks
num_tasks=$(jq '.tasks | length' ".ci/tasks-status.json")

# Loop through all tasks
for ((i=1; i<=$num_tasks; i++)); do
  # Read task details
  task_name=$(jq -r ".tasks[($i - 1)].name" ".ci/tasks-status.json")
  task_status=$(jq -r ".tasks[($i - 1)].status" ".ci/tasks-status.json")
  log_file=".ci/logs/${task_name}.log"

  # Execute the task if its status is "pending"
  if [ "$task_status" == "pending" ]; then
    echo "Running task: $task_name"
    update_task_status "$i" "in_progress" "$log_file"

    # Make the script executable and run it, capturing output to the log file
    script_path=".ci/$task_name.sh"
    chmod +x "$script_path"
    if "$script_path" > "$log_file" 2>&1; then
      update_task_status "$i" "success" "$log_file"
      echo "Task $task_name completed successfully"
    else
      update_task_status "$i" "failed" "$log_file"
      echo "Task $task_name failed. See logs in $log_file" >&2
      exit 1
    fi
  else
    echo "Task $task_name is not pending, skipping."
  fi
done

echo "All tasks completed."
