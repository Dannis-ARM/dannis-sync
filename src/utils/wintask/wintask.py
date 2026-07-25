
import logging
import subprocess
import argparse
import sys
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class TaskManager:
    """Manage Windows Scheduled Tasks via PowerShell ScheduledTasks module."""

    @staticmethod
    def _run_powershell(command):
        """Execute a PowerShell command and return (returncode, stdout, stderr)."""
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode, result.stdout or '', result.stderr or ''

    @staticmethod
    def add_task(
        task_name,
        exe_path,
        args_str=None,
        workdir=None,
        trigger_type="daily",
        time_str=None,
        days_str=None
    ):
        """Add a new scheduled task."""
        exe_p = Path(exe_path).resolve()

        if not exe_p.exists():
            logger.error(f"[X] Executable does not exist: {exe_p}")
            return

        if not time_str:
            logger.error("[X] --time is required (format: HH:MM)")
            return

        # Build action
        action_parts = [f'-Execute "{str(exe_p)}"']
        if args_str:
            action_parts.append(f'-Argument "{args_str}"')
        if workdir:
            workdir_p = Path(workdir).resolve()
            action_parts.append(f'-WorkingDirectory "{str(workdir_p)}"')
        else:
            action_parts.append(f'-WorkingDirectory "{str(exe_p.parent)}"')

        # Build action command
        action_cmd = f"New-ScheduledTaskAction {' '.join(action_parts)}"

        # Build trigger
        if trigger_type == "daily":
            trigger_cmd = f'New-ScheduledTaskTrigger -Daily -At "{time_str}"'
        elif trigger_type == "weekly":
            if not days_str:
                logger.error("[X] --days is required for weekly trigger (e.g., Mon,Tue,Wed)")
                return
            # Convert day names (Mon -&gt; Monday)
            day_map = {
                "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
                "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"
            }
            days = [d.strip() for d in days_str.split(",")]
            full_days = []
            for d in days:
                if d in day_map:
                    full_days.append(day_map[d])
                elif d in day_map.values():
                    full_days.append(d)
                else:
                    logger.error(f"[X] Invalid day: {d}")
                    return
            trigger_cmd = f'New-ScheduledTaskTrigger -Weekly -At "{time_str}" -DaysOfWeek {",".join(full_days)}'
        else:
            logger.error(f"[X] Unsupported trigger type: {trigger_type}")
            return

        ps_command = (
            f"$action = {action_cmd}; "
            f"$trigger = {trigger_cmd}; "
            f"Register-ScheduledTask -TaskName '{task_name}' -Action $action -Trigger $trigger -Force | Out-Null"
        )

        returncode, stdout, stderr = TaskManager._run_powershell(ps_command)

        if returncode == 0:
            logger.info(f"[+] Task '{task_name}' added successfully ")
        else:
            logger.error(f"[X] Failed to add task: {stderr}")

    @staticmethod
    def remove_task(task_name, skip_confirm=False):
        """Remove a scheduled task."""
        if not skip_confirm:
            confirm = input(f"[?] Are you sure you want to remove task '{task_name}'? (y/N): ")
            if confirm.lower() != 'y':
                logger.info("[-] Cancelled")
                return

        ps_command = f"Unregister-ScheduledTask -TaskName '{task_name}' -Confirm:$false -ErrorAction SilentlyContinue"
        returncode, stdout, stderr = TaskManager._run_powershell(ps_command)

        if returncode == 0:
            logger.info(f"[-] Task '{task_name}' removed successfully ")
        else:
            logger.error(f"[X] Failed to remove task: {stderr}")

    @staticmethod
    def list_tasks(full=False):
        """List scheduled tasks."""
        if full:
            ps_command = "Get-ScheduledTask -TaskPath '\\' | Select-Object TaskName, State, Description | ConvertTo-Json -Depth 10"
        else:
            ps_command = "Get-ScheduledTask -TaskPath '\\' | Select-Object TaskName, State | ConvertTo-Json -Depth 10"

        returncode, stdout, stderr = TaskManager._run_powershell(ps_command)

        if returncode != 0:
            logger.error(f"[X] Failed to list tasks: {stderr}")
            return

        try:
            tasks = json.loads(stdout)
            if isinstance(tasks, dict):
                tasks = [tasks]

            logger.info(" Scheduled Tasks:")
            for task in tasks:
                name = task.get("TaskName", "Unknown")
                state = task.get("State", "Unknown")
                if full:
                    desc = task.get("Description", "")
                    logger.info(f"  - {name} [{state}] {desc}")
                else:
                    logger.info(f"  - {name} [{state}]")
        except json.JSONDecodeError:
            logger.warning("[!] No tasks found or failed to parse output")

    @staticmethod
    def show_task(task_name):
        """Show details of a specific task."""
        ps_command = (
            f"Get-ScheduledTask -TaskName '{task_name}' -ErrorAction SilentlyContinue | "
            f"Select-Object TaskName, State, Description | ConvertTo-Json -Depth 10"
        )

        returncode, stdout, stderr = TaskManager._run_powershell(ps_command)

        if returncode != 0 or not stdout.strip():
            logger.error(f"[X] Task '{task_name}' not found")
            return

        try:
            task = json.loads(stdout)
            logger.info(f" Task: {task.get('TaskName')}")
            logger.info(f"   State: {task.get('State')}")
            logger.info(f"   Description: {task.get('Description', '(none)')}")
        except json.JSONDecodeError:
            logger.error(f"[X] Failed to parse task details")


def main():
    parser = argparse.ArgumentParser(
        description="Windows Task Scheduler Manager",
        epilog="Tip: Use 'taskschd.msc' to open Task Scheduler GUI for manual verification",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new scheduled task")
    add_parser.add_argument("task_name", help="Name of the task")
    add_parser.add_argument("--exe", required=True, help="Path to executable")
    add_parser.add_argument("--args", help="Arguments for the executable")
    add_parser.add_argument("--workdir", help="Working directory (default: exe directory)")
    add_parser.add_argument("--trigger", choices=["daily", "weekly"], default="daily", help="Trigger type (default: daily)")
    add_parser.add_argument("--time", required=True, help="Execution time (HH:MM)")
    add_parser.add_argument("--days", help="Days for weekly trigger (e.g., Mon,Tue,Wed)")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a scheduled task")
    remove_parser.add_argument("task_name", help="Name of the task")
    remove_parser.add_argument("--yes", action="store_true", help="Skip confirmation")

    # List command
    list_parser = subparsers.add_parser("list", help="List scheduled tasks")
    list_parser.add_argument("--full", action="store_true", help="Show full details")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_name", help="Name of the task")

    args = parser.parse_args()

    if args.command == "add":
        TaskManager.add_task(
            args.task_name,
            args.exe,
            args.args,
            args.workdir,
            args.trigger,
            args.time,
            args.days
        )
    elif args.command == "remove":
        TaskManager.remove_task(args.task_name, args.yes)
    elif args.command == "list":
        TaskManager.list_tasks(args.full)
    elif args.command == "show":
        TaskManager.show_task(args.task_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

