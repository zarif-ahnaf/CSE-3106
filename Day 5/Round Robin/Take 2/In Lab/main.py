import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import deque
from typing import List, Dict, Tuple, Optional

# Type aliases
Process = Dict[str, int]
GanttEntry = Tuple[int, int, int]          # (pid, start_time, end_time)
QueueState = Tuple[int, List[int]]         # (time, list of pids in ready queue)
SchedulingResult = Dict[str, List]

def round_robin_scheduling(processes: List[Process], time_quantum: int) -> SchedulingResult:
    """
    Simulates Round Robin CPU scheduling with a FIFO ready queue (using deque).
    
    Args:
        processes: List of processes with 'pid', 'at', 'bt'
        time_quantum: Positive integer time slice
    
    Returns:
        Dict with 'processes', 'gantt_chart', 'ready_queue'
    """
    # Create mutable working copies
    proc_list: List[Process] = [
        {
            'pid': p['pid'],
            'at': p['at'],
            'bt': p['bt'],
            'remaining': p['bt']
        }
        for p in processes
    ]
    
    n: int = len(proc_list)
    for p in proc_list:
        p.update({'ct': 0, 'tat': 0, 'wt': 0})
    
    gantt_chart: List[GanttEntry] = []
    ready_queue_log: List[QueueState] = []
    current_time: int = 0
    completed: int = 0
    ready_queue: deque[Process] = deque()  # FIFO queue

    while completed < n:
        # Add newly arrived processes to the END of the ready queue (FIFO)
        for p in proc_list:
            if p['at'] <= current_time and p['remaining'] > 0 and p not in ready_queue:
                ready_queue.append(p)
        
        # Log current ready queue state (convert to list of pids)
        ready_queue_log.append((current_time, [proc['pid'] for proc in ready_queue]))
        
        if not ready_queue:
            # CPU idle: jump to next arrival time
            next_arrival: int = min(
                (p['at'] for p in proc_list if p['remaining'] > 0),
                default=current_time
            )
            current_time = next_arrival
            continue
        
        # Get next process from FRONT of queue (FIFO)
        current_proc: Process = ready_queue.popleft()
        exec_time: int = min(time_quantum, current_proc['remaining'])
        
        # Record execution in Gantt chart
        gantt_chart.append((current_proc['pid'], current_time, current_time + exec_time))
        current_time += exec_time
        current_proc['remaining'] -= exec_time
        
        # Add any processes that arrived DURING this time slice (to end of queue)
        for p in proc_list:
            if (
                p['at'] <= current_time 
                and p['remaining'] > 0 
                and p not in ready_queue 
                and p != current_proc
            ):
                ready_queue.append(p)
        
        # If not finished, put back at END of queue (FIFO discipline)
        if current_proc['remaining'] > 0:
            ready_queue.append(current_proc)
        else:
            # Process completed
            current_proc['ct'] = current_time
            current_proc['tat'] = current_proc['ct'] - current_proc['at']
            current_proc['wt'] = current_proc['tat'] - current_proc['bt']
            completed += 1

    return {
        'processes': proc_list,
        'gantt_chart': gantt_chart,
        'ready_queue': ready_queue_log
    }

def visualize_gantt_chart(gantt_data: List[GanttEntry]) -> None:
    """Visualize Gantt chart."""
    if not gantt_data:
        print("No Gantt chart data.")
        return

    fig, gnt = plt.subplots(figsize=(14, 3))
    max_time: int = max(end for _, _, end in gantt_data)
    gnt.set_xlim(0, max_time + 1)
    gnt.set_ylim(0, 10)
    gnt.set_xlabel('Time')
    gnt.set_yticks([])
    gnt.set_title('Gantt Chart - Round Robin Scheduling', fontsize=14)
    gnt.grid(True, axis='x', linestyle='--', alpha=0.6)

    # Handle matplotlib cm compatibility
    try:
        cmap = plt.cm.tab20
    except AttributeError:
        cmap = plt.cm.get_cmap('tab20')
    
    colors = cmap.colors if hasattr(cmap, 'colors') else cmap(range(20))

    for pid, start, end in gantt_data:
        color = colors[pid % len(colors)]
        gnt.broken_barh([(start, end - start)], (2, 6), facecolors=color, edgecolor='black')
        gnt.text((start + end) / 2, 5, f'P{pid}', ha='center', va='center',
                 fontweight='bold', color='white')

    plt.tight_layout()
    plt.show()

