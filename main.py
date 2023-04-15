import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI Example")

        # Set up the Execute button
        self.execute_button = tk.Button(self.root, text="Execute", bg="green", fg="white", font=(
            "Arial", 16), command=self.execute)
        self.execute_button.pack(pady=20)

        # Set up the Record button
        self.record_button = tk.Button(self.root, text="Record", bg="red", fg="white", font=(
            "Arial", 16), command=self.record)
        self.record_button.pack(pady=20)

        # Set up the status label
        self.status_label = tk.Label(
            self.root, text="Ready to execute", font=("Arial", 16))
        self.status_label.pack(pady=20)

        self.recording = False

        self.root.mainloop()

    def execute(self):
        if self.recording:
            self.status_label.configure(text="Cannot execute while recording")
        else:
            self.status_label.configure(text="Executing...")
            # Execute code here

    def record(self):
        if not self.recording:
            self.recording = True
            self.status_label.configure(text="Recording...")
            # Start recording code here
        else:
            self.recording = False
            self.status_label.configure(text="Ready to execute")
            # Stop recording code here


if __name__ == "__main__":
    app = App()
