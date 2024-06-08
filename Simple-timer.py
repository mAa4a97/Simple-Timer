import tkinter as tk

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")

        self.time_left = 0
        self.running = False
        self.count_up = False
        self.timer_id = None

        # Default time input
        self.default_time_frame = tk.Frame(root)
        self.default_time_frame.pack(pady=5)
        tk.Label(self.default_time_frame, text="Set Default Time (HH:MM:SS):").pack(side=tk.LEFT)
        self.default_time_entry = tk.Entry(self.default_time_frame, width=10)
        self.default_time_entry.pack(side=tk.LEFT)
        self.default_time_entry.insert(0, "00:00:00")

        # Current time display
        self.current_time_frame = tk.Frame(root)
        self.current_time_frame.pack(pady=5)
        tk.Label(self.current_time_frame, text="Current Time:").pack(side=tk.LEFT)
        self.current_time_entry = tk.Entry(self.current_time_frame, width=10, font=("Helvetica", 24))
        self.current_time_entry.pack(side=tk.LEFT)
        self.current_time_entry.insert(0, "00:00")
        self.current_time_entry.configure(state='readonly')

        # Reverse checkbox
        self.reverse_var = tk.BooleanVar(value=False)
        self.reverse_checkbox = tk.Checkbutton(root, text="Reverse", variable=self.reverse_var, command=self.toggle_reverse)
        self.reverse_checkbox.pack(pady=5)

        # Control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)

        self.start_button = tk.Button(self.control_frame, text="▶", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(self.control_frame, text="||", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(self.control_frame, text="■", command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=5)

        # Adjustment buttons
        self.adjustment_frame = tk.Frame(root)
        self.adjustment_frame.pack(pady=5)

        self.adjustments = [
            ("-H", -3600), ("-M", -60), ("-S", -1),
            ("+H", 3600), ("+M", 60), ("+S", 1)
        ]

        for i, (text, delta) in enumerate(self.adjustments):
            button = tk.Button(self.adjustment_frame, text=text, command=lambda delta=delta: self.adjust_time(delta))
            button.grid(row=0, column=i, padx=2)

        self.file_path = "timer_output.txt"

    def start(self):
        if not self.running:
            self.running = True
            if self.reverse_var.get():
                self.count_up = True
            else:
                self.count_up = False
            self.parse_default_time()
            self.countdown()

    def pause(self):
        if self.running:
            self.root.after_cancel(self.timer_id)
            self.running = False

    def stop(self):
        if self.running:
            self.root.after_cancel(self.timer_id)
            self.running = False
        self.time_left = 0
        self.update_label()
        self.write_to_file()

    def adjust_time(self, delta):
        if self.time_left < 3600 and delta == -3600:
            return
        if self.time_left < 60 and delta in (-60, -3600):
            return
        self.time_left += delta
        if self.time_left < 0:
            self.time_left = 0
        self.update_label()
        self.write_to_file()

    def countdown(self):
        if self.running:
            if (self.count_up and self.time_left < self.target_time) or (not self.count_up and self.time_left > 0):
                self.time_left += 1 if self.count_up else -1
                self.update_label()
                self.write_to_file()
                self.timer_id = self.root.after(1000, self.countdown)
            else:
                self.running = False
                self.current_time_entry.configure(bg='red')

    def parse_default_time(self):
        default_time = self.default_time_entry.get()
        parts = list(map(int, default_time.split(':')))
        while len(parts) < 3:
            parts.insert(0, 0)
        h, m, s = parts
        self.target_time = h * 3600 + m * 60 + s
        if not self.count_up:
            self.time_left = self.target_time

    def update_label(self):
        minutes, seconds = divmod(abs(self.time_left), 60)
        hours, minutes = divmod(minutes, 60)
        sign = "-" if self.time_left < 0 else ""
        if hours > 0:
            time_str = f"{sign}{hours}:{minutes:02}:{seconds:02}"
        else:
            time_str = f"{sign}{minutes}:{seconds:02}"

        self.current_time_entry.configure(state='normal')
        self.current_time_entry.delete(0, tk.END)
        self.current_time_entry.insert(0, time_str)
        self.current_time_entry.configure(state='readonly')

    def write_to_file(self):
        with open(self.file_path, "w") as file:
            minutes, seconds = divmod(abs(self.time_left), 60)
            hours, minutes = divmod(minutes, 60)
            sign = "-" if self.time_left < 0 else ""
            if hours > 0:
                file.write(f"{sign}{hours}:{minutes:02}:{seconds:02}")
            else:
                file.write(f"{sign}{minutes}:{seconds:02}")

    def toggle_reverse(self):
        if self.reverse_var.get():
            self.count_up = True
        else:
            self.count_up = False

if __name__ == "__main__":
    root = tk.Tk()
    timer = Timer(root)
    root.mainloop()