def visualize_execution_sequence(gantt_data: List[GanttEntry]) -> None:
    """Visualize the execution sequence with colored boxes and time labels below."""
    if not gantt_data:
        print("No execution data to visualize.")
        return

    # Get all unique time points
    time_points = sorted(set([t for entry in gantt_data for t in entry[1:]]))
    if not time_points:
        return
    
    # Create a figure with proper dimensions
    fig, ax = plt.subplots(figsize=(max(12, len(time_points) * 0.8), 2))
    
    # Set up the plot
    ax.set_xlim(0, time_points[-1])
    ax.set_ylim(0, 1)  # Only one row of boxes
    ax.set_xticks(time_points)
    ax.set_xticklabels([])
    ax.set_yticks([])
    
    # Remove all default spines and grid
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Draw grid lines manually - only vertical lines and bottom horizontal
    for t in time_points:
        ax.axvline(x=t, color='black', linewidth=1.2)
    
    # Draw bottom horizontal line
    ax.axhline(y=0, color='black', linewidth=1.2)
    
    # Assign colors to processes (same process = same color)
    process_colors = {}
    cmap = plt.cm.tab10
    for i, (pid, _, _) in enumerate(gantt_data):
        if pid not in process_colors:
            process_colors[pid] = cmap(i % 10)
    
    # Draw colored boxes for each process segment
    for pid, start, end in gantt_data:
        color = process_colors[pid]
        # Draw the box with color
        ax.add_patch(plt.Rectangle((start, 0), end - start, 1, 
                                 facecolor=color, edgecolor='black', linewidth=1.2))
        
        # Add process label
        ax.text((start + end) / 2, 0.5, f'P{pid}', 
               ha='center', va='center', fontsize=14, fontweight='bold', color='black')
    
    # Add time labels below the axis
    for t in time_points:
        ax.text(t, -0.2, f"{int(t)}", ha='center', va='top', fontsize=10, fontweight='bold')
    
    # Set title
    ax.set_title('Round Robin Execution Timeline', fontsize=14, pad=15)
    
    # Add extra space below for time labels
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()
    plt.show()

def read_processes_from_file(filename: str) -> List[Process]:
    """
    Read processes from CSV using built-in csv module.
    Expected columns: pid, at, bt
    """
    processes: List[Process] = []
    try:
        with open(filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            required = {'pid', 'at', 'bt'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError(f"Missing required columns: {required}. Found: {reader.fieldnames}")
            
            for i, row in enumerate(reader, start=2):
                try:
                    pid = int(row['pid'])
                    at = int(row['at'])
                    bt = int(row['bt'])
                    if bt <= 0:
                        raise ValueError("Burst time must be positive")
                    processes.append({'pid': pid, 'at': at, 'bt': bt})
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid data in row {i}: {e}") from e

        if not processes:
            raise ValueError("No valid processes found.")
        return processes

    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}") from e

def main() -> None:
    filename: str = input("Enter the input filename (e.g., processes.csv): ").strip()
    
    try:
        processes: List[Process] = read_processes_from_file(filename)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    try:
        time_quantum: int = int(input("What is the time quantum? "))
        if time_quantum <= 0:
            raise ValueError("Time quantum must be a positive integer.")
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        return

    print(f"\n✅ Loaded {len(processes)} processes | Time Quantum = {time_quantum}\n")

    result: SchedulingResult = round_robin_scheduling(processes, time_quantum)

    # Build result table
    table_rows: List[List[int]] = []
    for p in sorted(result['processes'], key=lambda x: x['pid']):
        table_rows.append([p['pid'], p['at'], p['bt'], p['ct'], p['tat'], p['wt']])
    
    avg_tat: float = sum(p['tat'] for p in result['processes']) / len(result['processes'])
    avg_wt: float = sum(p['wt'] for p in result['processes']) / len(result['processes'])

    print(tabulate(table_rows, headers=['PID', 'AT', 'BT', 'CT', 'TAT', 'WT'], tablefmt='grid'))
    print(f"\n📊 Average Turnaround Time: {avg_tat:.2f}")
    print(f"📊 Average Waiting Time: {avg_wt:.2f}")

    # Visualize
    visualize_gantt_chart(result['gantt_chart'])
    visualize_execution_sequence(result['gantt_chart'])

if __name__ == "__main__":
    main()