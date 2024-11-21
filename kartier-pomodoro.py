import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")

        # timer durations (default)
        self.work_duration = 25
        self.break_duration = 5
        self.sessions = 1
        self.current_session = 0
        self.is_running = False
        self.remaining_time = 0

        # widgets
        tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 18)).pack(pady=10)

        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 36))
        self.timer_label.pack(pady=20)

        # input
        self.work_input = self.create_input("Work Duration (minutes):", self.work_duration)
        self.break_input = self.create_input("Break Duration (minutes):", self.break_duration)
        self.sessions_input = self.create_input("Number of Sessions:", self.sessions)

        # buttons
        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, state=tk.DISABLED)
        self.reset_button.pack(pady=5)

    def create_input(self, label_text, default_value):
        """Helper to create labeled input fields."""
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=5)
        entry.insert(0, str(default_value))
        entry.pack(side=tk.RIGHT)
        return entry

    def start_timer(self):
        """Starts the Pomodoro timer based on user input."""
        try:
            # get user inputs
            self.work_duration = int(self.work_input.get())
            self.break_duration = int(self.break_input.get())
            self.sessions = int(self.sessions_input.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for durations and sessions.")
            return

        # initialize timer
        self.current_session = 1
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.start_work()

    def start_work(self):
        """Starts a work session."""
        if self.current_session <= self.sessions:
            self.is_running = True
            self.remaining_time = self.work_duration * 60
            self.update_timer(f"Work Session {self.current_session} of {self.sessions}")
        else:
            self.complete_all_sessions()

    def start_break(self):
        """Starts a break session."""
        self.is_running = True
        self.remaining_time = self.break_duration * 60
        self.update_timer("Break Time")

    def update_timer(self, label_text):
        """Updates the timer and countdown display."""
        self.timer_label.config(text=f"{label_text}")
        self.countdown()

    def countdown(self):
        """Performs the countdown."""
        if self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.root.after(1000, self.countdown)
        else:
            self.timer_ended()

    def timer_ended(self):
        """Handles end of work or break session."""
        if self.current_session <= self.sessions:
            if "Work" in self.timer_label.cget("text"):
              # work session ended
                messagebox.showinfo("Pomodoro Timer", "Work session ended! Time for a break.")
                self.start_break()
            else:
                # break session ended
                messagebox.showinfo("Pomodoro Timer", "Break session ended! Back to work.")
                self.current_session += 1
                self.start_work()

    def complete_all_sessions(self):
        """Marks all sessions as complete."""
        self.is_running = False
        self.timer_label.config(text="00:00")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        messagebox.showinfo("Pomodoro Timer", "All sessions completed! Great job!")

    def reset_timer(self):
        """Resets the timer and all inputs."""
        self.is_running = False
        self.timer_label.config(text="00:00")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.work_input.delete(0, tk.END)
        self.work_input.insert(0, str(self.work_duration))
        self.break_input.delete(0, tk.END)
        self.break_input.insert(0, str(self.break_duration))
        self.sessions_input.delete(0, tk.END)
        self.sessions_input.insert(0, str(self.sessions))


# run program
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
