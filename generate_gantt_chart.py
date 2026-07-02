
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def create_gantt_chart(data, output_path):
    df = pd.DataFrame(data)
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    df['duration'] = (df['end'] - df['start']).dt.days

    fig, ax = plt.subplots(figsize=(12, 8))

    for _i, task in df.iterrows():
        ax.barh(task['task'], task['duration'], left=task['start'], height=0.5, align='center', label=task['priority'])

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Task')
    plt.title('Implementation Roadmap Gantt Chart')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)

if __name__ == '__main__':
    gantt_data = [
        {'task': 'Testing Foundation', 'start': '2026-01-05', 'end': '2026-01-16', 'priority': 'P1'},
        {'task': 'Critical Test Coverage', 'start': '2026-01-19', 'end': '2026-02-06', 'priority': 'P1'},
        {'task': 'High-Priority Tests', 'start': '2026-02-09', 'end': '2026-02-20', 'priority': 'P1'},
        {'task': 'Medium-Priority Tests', 'start': '2026-02-23', 'end': '2026-02-27', 'priority': 'P1'},
        {'task': 'Test Validation', 'start': '2026-03-02', 'end': '2026-03-06', 'priority': 'P1'},
        {'task': 'Perf. Baseline', 'start': '2026-03-09', 'end': '2026-03-13', 'priority': 'P2'},
        {'task': 'Perf. Monitoring', 'start': '2026-03-16', 'end': '2026-03-20', 'priority': 'P2'},
        {'task': 'Doc. Infrastructure', 'start': '2026-03-09', 'end': '2026-03-13', 'priority': 'P3'},
        {'task': 'Doc. Enhancement', 'start': '2026-03-16', 'end': '2026-03-20', 'priority': 'P3'},
        {'task': 'Formatting Config', 'start': '2026-03-09', 'end': '2026-03-13', 'priority': 'P4'},
        {'task': 'Formatting CI/CD', 'start': '2026-03-16', 'end': '2026-03-20', 'priority': 'P4'},
        {'task': 'Component CI', 'start': '2026-03-16', 'end': '2026-03-20', 'priority': 'P5'},
        {'task': 'Integration Testing', 'start': '2026-03-23', 'end': '2026-03-27', 'priority': 'P5'},
        {'task': 'Release Automation', 'start': '2026-03-23', 'end': '2026-03-27', 'priority': 'P6'},
    ]
    create_gantt_chart(gantt_data, '/home/ubuntu/opencog-unified/gantt_chart.png')

